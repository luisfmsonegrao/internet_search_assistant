# Web Search Assistant

The Web Search Assistant is an AI agent that answers user queries by retrieving relevant information from the web.

## Table of Contents

  - [Repository Contents](#Repository-contents)
  - [Search Assistant current architecture](#Search-Assistant-current-architecture)
  - [Detailed Search Assistant description](#detailed-Search-Assistant-description)
  - [Tech-stack summary](#Tech-stack-summary)
  - [Using Search Assistant](#Using-Search-Assistant)
  - [Deployment Strategy](#Deployment-Strategy)

## Repository contents

  - `\src` contains the Search Assistant source code.
  - `\notebooks` contains jupyter notebooks used for testing the assistant's functionalities.
  - `\resources` contains various resources such as figures or custom AWS Lambda Layers.

## Search Assistant current architecture
![Internet Search Assistant schema](./resources/figures/internet-search-assistant.png)

## Search Assistant detailed description

The Search Assistant is an AI agent that answers user queries by retrieving relevant information from the web.
  - Upon receiving a new user query, the assistant loads most-recent K user interactions from a database;
  - Based on the query and the past interactions, the assistant uses an LLM to decide whether web search, knowledge base search or no search are required to answer the query.
  - If web search is needed:
    - the LLM converts the query to a web query
    - the assistant uses `DuckDuckGo`to search the web for relevant information
    - retrieved PDF and HTML are parsed, chunked and ingested into a vector database
    - the query is augmented with the most-relevant L entries from the vector database
    - the LLM answers the query from the retrieved context information
  - If knowledge base search is needed (the query continues the topic of previous interactions):
    - the query is augmented with the most-relevant L entries from the vector database
    - the LLM answers the query from the retrieved context information
  - If no information is needed (e.g. common knowledge questions the LLM knows how to answer):
    - the LLM answers the query
  - Finally:
    - the assistant saves the new interaction to memory
    - the assistant returns the answer


