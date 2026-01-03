import os
import subprocess
import sys


def test_demo_cli_runs():
    env = dict(os.environ, PYTHONPATH="src")
    # Run from the src directory to avoid package collision with root gardarika folder
    result = subprocess.run(
        [sys.executable, "-m", "gardarika.app", "demo"],
        env=env,
        cwd="src",
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Gardarika Demo" in result.stdout
    assert "Battle started" in result.stdout
    assert "Tax routed" in result.stdout


def test_render_cli_outputs_map():
    env = dict(os.environ, PYTHONPATH="src")
    # Run from the src directory to avoid package collision with root gardarika folder
    result = subprocess.run(
        [sys.executable, "-m", "gardarika.app", "render"],
        env=env,
        cwd="src",
        capture_output=True,
        text=True,
        check=True,
    )
    # 16 rows expected
    rows = [line for line in result.stdout.strip().splitlines() if line]
    assert len(rows) == 16
    assert any("P" in line for line in rows)
