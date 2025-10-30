import boto3
from src.config import AWS_REGION, KNOWLEDGEBASE_ID

bedrock_agent = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)


def retrieve_kb_context(query, top_k=5):
    """
    Retrieve relevant context from Amazon Bedrock Knowledge database
    """
    response = bedrock_agent.retrieve(
        knowledgeBaseId=KNOWLEDGEBASE_ID,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": top_k}
        },
    )
    contexts = []
    for r in response.get("retrievalResults", []):
        contexts.append(
            {
                "text": r.get("content", {}).get("text", ""),
                "score": r.get("score"),
                "metadata": r.get("metadata"),
            }
        )
    return contexts
