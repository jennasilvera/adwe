from datetime import datetime, timezone


LAST_HEARTBEAT: datetime | None = None


def record_heartbeat() -> None:
    global LAST_HEARTBEAT
    LAST_HEARTBEAT = datetime.now(timezone.utc)


def get_heartbeat() -> dict:
    return {
        "last_heartbeat": LAST_HEARTBEAT.isoformat() if LAST_HEARTBEAT else None,
    }
