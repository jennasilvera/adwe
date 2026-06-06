from adwe.workers.heartbeat import HEARTBEAT_KEY


def test_worker_heartbeat_key():
    assert HEARTBEAT_KEY == "adwe:worker:last_heartbeat"
