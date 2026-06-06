from adwe.workers.arq_worker import WorkerSettings
from adwe.workers.patch_runner import apply_patch_job


def test_patch_worker_registered():
    assert apply_patch_job in WorkerSettings.functions
