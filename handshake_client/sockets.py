import socketio
import asyncio
from handshake_client.utils import get_logger

sio = socketio.AsyncClient()
logger = get_logger()


async def create_connection(url: str) -> socketio.AsyncClient:
    assert type(url) == str
    logger.info("get_connection start")
    if sio.connected is False:
        logger.info("connected false")
        await sio.connect(url)
    return sio


@sio.event
async def block(data):
    logger.info(data)


@sio.on('block')
def on_block(message):
    logger.info(message)


if __name__ == "__main__":
    url = "http://x:password@localhost:14037"
    asyncio.ensure_future(create_connection(url))
    asyncio.get_event_loop().run_forever()
    sio.disconnect()
