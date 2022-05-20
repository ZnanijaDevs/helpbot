import os
import base64
from python_graphql_client import GraphqlClient


client = GraphqlClient(os.environ['BRAINLY_GRAPHQL_ENDPOINT_URL'])


def to_base64(id: str, prefix: str):
    """ Return the Base64 string with a prefix """
    encoded = base64.b64encode(
        bytes(f"{prefix}:{id}", 'utf-8')
    )

    return encoded.decode('utf-8')
