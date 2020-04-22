import logging
import asyncio
from dataclasses import asdict
from handshake_client.sockets import get_connection
from handshake_client.chain import ChainEntry


async def main():
    logger = logging.getLogger()
    url = "http://localhost:14037"
    api_key = "your-api-key"
    sio = await get_connection(url, api_key)
    tip = await sio.call("get tip")
    tip_data = ChainEntry.from_raw(tip[1])
    logger.info(asdict(tip_data))

    @sio.on("chain connect")
    async def chain_connect(raw_data: bytes):
        """
        If run example command, print data
            $ hsd-cli rpc generate 1
        """
        chain_entry = ChainEntry.from_raw(raw_data)
        logger.info(asdict(chain_entry))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.ensure_future(main())
    asyncio.get_event_loop().run_forever()
