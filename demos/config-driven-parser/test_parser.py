import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class ParserCliTest(unittest.TestCase):
    def test_sample_csv_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "output.json"
            errors = Path(tmp) / "errors.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "parser.py"),
                    "--config", str(ROOT / "config.csv"),
                    "--input", str(ROOT / "input.csv"),
                    "--output", str(output),
                    "--errors", str(errors),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8")),
                json.loads((ROOT / "expected.json").read_text(encoding="utf-8")),
            )
            self.assertEqual(json.loads(errors.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()
