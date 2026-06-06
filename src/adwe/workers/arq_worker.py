from adwe.workers.patch_runner import apply_patch_job
from adwe.workers.queue import get_redis_settings
from adwe.workers.workflow_runner import run_workflow


class WorkerSettings:
    functions = [run_workflow, apply_patch_job]
    redis_settings = get_redis_settings()
