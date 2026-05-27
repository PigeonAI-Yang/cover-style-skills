from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


PRODUCT_ROOT = Path(__file__).resolve().parents[1]


class McpPackageEntrypointTest(unittest.TestCase):
    def run_module(self, input_text: str, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        src_path = str(PRODUCT_ROOT / "src")
        env["PYTHONPATH"] = src_path + os.pathsep + env.get("PYTHONPATH", "")
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pigeonyang_cover_mcp.server",
                "--product-root",
                str(PRODUCT_ROOT),
                *args,
            ],
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            check=False,
        )

    def test_print_config(self) -> None:
        result = self.run_module("", "--print-config")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"product_root={PRODUCT_ROOT}", result.stdout)

    def test_stdio_tools_list(self) -> None:
        messages = "\n".join(
            [
                json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "notifications/initialized",
                        "params": {},
                    }
                ),
                json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
                "",
            ]
        )
        result = self.run_module(messages)
        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        tools = responses[-1]["result"]["tools"]
        names = {tool["name"] for tool in tools}
        self.assertIn("get_project_state", names)
        self.assertIn("list_generation_backends", names)
        self.assertIn("preflight_generation", names)
        self.assertIn("mark_final", names)


if __name__ == "__main__":
    unittest.main()
