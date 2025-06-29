from authzed.api.v1 import AsyncClient
from grpcutil import bearer_token_credentials  # type: ignore[import-untyped]


def create_async_client(endpoint: str, token: str) -> AsyncClient:
    return AsyncClient(endpoint, bearer_token_credentials(token=token))
