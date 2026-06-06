from enum import StrEnum


class PatchStatus(StrEnum):
    PROPOSED = "proposed"
    APPLIED = "applied"
    APPLYING = "applying"
    REJECTED = "rejected"
    FAILED = "failed"
