from dishka import Provider, Scope, provide

from .spicedb import AsyncClient, create_async_client


class AccessControlProvider(Provider):
    def __init__(self, endpoint: str, token: str):
        super().__init__()
        self.spice_client = create_async_client(endpoint, token)

    @provide(scope=Scope.SESSION, provides=AsyncClient)
    async def _spice_client(self) -> AsyncClient:
        return self.spice_client
