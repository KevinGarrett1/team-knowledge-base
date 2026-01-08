import boto3
from langchain_aws import BedrockEmbeddings


def create_embeddings(
    region_name: str = "us-east-1",
    model_id: str = "amazon.titan-embed-text-v2:0",
):
    """
    Create and return a BedrockEmbeddings instance.

    This function is intentionally lazy:
    - No AWS calls are made at import time
    - boto3 client is created only when invoked
    - Safe to mock in unit tests
    """

    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=region_name,
    )

    return BedrockEmbeddings(
        client=client,
        model_id=model_id,
    )
