import os

# assistant API Gateway endpoint
AGENT_API_URL = "https://xemcclumj8.execute-api.us-east-1.amazonaws.com/internet_search_assistant/internet-search-assistant"

# assistant state API Gateway endpoint
STATE_API_URL = "https://2e8gd55dkh.execute-api.us-east-1.amazonaws.com/state/state"

# Secret API Key
API_KEY = os.environ.get("ISA_API_KEY")

# Key string for bedrock knowledge base vector database
KNOWLEDGEBASE_SOURCE_URI_STRING = "x-amz-bedrock-kb-source-uri"

# ID of vector database
KNOWLEDGEBASE_ID = "JBUFV7WP0E"

# ID Of vector database data source
DATA_SOURCE_ID = "OSEESE71TJ"

# Text embedding model id
TEXT_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"

# Time to live of dynamodb database for past user interactions
INTERACTION_DB_TTL = 7200  # 2 hours

# Time to live of dynamo db database for state logs
STATE_DB_TTL = 7200  # 2 hours

# AWS Region
AWS_REGION = "us-east-1"

# BEDROCK LLM MODEL ID
BEDROCK_LLM_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# HISTORICAL CONTEXT SIZE
HISTORY_SIZE = 3

# RELEVANCE CONTEXT SIZE
CONTEXT_SIZE = 3

# MAXIMUM ALLOWED WEB SEARCH HITS
MAX_SEARCH_HITS = 1

# WEB SEARCH ENDPOINT
WEBSEARCH_ENDPOINT = "https://html.duckduckgo.com/html/"
