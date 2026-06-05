from enum import StrEnum


class PatchStatus(StrEnum):
    PROPOSED = "proposed"
    APPLIED = "applied"
    FAILED = "failed"
