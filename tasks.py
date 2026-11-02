"""Local automation for woo-als-een-pro. Run `inv --list`."""

from pathlib import Path

from invoke import Context, task

ROOT = Path(__file__).resolve().parent
PORT = 8000


@task(help={"port": f"Port; default {PORT}"})
def serve(c: Context, port: int = PORT) -> None:
    """Serve the site from the working tree at http://localhost:<port>."""
    # app.py reads the markdown on each request: content edits show without a restart.
    with c.cd(str(ROOT)):
        c.run(f"site/app.py --port {port}", pty=True)


@task
def check(c: Context) -> None:
    """Check links and anchors in docs/, templates/ and uitspraken/."""
    with c.cd(str(ROOT)):
        c.run("tools/check_links.py")


@task
def test(c: Context) -> None:
    """Run the tool tests."""
    with c.cd(str(ROOT)):
        c.run("uv run --with pytest pytest -q tools/")
