import json
from decimal import Decimal
from typing import Optional, Union, List, Dict, Any
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from handshake_client.constant import TIMEOUT, COMMANDS


class RpcClient:
    """
    see https://hsd-dev.org/api-docs/index.html
    NOTE: Not done yet RPC Calls - Wallet https://hsd-dev.org/api-docs/index.html?shell--cli#rpc-calls-wallet
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
        self.url = f"{schema}://{user}:{api_key}@{host}:{port}"

    def rpc_call(self, method: str, *args) -> Any:
        assert type(method) == str
        try:
            r = AuthServiceProxy(self.url, method).__call__(*args)
            return r
        except (ConnectionRefusedError, JSONRPCException) as e:
            # return handshake Errors format
            return {"error": {"message": str(e)}}

    # RPC Calls - Node
    def stop(self) -> str:
        """
        Stops the running node.
        return: 'Stopping.'
        """
        return self.rpc_call("stop")

    def getinfo(self) -> Dict[str, Any]:
        return self.rpc_call("getinfo")

    def getmemoryinfo(self) -> Dict[str, Any]:
        return self.rpc_call("getmemoryinfo")

    def setloglevel(self, level: str) -> None:
        assert type(level) == str
        return self.rpc_call("setloglevel", level)

    def validateaddress(self, address: str) -> Dict[str, Any]:
        assert type(address) == str
        return self.rpc_call("validateaddress", address)

    def createmultisig(self, n_required: int, pubkeys: List[str]) -> Dict[str, Any]:
        """
        n_required: Required number of approvals for spending
        pubkeys: List of public keys
        """
        assert type(n_required) == int
        assert type(pubkeys) == list
        return self.rpc_call("createmultisig", n_required, pubkeys)

    def signmessagewithprivkey(self, privkey: str, message: str) -> Dict[str, Any]:
        """
        privkey: Private key
        message: Message you want to sign.
        """
        assert type(privkey) == str
        assert type(message) == str
        return self.rpc_call("signmessagewithprivkey", privkey, message)

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
        return self.rpc_call("verifymessage", address, signature, message)

    def setmocktime(self, timestamp: int) -> None:
        """
        Changes network time (This is consensus-critical)
        timestamp: unixtime
        """
        assert type(timestamp) == int
        return self.rpc_call("setmocktime", timestamp)

    # RPC Calls - Chain
    def pruneblockchain(self) -> None:
        """
        Prunes the blockchain, it will keep blocks specified in Network Configurations
        """
        return self.rpc_call("pruneblockchain")

    def invalidateblock(self, block_hash: str) -> None:
        """
        Invalidates the block in the chain. It will rewind network to blockhash and invalidate it.
        """
        return self.rpc_call("invalidateblock", block_hash)

    def reconsiderblock(self, block_hash: str) -> None:
        """
        This rpc command will remove block from invalid block set.
        """
        return self.rpc_call("reconsiderblock", block_hash)

    # RPC Calls - Block
    def getblockchaininfo(self) -> Dict[str, Any]:
        return self.rpc_call("getblockchaininfo")

    def getbestblockhash(self) -> str:
        return self.rpc_call("getbestblockhash")

    def getblockcount(self) -> int:
        return self.rpc_call("getblockcount")

    def getblock(
        self, block_hash: str, verbose: int = 1, details: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        assert type(details) == int
        return self.rpc_call("getblock", block_hash, verbose, details)

    def getblockbyheight(
        self, block_hash: str, verbose: int = 1, details: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        assert type(details) == int
        return self.rpc_call("getblockbyheight", block_hash, verbose, details)

    def getblockhash(self, height: int) -> str:
        assert type(height) == int
        return self.rpc_call("getblockhash", height)

    def getblockheader(
        self, block_hash: str, verbose: int = 1
    ) -> Union[str, Dict[str, Any]]:
        assert type(block_hash) == str
        assert type(verbose) == int
        return self.rpc_call("getblockheader", block_hash, verbose)

    def getchaintips(self) -> List[Dict[str, Any]]:
        return self.rpc_call("getchaintips")

    def getdifficulty(self) -> Decimal:
        return self.rpc_call("getdifficulty")

    # RPC Calls - Mempool
    def getmempoolinfo(self) -> Dict[str, Any]:
        return self.rpc_call("getmempoolinfo")

    def getmempoolancestors(
        self, tx_hash: str, verbose: int = 1
    ) -> Union[List[str], List[Dict[str, Any]]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.rpc_call("getmempoolancestors", tx_hash, verbose)

    def getmempooldescendants(
        self, tx_hash: str, verbose: int = 1
    ) -> Union[List[str], List[Dict[str, Any]]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.rpc_call("getmempooldescendants", tx_hash, verbose)

    def getmempoolentry(self, tx_hash: str) -> Dict[str, Any]:
        assert type(tx_hash) == str
        return self.rpc_call("getmempoolentry", tx_hash)

    def getrawmempool(self, verbose: int = 1) -> Dict[str, Any]:
        return self.rpc_call("getrawmempool", verbose)

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
        return self.rpc_call("prioritisetransaction", tx_hash, priority_delta, fee_delta)

    def estimatefee(self, n_blocks: int = 1) -> int:
        # TODO 返り値Decimalかfloatかも
        assert type(n_blocks) == int
        return self.rpc_call("estimatefee", n_blocks)

    def estimatepriority(self, n_blocks: int = 1) -> int:
        # TODO 返り値Decimalかfloatかも
        assert type(n_blocks) == int
        return self.rpc_call("estimatepriority", n_blocks)

    def estimatesmartfee(self, n_blocks: int = 1) -> Dict[str, Any]:
        assert type(n_blocks) == int
        return self.rpc_call("estimatesmartfee", n_blocks)

    def estimatesmartpriority(self, n_blocks: int = 1) -> Dict[str, Any]:
        assert type(n_blocks) == int
        return self.rpc_call("estimatesmartpriority", n_blocks)

    # RPC Calls - Transactions
    def gettxout(
        self, tx_hash: str, index: int, includemempool: int = 1
    ) -> Dict[str, Any]:
        assert type(tx_hash) == str
        assert type(index) == int
        assert type(includemempool) == int
        return self.rpc_call("gettxout", tx_hash, index, includemempool)

    def getrawtransaction(
        self, tx_hash: str, verbose: int = 0
    ) -> Union[str, Dict[str, Any]]:
        assert type(tx_hash) == str
        assert type(verbose) == int
        return self.rpc_call("getrawtransaction", tx_hash, verbose)

    def decoderawtransaction(self, raw_tx: str) -> Dict[str, Any]:
        assert type(raw_tx) == str
        return self.rpc_call("decoderawtransaction", raw_tx)

    def decodescript(self, script_hex: str) -> Dict[str, Any]:
        assert type(script_hex) == str
        return self.rpc_call("decodescript", script_hex)

    def sendrawtransaction(self, raw_tx: str) -> Dict[str, Any]:
        assert type(raw_tx) == str
        return self.rpc_call("sendrawtransaction", raw_tx)

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
        return self.rpc_call("createrawtransaction", outpoints, send_to, locktime)

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
        return self.rpc_call("signrawtransaction", raw_tx, inputs, privkey_list, sighashtype)

    def gettxoutproof(
        self, txid_list: List[str], block_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        assert type(txid_list) == list
        assert block_hash is None or type(block_hash) == str
        return self.rpc_call("gettxoutproof", txid_list, block_hash)

    def verifytxoutproof(self, proof: str) -> List[str]:
        assert type(proof) == str
        return self.rpc_call("verifytxoutproof", proof)

    # RPC Calls - Mining
    def getnetworkhashps(self, blocks: int, height: int) -> float:
        assert type(blocks) == int
        assert type(height) == int
        return self.rpc_call("getnetworkhashps", blocks, height)

    def getmininginfo(self) -> Dict[str, Any]:
        return self.rpc_call("getmininginfo")

    def getwork(self, data: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns hashing work to be solved by miner. Or submits solved block.
        data: required hex string. Data to be submitted to the network.
        """
        assert data is None or type(data) == str
        return self.rpc_call("getwork", data)

    def getworklp(self) -> Dict[str, Any]:
        return self.rpc_call("getworklp")

    def getblocktemplate(self, json_obj: Dict[str, Any]) -> Dict[str, Any]:
        """
        returns block template or proposal for use with mining. Also validates proposal if mode is specified as proposal.
        see https://hsd-dev.org/api-docs/index.html?shell--curl#getblocktemplate
        """
        assert type(json_obj) == dict
        return self.rpc_call("getblocktemplate", json_obj)

    def submitblock(self, block_data_by_hex: str) -> None:
        assert type(block_data_by_hex) == str
        return self.rpc_call("submitblock", block_data_by_hex)

    def verifyblock(self, block_data_by_hex: str) -> None:
        assert type(block_data_by_hex) == str
        return self.rpc_call("verifyblock", block_data_by_hex)

    def setgenerate(self, mining: int, proc_limit: int) -> bool:
        """
        Will start the mining on CPU.
        mining: 1 will start mining, 0 will stop.
        """
        assert mining in [0, 1]
        assert type(proc_limit) == int
        return self.rpc_call("setgenerate", mining, proc_limit)

    def getgenerate(self) -> Dict[str, Any]:
        return self.rpc_call("getgenerate")

    def generate(self, num_blocks: int, maxtries: Optional[int] = None) -> List[str]:
        assert type(num_blocks) == int
        assert maxtries is None or type(maxtries) == int
        return self.rpc_call("generate", num_blocks, maxtries)

    def generatetoaddress(self, num_blocks: int, address: str) -> List[str]:
        assert type(num_blocks) == int
        assert type(address) == str
        return self.rpc_call("generatetoaddress", num_blocks, address)

    # RPC Calls - Network
    def ping(self) -> None:
        return self.rpc_call("ping")

    def getpeerinfo(self) -> List[Dict[str, Any]]:
        return self.rpc_call("getpeerinfo")

    def addnode(self, ip_addr: str, cmd: str) -> None:
        """
        Adds or removes peers in Host List.
        ip_addr: IP Address of the Node.
        cmd: Command ex.
            add: Adds node to Host List and connects to it
            onetry: Tries to connect to the given node
            remove: Removes node from host list
        """
        assert type(ip_addr) == str
        assert cmd in COMMANDS
        return self.rpc_call("addnode", ip_addr, cmd)

    def disconnectnode(self, ip_addr: str) -> None:
        assert type(ip_addr) == str
        return self.rpc_call("disconnectnode")

    def getaddednodeinfo(self, ip_addr: str) -> List[Dict[str, Any]]:
        assert type(ip_addr) == str
        return self.rpc_call("getaddednodeinfo", ip_addr)

    def getnettotals(self) -> Dict[str, Any]:
        return self.rpc_call("getnettotals")

    def getnetworkinfo(self) -> Dict[str, Any]:
        return self.rpc_call("getnetworkinfo")

    def setban(self, ip_addr: str, cmd: str) -> None:
        assert type(ip_addr) == str
        assert cmd in COMMANDS
        return self.rpc_call("setban", ip_addr, cmd)

    def listbanned(self) -> List[Dict[str, Any]]:
        return self.rpc_call("listbanned")

    def clearbanned(self) -> None:
        return self.rpc_call("clearbanned")

    # RPC Calls - Names
    def getnameinfo(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("getnameinfo", name)

    def getnames(self) -> List[Dict[str, Any]]:
        """
        The result depends on the port.
        mainnet ex:
            12037 https://hsd-dev.org/api-docs/index.html?shell--curl#getnames-hsd
            12039 https://hsd-dev.org/api-docs/index.html?shell--curl#getnames-hsw
        """
        # NOTE: warning this does not yet support pagination
        return self.rpc_call("getnames")

    def getnamebyhash(self, name_hash: str) -> Dict[str, Any]:
        assert type(name_hash) == str
        return self.rpc_call("getnamebyhash", name_hash)

    def getnameresource(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("getnameresource", name)

    def getnameproof(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("getnameproof", name)

    def createclaim(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("createclaim", name)

    def sendclaim(self, name: str) -> None:
        assert type(name) == str
        return self.rpc_call("sendclaim", name)

    def sendrawclaim(self, claim_hex: str) -> None:
        assert type(claim_hex) == str
        return self.rpc_call("sendrawclaim", claim_hex)

    def sendrawairdrop(self, claim_hex: str) -> None:
        assert type(claim_hex) == str
        return self.rpc_call("sendrawairdrop", claim_hex)

    def grindname(self, length: int) -> None:
        """
        Grind a rolled-out available name.
        """
        assert type(length) == int
        return self.rpc_call("grindname")

    # RPC Calls - Wallet Auctions
    # port change(ex. mainnet port 12039)
    def getauctioninfo(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('getauctioninfo', name)

    def getbids(self) -> List[Dict[str, Any]]:
        return self.rpc_call('getbids')

    def getreveals(self) -> List[Dict[str, Any]]:
        return self.rpc_call('getreveals')

    def sendopen(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('sendopen', name)

    def sendbid(self, name: str, amount: float, lockup: float) -> Dict[str, Any]:
        assert type(name) == str
        assert type(amount) == float
        assert type(lockup) == float
        return self.rpc_call('sendbid', name, amount, lockup)

    def sendreveal(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('sendreveal', name)

    def sendredeem(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('sendredeem', name)

    def sendupdate(self, name: str, data: Dict[str, List[Dict[str, str]]]) -> Dict[str, Any]:
        """
        data: Resource Object see URL
        https://hsd-dev.org/api-docs/index.html?shell--cli#resource-object
        """
        assert type(name) == str
        assert type(data) == dict
        return self.rpc_call('sendupdate', name, json.dumps(data))

    def sendrenewal(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('sendrenewal', name)

    def sendtransfer(self, name: str, address: str) -> Dict[str, Any]:
        assert type(name) == str
        assert type(address) == str
        return self.rpc_call('sendtransfer', name, address)

    def sendfinalize(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call('sendfinalize', name)

    def sendcancel(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("sendcancel", name)

    def sendrevoke(self, name: str) -> Dict[str, Any]:
        assert type(name) == str
        return self.rpc_call("sendrevoke", name)

    def importnonce(self, name: str, address: str, value: float) -> Dict[str, Any]:
        assert type(name) == str
        assert type(address) == str
        assert type(value) == float
        return self.rpc_call("importnonce", name, address, value)
