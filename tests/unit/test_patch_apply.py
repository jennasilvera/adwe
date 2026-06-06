import subprocess

from adwe.services.patch_apply import apply_patch


def test_apply_patch(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)

    readme = tmp_path / "README.md"
    readme.write_text("hello\n")

    diff = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1 +1,2 @@
 hello
+world
"""

    apply_patch(tmp_path, diff)

    assert readme.read_text() == "hello\nworld\n"
