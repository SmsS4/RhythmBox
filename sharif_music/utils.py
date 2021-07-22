import uuid


def gen_id() -> int:
    return int(uuid.uuid1()) % 1_000_000_000
