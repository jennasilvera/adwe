from adwe.workers.queue import get_redis_settings
from adwe.workers.workflow_runner import run_workflow


class WorkerSettings:
    functions = [run_workflow]
    redis_settings = get_redis_settings()
