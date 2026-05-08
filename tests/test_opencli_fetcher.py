import importlib.util
import io
import sys
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "opencli_fetcher.py"
SPEC = importlib.util.spec_from_file_location("opencli_fetcher", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module from {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OpenCliFetcherTests(unittest.TestCase):
    def test_prefers_opencli_on_posix(self):
        with mock.patch.object(MODULE.os, "name", "posix"):
            with mock.patch.object(MODULE.shutil, "which", side_effect=lambda name: "/usr/local/bin/opencli" if name == "opencli" else None):
                self.assertEqual(MODULE.resolve_opencli_command(), ["/usr/local/bin/opencli"])

    def test_uses_cmd_wrapper_on_windows(self):
        mapping = {
            "opencli": None,
            "opencli.cmd": r"C:\Program Files\nodejs\opencli.cmd",
            "opencli.exe": None,
            "opencli.bat": None,
            "opencli.ps1": r"C:\Program Files\nodejs\opencli.ps1",
        }
        with mock.patch.object(MODULE.os, "name", "nt"):
            with mock.patch.object(MODULE.shutil, "which", side_effect=lambda name: mapping.get(name)):
                self.assertEqual(
                    MODULE.resolve_opencli_command(),
                    [r"C:\Program Files\nodejs\opencli.cmd"],
                )

    def test_uses_powershell_when_only_ps1_exists_on_windows(self):
        mapping = {
            "opencli": None,
            "opencli.cmd": None,
            "opencli.exe": None,
            "opencli.bat": None,
            "opencli.ps1": r"C:\Program Files\nodejs\opencli.ps1",
        }
        with mock.patch.object(MODULE.os, "name", "nt"):
            with mock.patch.object(MODULE.shutil, "which", side_effect=lambda name: mapping.get(name)):
                self.assertEqual(
                    MODULE.resolve_opencli_command(),
                    [
                        "powershell",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        r"C:\Program Files\nodejs\opencli.ps1",
                    ],
                )

    def test_run_opencli_reports_missing_executable(self):
        with mock.patch.object(MODULE, "resolve_opencli_command", return_value=None):
            result = MODULE.run_opencli(["zhihu", "hot"])
        self.assertEqual(result["success"], False)
        self.assertIn("not found", result["error"])

    def test_emit_text_falls_back_when_stdout_cannot_encode(self):
        class BufferWrapper:
            def __init__(self):
                self.buffer = io.BytesIO()
                self.encoding = "gbk"

            def write(self, s):
                raise UnicodeEncodeError("gbk", s, 0, 1, "boom")

            def flush(self):
                return None

        wrapper = BufferWrapper()
        with mock.patch.object(sys, "stdout", wrapper):
            MODULE.emit_text("topic \u0e20\n")
        self.assertIn(b"topic ?", wrapper.buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
