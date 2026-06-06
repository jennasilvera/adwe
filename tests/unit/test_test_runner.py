import sys

from adwe.services.test_runner import run_tests


def test_run_tests_success(tmp_path):
    result = run_tests(tmp_path, [sys.executable, "-c", "print('ok')"])

    assert result["passed"] is True
    assert result["exit_code"] == 0
    assert "ok" in result["stdout"]
