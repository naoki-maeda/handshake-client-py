from decimal import Decimal
from typing import Optional, Union, List, Dict, Any
from bitcoinrpc.authproxy import AuthServiceProxy
from handshake_client.constant import TIMEOUT


class RpcClient:
    """
    see https://hsd-dev.org/api-docs/index.html
    """

    def __init__(
        self,
        api_key: str,
        host: str,
        port: str,
        user: str = "x",
        ssl: bool = False,
        timeout: int = TIMEOUT,
    ):
        assert type(api_key) == str
        assert type(host) == str
        assert type(port) == str
        assert type(user) == str
        assert type(ssl) == bool
        assert type(timeout) == int
        schema: str = "http"
        if ssl is True:
            schema = "https"
        url = f"{schema}://{user}:{api_key}@{host}:{port}"
        self.proxy = AuthServiceProxy(url, timeout=timeout)

    # RPC Calls - Node
    def stop(self) -> str:
        """
        Stops the running node.
        return: 'Stopping.'
        """
        return self.proxy.stop()

    def getinfo(self) -> Dict[str, Any]:
        return self.proxy.getinfo()

    def getmemoryinfo(self) -> Dict[str, Any]:
        return self.proxy.getmemoryinfo()

    def setloglevel(self, level: str) -> None:
        assert type(level) == str
        self.proxy.setloglevel(level)

    def validateaddress(self, address: str) -> Dict[str, Any]:
        assert type(address) == str
        return self.proxy.validateaddress(address)

    def createmultisig(self, n_required: int, pubkeys: List[str]) -> Dict[str, Any]:
        """
        n_required: Required number of approvals for spending
        pubkeys: List of public keys
        """
        assert type(n_required) == int
        assert type(pubkeys) == list
        return self.proxy.createmultisig(n_required, pubkeys)

    def signmessagewithprivkey(self, privkey: str, message: str) -> Dict[str, Any]:
        """
        privkey: Private key
        message: Message you want to sign.
        """
        assert type(privkey) == str
        assert type(message) == str
        return self.proxy.signmessagewithprivkey(privkey, message)

    def verifymessage(
        self, address: str, signature: str, message: str
    ) -> Dict[str, Any]:
        """
        address: Address of the signer
        signature: Signature of signed message
        message: Message that was signed
        """
        assert type(address) == str
        assert type(signature) == str
        assert type(message) == str
        return self.proxy.verifymessage(address, signature, message)

    def setmocktime(self, timestamp: int) -> None:
        """
        Changes network time (This is consensus-critical)
        timestamp: unixtime
        """
        assert type(timestamp) == int
        self.proxy.setmocktime(timestamp)

    # RPC Calls - Chain
    def pruneblockchain(self) -> None:
        """
        Prunes the blockchain, it will keep blocks specified in Network Configurations
        """
        self.proxy.pruneblockchain()

    def invalidateblock(self, block_hash: str) -> None:
        """
        Invalidates the block in the chain. It will rewind network to blockhash and invalidate it.
        """
        self.proxy.invalidateblock(block_hash)

    def reconsiderblock(self, block_hash: str) -> None:
        """
        This rpc command will remove block from invalid block set.
        """
        self.proxy.reconsiderblock(block_hash)

    # RPC Calls - Block
    def getblockchaininfo(self) -> Dict[str, Any]:
        return self.proxy.getblockchaininfo()

    def getbestblockhash(self) -> str:
        return self.proxy.getbestblockhash()

    def getblockcount(self) -> int:
        return self.proxy.getblockcount()

    def getblock(
        self, block_hash: str, verbose: int = 1, details: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        assert type(details) == int
        return self.proxy.getblock(block_hash, verbose, details)

    def getblockbyheight(
        self, block_hash: str, verbose: int = 1, details: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        assert type(details) == int
        return self.proxy.getblockbyheight(block_hash, verbose, details)

    def getblockhash(self, height: int) -> str:
        assert type(height) == int
        return self.proxy.getblockhash(height)

    def getblockheader(
        self, block_hash: str, verbose: int = 1
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        return self.proxy.getblockheader(block_hash, verbose)

    def getchaintips(self) -> List[Dict[str, Any]]:
        return self.proxy.getchaintips()

    def getdifficulty(self) -> Decimal:
        return self.proxy.getdifficulty()

    # RPC Calls - Mempool
    def getmempoolinfo(self) -> Dict[str, Any]:
        return self.proxy.getmempoolinfo()

    def getmempoolancestors(
        self, tx_hash: str, verbose: int = 1
    ) -> Union[List[str], List[Dict[str, Any]]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.proxy.getmempoolancestors(tx_hash, verbose)

    def getmempooldescendants(
        self, tx_hash: str, verbose: int = 1
    ) -> Union[List[str], List[Dict[str, Any]]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.proxy.getmempooldescendants(tx_hash, verbose)

    def getmempoolentry(self, tx_hash: str) -> Dict[str, Any]:
        assert type(tx_hash) == str
        return self.proxy.getmempoolentry(tx_hash)

    def getrawmempool(self, verbose: int = 1) -> Dict[str, Any]:
        return self.proxy.getrawmempool(verbose)

    def prioritisetransaction(
        self, tx_hash: str, priority_delta: int, fee_delta: int
    ) -> bool:
        """
        Prioritises the transaction.
        Note: changing fee or priority will only trick local miner (using this mempool) into accepting Transaction(s) into the block. (even if Priority/Fee doesn't qualify)
        tx_hash: Transaction hash
        priority_delta: Virtual priority to add/subtract to the entry
        fee_delta: Virtual fee to add/subtract to the entry
        """
        assert type(tx_hash) == str
        assert type(priority_delta) == int
        assert type(fee_delta) == int
        return self.proxy.prioritisetransaction(tx_hash, priority_delta, fee_delta)

    def estimatefee(self, n_blocks: int = 1) -> int:
        # TODO 返り値Decimalかfloatかも
        assert type(n_blocks) == int
        return self.proxy.estimatefee(n_blocks)

    def estimatepriority(self, n_blocks: int = 1) -> int:
        # TODO 返り値Decimalかfloatかも
        assert type(n_blocks) == int
        return self.proxy.estimatepriority(n_blocks)

    def estimatesmartfee(self, n_blocks: int = 1) -> Dict[str, Any]:
        assert type(n_blocks) == int
        return self.proxy.estimatesmartfee(n_blocks)

    def estimatesmartpriority(self, n_blocks: int = 1) -> Dict[str, Any]:
        assert type(n_blocks) == int
        return self.proxy.estimatesmartpriority(n_blocks)

    # RPC Calls - Transactions
    def gettxout(
        self, tx_hash: str, index: int, includemempool: int = 1
    ) -> Dict[str, Any]:
        assert type(tx_hash) == str
        assert type(index) == int
        assert type(includemempool) == int
        return self.proxy.gettxout(tx_hash, index, includemempool)

    def getrawtransaction(
        self, tx_hash: str, verbose: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.proxy.getrawtransaction(tx_hash, verbose)

    def decoderawtransaction(self, raw_tx: str) -> Dict[str, Any]:
        assert type(raw_tx) == str
        return self.proxy.decoderawtransaction(raw_tx)

    def decodescript(self, script_hex: str) -> Dict[str, Any]:
        assert type(script_hex) == str
        return self.proxy.decodescript(script_hex)

    def sendrawtransaction(self, raw_tx: str) -> Dict[str, Any]:
        assert type(raw_tx) == str
        return self.proxy.sendrawtransaction(raw_tx)

    def createrawtransaction(
        self,
        outpoints: List[Dict[str, Any]],
        send_to: Dict[str, float],
        locktime: Optional[int] = None,
    ) -> str:
        """
        Creates raw, unsigned transaction without any formal verification.
        see https://hsd-dev.org/api-docs/index.html#createrawtransaction
        outpoints ex:
            [{ "txid": "'$txhash'", "vout": '$txindex' }]
        send_to ex:
            { "'$address'": '$amount', "data": "'$data'" }
        """
        assert type(outpoints) == list
        assert type(send_to) == dict
        assert locktime is None or type(locktime) == int
        return self.proxy.createrawtransaction(outpoints, send_to, locktime)

    def signrawtransaction(
        self,
        raw_tx: str,
        inputs: List[Dict[str, Any]],
        privkey_list: List[str],
        sighashtype: int = 1,
    ) -> Dict[str, Any]:
        """
        Signs raw transaction
        see https://hsd-dev.org/api-docs/index.html?shell--curl#signrawtransaction
        raw_tx:
            raw tx hex
        inputs ex:
            [{"txid": "'$txhash'", "vout": '$txindex', "address": "'$address'", "amount": '$amount'}]
        privkey_list:
            List of private keys
        sighashtype:
            Type of signature hash
            default 'ALL'
        """
        assert type(raw_tx) == str
        assert type(inputs) == list
        assert type(privkey_list) == str
        assert type(sighashtype) == int
        return self.proxy.signrawtransaction(raw_tx, inputs, privkey_list, sighashtype)

    def gettxoutproof(
        self, txid_list: List[str], block_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        assert type(txid_list) == list
        assert block_hash is None or type(block_hash) == str
        return self.proxy.gettxoutproof(txid_list, block_hash)

    def verifytxoutproof(self, proof: str) -> List[str]:
        assert type(proof) == str
        return self.proxy.verifytxoutproof(proof)
