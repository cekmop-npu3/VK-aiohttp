from aiohttp import ClientSession
from typing import TypeVar, Generic, Annotated, Optional, TypedDict

__all__ = (
    'Firebase',
)

Data = TypeVar('Data', bound=dict)


class AddData(TypedDict):
    name: Annotated[str, 'Auto generated hash-like key']


class Firebase(Generic[Data]):
    __slots__ = 'url', 'auth'

    def __init__(self, app_url: str, auth: Optional[Annotated[str, 'Database secret']] = None) -> None:
        self.url = app_url
        self.auth = {'auth': auth} if auth else None

    async def read(self, path: Annotated[str, 'Database endpoint'] = '') -> Optional[dict]:
        async with ClientSession() as session:
            async with session.get(
                    url=f'{self.url}/{path}' if path.endswith('.json') else f'{self.url}/{path}.json',
                    params=self.auth,
            ) as response:
                return await response.json()

    async def write(self, path: Annotated[str, 'Endpoint to overwrite'], data: Data) -> Data:
        async with ClientSession() as session:
            async with session.put(
                    url=f'{self.url}/{path}' if path.endswith('.json') else f'{self.url}/{path}.json',
                    params=self.auth,
                    json=data
            ) as response:
                return await response.json()

    async def add(self, path: Annotated[str, 'Endpoint to add data to'], data: dict) -> AddData:
        async with ClientSession() as session:
            async with session.post(
                    url=f'{self.url}/{path}' if path.endswith('.json') else f'{self.url}/{path}.json',
                    params=self.auth,
                    json=data
            ) as response:
                return await response.json()

    async def update(self, path: Annotated[str, 'Endpoint to update'], data: Data) -> Data:
        async with ClientSession() as session:
            async with session.patch(
                    url=f'{self.url}/{path}' if path.endswith('.json') else f'{self.url}/{path}.json',
                    params=self.auth,
                    json=data
            ) as response:
                return await response.json()

    async def delete(self, path: Annotated[str, 'Endpoint to be deleted']) -> None:
        async with ClientSession() as session:
            async with session.delete(
                    url=f'{self.url}/{path}' if path.endswith('.json') else f'{self.url}/{path}.json',
                    params=self.auth
            ) as response:
                return await response.json()
