import boto3
import time
from src.config import KNOWLEDGEBASE_ID, DATA_SOURCE_ID, AWS_REGION

kb_client = boto3.client("bedrock-agent")
bedrock = boto3.client(service_name="bedrock-runtime", region_name=AWS_REGION)
INGESTION_BATCH_SIZE = 25


def chunk_text(
    text, prefix, chunk_size=600, overlap=20
):  # need to optimize prefix to disambiguate similar queries that refer to different entities/dates/etc. Maybe also add keywords...
    """
    Split text into chunks. Append prefix to try to disambiguate chunks from different documents.
    """
    prefix = prefix + " Siemens annual report 2024"
    chunks = []
    start = 0
    prefix_size = len(prefix)
    while start < len(text):
        end = start + chunk_size - prefix_size
        chunk = prefix + text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap - prefix_size
    return chunks


def upload_to_knowledge_base(document): # Currently the assistant chunks web text and uploads to 
    """
    Store embedded chunks in a Bedrock Knowledge Base.
    """
    content = document.get("text_content")
    title = document.get("title")
    url = document.get("url")
    chunks = chunk_text(content, title)
    chunk_documents = make_documents(chunks, title, url)
    for doc_idx in range(0, len(chunk_documents), INGESTION_BATCH_SIZE):
        batch = chunk_documents[doc_idx : doc_idx + INGESTION_BATCH_SIZE - 1]
        batch = remove_present(batch)
        if batch:
            kb_client.ingest_knowledge_base_documents(
                knowledgeBaseId=KNOWLEDGEBASE_ID,
                dataSourceId=DATA_SOURCE_ID,
                documents=batch,
            )
            wait_for_completion(batch)
            print(f"DOCS: {doc_idx}-{doc_idx + INGESTION_BATCH_SIZE}\n")


def make_documents(chunks, title, url):
    """
    Format chunks for bedrock knowledge base
    """
    documents = []
    for idx, chunk in enumerate(chunks):
        doc = {
            "content": {
                "dataSourceType": "CUSTOM",
                "custom": {
                    "customDocumentIdentifier": {"id": f"{title}-{idx}"},
                    "sourceType": "IN_LINE",
                    "inlineContent": {"type": "TEXT", "textContent": {"data": chunk}},
                },
            },
            "metadata": {
                "type": "IN_LINE_ATTRIBUTE",
                "inlineAttributes": [
                    {"key": "url", "value": {"type": "STRING", "stringValue": url}}
                ],
            },
        }
        documents.append(doc)

    return documents


def wait_for_completion(batch):  # check if it's possible that this can get stuck, e.g. there are states not considered such as "FAILED"
    """
    Waits until all provided documents are ingested by knowledge base.
    """
    uris = [c["content"]["custom"]["customDocumentIdentifier"]["id"] for c in batch]
    remaining = set(uris)
    while remaining:
        doc_ids = [{"dataSourceType": "CUSTOM", "custom": {"id": r}} for r in remaining]

        resp = kb_client.get_knowledge_base_documents(
            knowledgeBaseId=KNOWLEDGEBASE_ID,
            dataSourceId=DATA_SOURCE_ID,
            documentIdentifiers=doc_ids,
        )

        for doc in resp["documentDetails"]:
            uri = doc["identifier"]["custom"]["id"]
            status = doc["status"]
            print(f"{uri} → {status}")

            if status in ["INDEXED", "PARTIALLY_INDEXED"]:
                remaining.discard(uri)

        if remaining:
            time.sleep(10)


def format_uris(uris):
    """
    Formta URIs to get documents from bedrock knowlegde base
    """
    doc_ids = [{"dataSourceType": "CUSTOM", "custom": {"id": r}} for r in uris]
    return doc_ids


def remove_present(batch):  # to be completed
    """
    Filter out documents that are already present in bedrock knowledge base
    """
    uris = [c["content"]["custom"]["customDocumentIdentifier"]["id"] for c in batch]
    doc_ids = format_uris(uris)
    st = kb_client.get_knowledge_base_documents(
        knowledgeBaseId=KNOWLEDGEBASE_ID,
        dataSourceId=DATA_SOURCE_ID,
        documentIdentifiers=doc_ids,
    )
    already_present = [
        i
        for (i, doc) in enumerate(st["documentDetails"])
        if doc["status"] not in ["NOT_FOUND", "FAILED", "PARTIALLY_INDEXED"]
    ]
    filtered_batch = [b for (i, b) in enumerate(batch) if i not in already_present]
    return filtered_batch
