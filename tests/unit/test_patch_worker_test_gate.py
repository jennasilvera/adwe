from pathlib import Path


def test_patch_worker_passes_test_command_to_patch_workflow():
    source = Path("src/adwe/workers/patch_runner.py").read_text()

    assert 'test_command=["python", "-m", "pytest"]' in source
