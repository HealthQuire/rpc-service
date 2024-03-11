import asyncio
import pprint
import requests
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from os import environ
from dotenv import load_dotenv

if environ.get("USER_SERVICE") is None:
    load_dotenv()
USER_SERVICE = environ.get("USER_SERVICE")
RABBIT_URL = environ.get("RABBIT_URL")


async def resolve(method: str,
                  path: str,
                  params: dict = None,
                  json_data: dict = None,
                  headers: dict = None) -> tuple[dict, int]:
    print(f"Send {method} request to {path}")
    pprint.pprint(params)
    pprint.pprint(json_data)
    pprint.pprint(headers)
    service = path.split("/")[1]
    endpoint = "/".join(path.split("/")[2:])
    if method == "POST":
        function = requests.post
    elif method == "GET":
        function = requests.get
    elif method == "DELETE":
        function = requests.delete
    else:
        function = requests.patch
    if service == "user":
        res = function(USER_SERVICE + endpoint, json=json_data)
    return res.json(), res.status_code


async def server() -> None:
    connection = await connect_robust(RABBIT_URL)

    async with connection:
        channel = await connection.channel()
        rpc = await RPC.create(channel)
        await rpc.register(resolve.__name__, resolve, auto_delete=True)

        try:
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == "__main__":
    asyncio.run(server())
