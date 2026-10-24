"""No provider/network access: regression tests for OGI-013 host package bootstrap."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "runners" / "ogi013_host_bootstrap.py"
spec = importlib.util.spec_from_file_location("ogi013_host_bootstrap", PATH)
host = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(host)


class HostBootstrapTests(TestCase):
    def test_tau2_runtime_requires_supported_python(self):
        with patch.object(host, "subprocess") as process:
            process.run.return_value.returncode = 0
            process.run.return_value.stdout = "3.11"
            with self.assertRaisesRegex(RuntimeError, "Python 3.12 or 3.13"):
                host.verify_python("/host/python")

    def test_only_official_local_tau2_source_is_admitted(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "src" / "tau2").mkdir(parents=True)
            project = root / "pyproject.toml"
            project.write_text(
                '[project.urls]\nRepository = "https://github.com/sierra-research/tau2-bench"\n'
            )
            host.verify_tau2_source(root)
            project.write_text(
                '[project.urls]\nRepository = "https://example.invalid/unrelated"\n'
            )
            with self.assertRaisesRegex(ValueError, "official"):
                host.verify_tau2_source(root)

    def test_pip_install_is_from_existing_checkout_not_pypi_tau2(self):
        with patch.object(host, "in_python", return_value=True), patch.object(host, "run") as call:
            host.install("/host/venv/bin/python", Path("/canonical/tau2-bench"))
        call.assert_called_once_with(
            "/host/venv/bin/python", "-m", "pip", "install",
            "--disable-pip-version-check", "-e", "/canonical/tau2-bench"
        )

    def test_launcher_requires_real_runner_and_canonical_sources(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(FileNotFoundError, "Host Python or requested"):
                host.main([
                    "--host-python", str(root / "python"),
                    "--tau2-checkout", str(root / "tau2-bench"),
                    "--components-root", str(root),
                    "--runner", str(root / "runner.py"),
                ])

    def test_runner_arguments_are_forwarded_unchanged(self):
        options = host.parse([
            "--host-python", "/host/venv/bin/python",
            "--tau2-checkout", "/source/tau2-bench",
            "--components-root", "/source/fruitstack",
            "--runner", "/eval/ogi013_tau2_run.py",
            "--task-limit", "3",
        ])
        self.assertEqual(options.runner_args, ["--task-limit", "3"])

    def test_launcher_preserves_host_python_venv_symlink(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "base-python"
            target.touch()
            host_python = root / "venv" / "bin" / "python"
            host_python.parent.mkdir(parents=True)
            host_python.symlink_to(target)
            tau2 = root / "tau2"
            runner = root / "runner.py"
            runner.touch()
            components = root / "components"
            for repo in host.COMPONENTS.values():
                checkout = components / repo
                checkout.mkdir(parents=True)
                (checkout / "pyproject.toml").touch()

            with (
                patch.object(host, "verify_python"),
                patch.object(host, "verify_tau2_source"),
                patch.object(host, "is_module_from_source", return_value=True),
                patch.object(host, "is_component_from_checkout", return_value=True),
                patch.object(host.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, stdout="abc\n")),
                patch.object(host, "run") as execute,
            ):
                host.main([
                    "--host-python", str(host_python),
                    "--tau2-checkout", str(tau2),
                    "--components-root", str(components),
                    "--runner", str(runner),
                ])

            self.assertEqual(execute.call_args.args[:2], (str(host_python), str(runner)))
