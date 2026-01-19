import os
import subprocess
import sys


def test_demo_cli_runs():
    # Execute in src directory so it picks up the src/gardarika package
    result = subprocess.run(
        [sys.executable, "-m", "gardarika.app", "demo"],
        cwd="src",
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Gardarika Demo" in result.stdout
    assert "Battle started" in result.stdout
    assert "Tax routed" in result.stdout


def test_render_cli_outputs_map():
    # Execute in src directory so it picks up the src/gardarika package
    result = subprocess.run(
        [sys.executable, "-m", "gardarika.app", "render"],
        cwd="src",
        capture_output=True,
        text=True,
        check=True,
    )
    # 16 rows expected
    rows = [line for line in result.stdout.strip().splitlines() if line]
    assert len(rows) == 16
    assert any("P" in line for line in rows)
