from adwe.api.patch_preview import _extract_changed_files


def test_extract_changed_files_from_diff():
    diff = """diff --git a/docs/example.md b/docs/example.md
new file mode 100644
--- /dev/null
+++ b/docs/example.md
@@ -0,0 +1,1 @@
+hello
"""

    assert _extract_changed_files(diff) == ["docs/example.md"]
