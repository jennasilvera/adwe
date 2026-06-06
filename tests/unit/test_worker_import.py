from adwe.workers.workflow_runner import run_workflow


def test_worker_imports():
    assert callable(run_workflow)
