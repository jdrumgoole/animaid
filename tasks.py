"""Invoke tasks for animaid project."""

import signal
import sys
from pathlib import Path

from invoke import task
from invoke.context import Context

# PID file for tracking tutorial server
TUTORIAL_PID_FILE = Path(".tutorial.pid")


@task
def install(c: Context, dev: bool = False, docs: bool = False) -> None:
    """Install the package and dependencies."""
    extras = []
    if dev:
        extras.append("dev")
    if docs:
        extras.append("docs")

    if extras:
        c.run(f"uv pip install -e '.[{','.join(extras)}]'")
    else:
        c.run("uv pip install -e .")


@task
def test(c: Context, verbose: bool = False, cov: bool = False) -> None:
    """Run tests with pytest."""
    cmd = "uv run pytest"
    if verbose:
        cmd += " -v"
    if cov:
        cmd += " --cov=animaid --cov-report=term-missing"
    c.run(cmd, pty=True)


@task
def lint(c: Context, fix: bool = False) -> None:
    """Run ruff linter."""
    cmd = "uv run ruff check src tests"
    if fix:
        cmd += " --fix"
    c.run(cmd, pty=True)


@task
def format(c: Context, check: bool = False) -> None:
    """Format code with ruff."""
    cmd = "uv run ruff format src tests"
    if check:
        cmd += " --check"
    c.run(cmd, pty=True)


@task
def typecheck(c: Context) -> None:
    """Run mypy type checker."""
    c.run("uv run mypy src", pty=True)


@task
def check(c: Context) -> None:
    """Run all checks (lint, format, typecheck, test)."""
    lint(c)
    format(c, check=True)
    typecheck(c)
    test(c)


@task
def docs(c: Context) -> None:
    """Build Sphinx documentation."""
    c.run("uv run sphinx-build -b html docs docs/_build/html", pty=True)


@task
def docs_serve(c: Context, port: int = 8200) -> None:
    """Serve documentation locally."""
    c.run(f"uv run python -m http.server {port} -d docs/_build/html", pty=True)


@task
def clean(c: Context) -> None:
    """Clean build artifacts."""
    patterns = [
        "dist",
        "build",
        "*.egg-info",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "docs/_build",
        "**/__pycache__",
        "**/*.pyc",
    ]
    for pattern in patterns:
        c.run(f"rm -rf {pattern}", warn=True)


@task
def build(c: Context) -> None:
    """Build the package."""
    clean(c)
    c.run("uv build")


@task
def version(c: Context) -> None:
    """Show current version."""
    c.run("uv run python -c 'import animaid; print(animaid.__version__)'")


@task
def bump_version(c: Context, part: str = "patch") -> None:
    """Bump version (patch, minor, or major)."""
    import re
    from pathlib import Path

    # Read current version from __init__.py
    init_path = Path("src/animaid/__init__.py")
    content = init_path.read_text()
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("Could not find version in __init__.py")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        print(f"Invalid part: {part}. Use 'major', 'minor', or 'patch'")
        sys.exit(1)

    new_version = f"{major}.{minor}.{patch}"

    # Update __init__.py
    new_content = re.sub(
        r'__version__\s*=\s*"[\d.]+"',
        f'__version__ = "{new_version}"',
        content,
    )
    init_path.write_text(new_content)

    # Update pyproject.toml
    pyproject_path = Path("pyproject.toml")
    pyproject_content = pyproject_path.read_text()
    new_pyproject = re.sub(
        r'^version\s*=\s*"[\d.]+"',
        f'version = "{new_version}"',
        pyproject_content,
        flags=re.MULTILINE,
    )
    pyproject_path.write_text(new_pyproject)

    # Update docs/conf.py
    docs_conf_path = Path("docs/conf.py")
    if docs_conf_path.exists():
        docs_content = docs_conf_path.read_text()
        new_docs = re.sub(
            r'^release\s*=\s*"[\d.]+"',
            f'release = "{new_version}"',
            docs_content,
            flags=re.MULTILINE,
        )
        docs_conf_path.write_text(new_docs)

    print(f"Version bumped to {new_version}")


# -------------------------------------------------------------------------
# Tutorial App Tasks
# -------------------------------------------------------------------------


@task
def tutorial_install(c: Context) -> None:
    """Install tutorial dependencies."""
    c.run("uv pip install -e '.[tutorial]'")


@task
def tutorial_start(c: Context, host: str = "127.0.0.1", port: int = 8200) -> None:
    """Start the tutorial web application."""
    import subprocess

    # Check if already running
    if TUTORIAL_PID_FILE.exists():
        pid = int(TUTORIAL_PID_FILE.read_text().strip())
        try:
            # Check if process is running
            import os

            os.kill(pid, 0)
            print(f"Tutorial server already running (PID {pid})")
            print(f"Visit http://{host}:{port}")
            return
        except OSError:
            # Process not running, remove stale PID file
            TUTORIAL_PID_FILE.unlink()

    # Start the server in background
    print(f"Starting tutorial server on http://{host}:{port}")
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "tutorial.app:app",
            "--host",
            host,
            "--port",
            str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Save PID
    TUTORIAL_PID_FILE.write_text(str(process.pid))
    print(f"Tutorial server started (PID {process.pid})")
    print(f"Visit http://{host}:{port}")


@task
def tutorial_stop(c: Context) -> None:
    """Stop the tutorial web application."""
    import os

    if not TUTORIAL_PID_FILE.exists():
        print("Tutorial server is not running")
        return

    pid = int(TUTORIAL_PID_FILE.read_text().strip())
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Tutorial server stopped (PID {pid})")
    except OSError as e:
        print(f"Could not stop server: {e}")
    finally:
        TUTORIAL_PID_FILE.unlink(missing_ok=True)


@task
def tutorial_restart(c: Context, host: str = "127.0.0.1", port: int = 8200) -> None:
    """Restart the tutorial web application."""
    tutorial_stop(c)
    import time

    time.sleep(1)
    tutorial_start(c, host=host, port=port)


@task
def tutorial_status(c: Context) -> None:
    """Check if the tutorial server is running."""
    import os

    if not TUTORIAL_PID_FILE.exists():
        print("Tutorial server is not running")
        return

    pid = int(TUTORIAL_PID_FILE.read_text().strip())
    try:
        os.kill(pid, 0)
        print(f"Tutorial server is running (PID {pid})")
    except OSError:
        print("Tutorial server is not running (stale PID file)")
        TUTORIAL_PID_FILE.unlink()


@task
def tutorial_run(c: Context, host: str = "127.0.0.1", port: int = 8200) -> None:
    """Run the tutorial web application in foreground (for development)."""
    print(f"Starting tutorial server on http://{host}:{port}")
    print("Press Ctrl+C to stop")
    c.run(
        f"uv run uvicorn tutorial.app:app --host {host} --port {port} --reload",
        pty=True,
    )


@task
def tutorial(c: Context, host: str = "127.0.0.1", port: int = 8200) -> None:
    """Start tutorial server and open in browser."""
    import subprocess
    import time
    import webbrowser

    url = f"http://{host}:{port}"

    # Check if already running
    if TUTORIAL_PID_FILE.exists():
        pid = int(TUTORIAL_PID_FILE.read_text().strip())
        try:
            import os

            os.kill(pid, 0)
            print(f"Tutorial server already running (PID {pid})")
            print(f"Opening {url} in browser...")
            webbrowser.open(url)
            return
        except OSError:
            TUTORIAL_PID_FILE.unlink()

    # Start the server in background
    print(f"Starting tutorial server on {url}")
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "tutorial.app:app",
            "--host",
            host,
            "--port",
            str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    # Save PID
    TUTORIAL_PID_FILE.write_text(str(process.pid))
    print(f"Tutorial server started (PID {process.pid})")

    # Wait a moment for the server to start
    time.sleep(1.5)

    # Open in browser
    print(f"Opening {url} in browser...")
    webbrowser.open(url)


# -------------------------------------------------------------------------
# Demo Tasks
# -------------------------------------------------------------------------

AVAILABLE_DEMOS = [
    "countdown_timer",
    "live_list",
    "score_tracker",
    "sorting_visualizer",
    "dashboard",
    "typewriter",
    "todo_app",
    "data_pipeline",
]


@task
def demo(c: Context, name: str = "") -> None:
    """Run a demo program by name.

    Available demos:
    - countdown_timer: Real-time countdown with color transitions
    - live_list: Reactive shopping cart list
    - score_tracker: Game score tracking with dict updates
    - sorting_visualizer: Bubble sort algorithm visualization
    - dashboard: Multi-type dashboard with all HTML types
    - typewriter: Typewriter effect with styling animation
    - todo_app: Interactive todo list mini app
    - data_pipeline: ETL pipeline progress tracking

    Example: invoke demo countdown_timer
    """
    if not name:
        print("Available demos:")
        for demo_name in AVAILABLE_DEMOS:
            print(f"  - {demo_name}")
        print()
        print("Run a demo with: invoke demo <name>")
        print("Example: invoke demo countdown_timer")
        return

    if name not in AVAILABLE_DEMOS:
        print(f"Unknown demo: {name}")
        print()
        print("Available demos:")
        for demo_name in AVAILABLE_DEMOS:
            print(f"  - {demo_name}")
        sys.exit(1)

    c.run(f"uv run python demos/{name}.py", pty=True)


@task
def demo_list(c: Context) -> None:
    """List all available demo programs."""
    print("Available AnimAID demos:")
    print()
    descriptions = {
        "countdown_timer": "Real-time countdown with color transitions",
        "live_list": "Reactive shopping cart list",
        "score_tracker": "Game score tracking with dict updates",
        "sorting_visualizer": "Bubble sort algorithm visualization",
        "dashboard": "Multi-type dashboard with all HTML types",
        "typewriter": "Typewriter effect with styling animation",
        "todo_app": "Interactive todo list mini app",
        "data_pipeline": "ETL pipeline progress tracking",
    }
    for demo_name in AVAILABLE_DEMOS:
        desc = descriptions.get(demo_name, "")
        print(f"  {demo_name:20} - {desc}")
    print()
    print("Run a demo with: invoke demo <name>")
