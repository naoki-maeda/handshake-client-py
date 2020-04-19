from dataclasses import dataclass


@dataclass()
class ChainEntry:
    hash: str
    height: int
    nonce: int
    time: int
    prevBlock: str
    treeRoot: str
    extraNonce: str
    reservedRoot: str
    witnessRoot: str
    merkleRoot: str
    version: int
    bits: int
    mask: str
    chainwork: str

    @classmethod
    def from_raw(cls, buffer: bytes):
        """
        create dataclass from chain data
        fixed length?
        """
        assert len(buffer) == 304
        block_hash = to_str(buffer[:32])
        height = to_int(buffer[32:36])
        nonce = to_int(buffer[36:40])
        time = to_int(buffer[40:48])
        prevBlock = to_str(buffer[48:80])
        treeRoot = to_str(buffer[80:112])
        extraNonce = to_str(buffer[112:136])
        reservedRoot = to_str(buffer[136:168])
        witnessRoot = to_str(buffer[168:200])
        merkleRoot = to_str(buffer[200:232])
        version = to_int(buffer[232:236])
        bits = to_int(buffer[236:240])
        mask = to_str(buffer[240:272])
        chainwork = to_str(buffer[272:304])
        return ChainEntry(
            block_hash,
            height,
            nonce,
            time,
            prevBlock,
            treeRoot,
            extraNonce,
            reservedRoot,
            witnessRoot,
            merkleRoot,
            version,
            bits,
            mask,
            chainwork,
        )


def to_int(buf: bytes) -> int:
    """
    bytes to int(little endian)
    """
    return int.from_bytes(buf, byteorder="little")


def to_str(buf: bytes) -> str:
    """
    bytes to str
    """
    return buf.hex()
