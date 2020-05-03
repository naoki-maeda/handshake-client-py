from handshake_client.http_ import HttpClient


if __name__ == "__main__":
    # network regtest
    client = HttpClient(
        api_key="YOUR API KEY", host="localhost", port="14037", user="x", ssl=False
    )
    print(client.get_info())
