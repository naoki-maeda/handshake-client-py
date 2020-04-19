import logging
import socketio
from typing import List
from dataclasses import asdict
from handshake_client.chain import ChainEntry


logger = logging.getLogger("handshake.socket")
sio = socketio.AsyncClient(logger=logger)


async def get_connection(
    url: str, api_key: str, watch_chain: bool = True
) -> socketio.AsyncClient:
    """
    see https://hsd-dev.org/guides/events.html
    """
    assert type(url) == str
    assert type(api_key) == str
    assert type(watch_chain) == bool
    if sio.connected is False:
        await sio.connect(url, transports=["websocket"])
        await sio.call("auth", api_key)
        if watch_chain:
            await sio.call("watch chain")
    return sio


@sio.event
async def disconnect() -> None:
    logger.info("closing socket connection")
    if sio.connected:
        await sio.disconnect()


@sio.on("chain connect")
async def chain_connect(raw_data: bytes):
    chain_entry = ChainEntry.from_raw(raw_data)
    logger.info(asdict(chain_entry))


@sio.on("block connect")
async def block_connect(raw_data: bytes, block: List):
    """
    TODO: block typing: List[Tx]
    """
    chain_entry = ChainEntry.from_raw(raw_data)
    logger.info(asdict(chain_entry))
