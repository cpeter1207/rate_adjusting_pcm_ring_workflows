#!/usr/bin/env python3
"""Exercise release staging without building or publishing production artifacts."""

import os
import re
import subprocess
import tarfile
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "3.0.0-alpha.1"
DEBIAN_VERSION = "3.0.0~alpha1-1"


def binary_release_commands():
    """Read the literal packaging step, leaving its shell behavior unchanged."""
    workflow = (ROOT / ".github/workflows/release.yml").read_text()
    match = re.search(
        r"^      - name: Build the ABI-major-\d+ shared object and Debian packages\n"
        r".*?^        run: \|\n(.*?)(?=^      - )",
        workflow,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError("binary release packaging step was not found")
    return textwrap.dedent(match[1])


def write_fixture(workspace, relative, contents, executable=False):
    """Place an input artifact or stand-in build command in a temporary tree."""
    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents)
    if executable:
        path.chmod(0o755)


class ReleaseContractTests(unittest.TestCase):
    def test_packages_abi3_artifacts_for_each_native_architecture(self):
        for architecture in ("amd64", "arm64"):
            with (
                self.subTest(architecture=architecture),
                tempfile.TemporaryDirectory() as tmp,
            ):
                workspace = Path(tmp)

                library = f"librate_adjusting_pcm_ring3.so.3.{VERSION}"
                write_fixture(workspace, f"build/{library}", "shared object fixture")
                write_fixture(
                    workspace, "build/rate_adjusting_pcm_ring3.pc", "pkg-config fixture"
                )
                write_fixture(
                    workspace,
                    "include/rate_adjusting_pcm_ring3/rate_adjusting_pcm_ring3.h",
                    "header fixture",
                )
                packages = [
                    f"{name}_{DEBIAN_VERSION}_{architecture}.deb"
                    for name in (
                        "librate-adjusting-pcm-ring3",
                        "librate-adjusting-pcm-ring3-dev",
                    )
                ]
                for package in packages:
                    write_fixture(workspace, f"build/debian-source/{package}", package)
                write_fixture(
                    workspace,
                    "Makefile",
                    ".PHONY: all debian-package-check\nall debian-package-check:\n\t@:\n",
                )
                write_fixture(
                    workspace,
                    "tools/run-in-quality-container.sh",
                    '#!/bin/sh\nshift\nexec "$@"\n',
                )
                write_fixture(
                    workspace,
                    "bin/dpkg",
                    f"#!/bin/sh\nprintf '%s\\n' '{architecture}'\n",
                    True,
                )
                write_fixture(
                    workspace,
                    "bin/dpkg-parsechangelog",
                    f"#!/bin/sh\nprintf '%s\\n' '{DEBIAN_VERSION}'\n",
                    True,
                )
                result = subprocess.run(
                    ["bash", "-eu", "-o", "pipefail", "-c", binary_release_commands()],
                    cwd=workspace,
                    env={
                        **os.environ,
                        "PATH": f"{workspace / 'bin'}:{os.environ['PATH']}",
                        "TAG": f"v{VERSION}",
                        "QUALITY_IMAGE": "fixture-image",
                    },
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                archive = (
                    workspace
                    / f"rate-adjusting-pcm-ring-v{VERSION}-debian13-{architecture}.tar.gz"
                )
                with tarfile.open(archive) as staged:
                    self.assertEqual(
                        set(staged.getnames()),
                        {
                            "abi3",
                            f"abi3/{library}",
                            "abi3/librate_adjusting_pcm_ring3.so.3",
                            "abi3/librate_adjusting_pcm_ring3.so",
                            "abi3/rate_adjusting_pcm_ring3.h",
                            "abi3/rate_adjusting_pcm_ring3.pc",
                        },
                    )
                    self.assertEqual(
                        staged.getmember(
                            "abi3/librate_adjusting_pcm_ring3.so.3"
                        ).linkname,
                        library,
                    )
                    self.assertEqual(
                        staged.getmember(
                            "abi3/librate_adjusting_pcm_ring3.so"
                        ).linkname,
                        "librate_adjusting_pcm_ring3.so.3",
                    )
                for package in packages:
                    self.assertEqual(
                        (workspace / "release" / package).read_text(), package
                    )

    def test_quality_and_release_default_to_the_required_adapter_release(self):
        for name in ("quality", "release"):
            with self.subTest(workflow=name):
                workflow = (ROOT / f".github/workflows/{name}.yml").read_text()
                adapter_input = workflow.split("      samplerate_adapter_tag:\n", 1)[
                    1
                ].split("\n\n", 1)[0]
                default = re.search(
                    r"^        default: (.+)$", adapter_input, re.MULTILINE
                )
                self.assertIsNotNone(default)
                self.assertEqual(default[1], "v0.1.0-alpha.3")


if __name__ == "__main__":
    unittest.main()
