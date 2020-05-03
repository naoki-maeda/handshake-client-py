from handshake_client.rpc import RpcClient


if __name__ == "__main__":
    # network regtest
    rpc_client = RpcClient("password", "localhost", "12037")
    print(rpc_client.getinfo())
    print(rpc_client.getblockchaininfo())
