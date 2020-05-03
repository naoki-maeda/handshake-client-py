import logging
import socketio


logger = logging.getLogger("handshake.socket")
sio = socketio.AsyncClient(logger=logger)


async def get_connection(
    url: str, api_key: str, watch_chain: bool = True, watch_mempool: bool = True,
) -> socketio.AsyncClient:
    """
    see https://hsd-dev.org/guides/events.html
    """
    assert type(url) == str
    assert type(api_key) == str
    assert type(watch_chain) == bool
    assert type(watch_mempool) == bool
    if sio.connected is False:
        await sio.connect(url, transports=["websocket"])
        await sio.call("auth", api_key)
        if watch_chain:
            await sio.call("watch chain")
        if watch_mempool:
            await sio.call("watch mempool")
    return sio


@sio.event
async def disconnect() -> None:
    logger.info("closing socket connection")
    if sio.connected:
        await sio.disconnect()


async def get_wallet_connection(
    url: str, api_key: str, wallet_id: str = "*",
) -> socketio.AsyncClient:
    """
    see https://hsd-dev.org/guides/events.html
    """
    assert type(url) == str
    assert type(api_key) == str
    assert type(wallet_id) == str
    if sio.connected is False:
        await sio.connect(url, transports=["websocket"])
        await sio.call("auth", api_key)
        await sio.call("join", wallet_id)
    return sio
