import os
import re
import base64
from python_graphql_client import GraphqlClient


client = GraphqlClient(os.environ['BRAINLY_GRAPHQL_ENDPOINT_URL'])


def to_base64(id: str, prefix: str):
    """ Return the Base64 string with a prefix """
    encoded = base64.b64encode(
        bytes(f"{prefix}:{id}", 'utf-8')
    )

    return encoded.decode('utf-8')


class BrainlyGraphQLException(Exception):
    """Raise for errors related to the Brainly GraphQL API"""


async def get_question(id: int):
    data = await client.execute_async(query="""
        query GetQuestion($id: ID!) {
            question(id: $id) {
                subject {name}
                content
                answers { nodes {content} }
            }
        }
    """, variables={
        'id': to_base64(str(id), 'question')
    })

    if 'errors' in data:
        raise BrainlyGraphQLException(f"An error has occured while trying to fetch Brainly: {data}")

    question = data['data']['question']

    if question is None:
        raise BrainlyGraphQLException(f"Question {id} does not exist")

    question['content'] = re.sub(r"<\w+\s?\/?>", '', question['content'])
    question['short_content'] = f"{question['content'][:300]}..." if len(question['content']) > 300 else question['content']
    question['answers_count'] = len(question['answers']['nodes'])

    return question
