from handshake_client.rpc import RpcClient


if __name__ == "__main__":
    # network regtest
    rpc_client = RpcClient("password", "localhost", "14039")
    rpc_client.rpc_call("sendtoaddress", "rs1q4n2ac0xlfgx239ucfavfus5wl7e68qzcj3gwnd", 1)
