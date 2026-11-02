"""Local automation for woo-als-een-pro. Run `inv --list`."""

import io
import shlex
from pathlib import Path

from invoke import Context, task
from invoke.exceptions import Exit

ROOT = Path(__file__).resolve().parent
PORT = 8000
IMAGE = "woo-als-een-pro"


def _env() -> dict[str, str]:
    """Read `export KEY=VALUE` lines from .env."""
    path = ROOT / ".env"
    if not path.is_file():
        raise Exit(".env not found: set DOCKERHUB_USER and DOCKERHUB_TOKEN")
    pairs = (line.removeprefix("export ").split("=", 1) for line in path.read_text().splitlines() if "=" in line)
    return {k.strip(): v.strip().strip("'\"") for k, v in pairs}


@task(help={"port": f"Port; default {PORT}"})
def serve(c: Context, port: int = PORT) -> None:
    """Serve the site at http://localhost:<port>; pages refresh on content changes."""
    with c.cd(str(ROOT)):
        c.run(f"site/app.py --port {port} --reload", pty=True)


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


@task(help={"port": f"Port; default {PORT}"})
def docker(c: Context, port: int = PORT) -> None:
    """Build the image and run it as in production at http://localhost:<port>."""
    with c.cd(str(ROOT)):
        c.run(f"docker build -t {IMAGE}:local .", pty=True)
        c.run(f"docker run --rm --read-only -p {port}:8000 {IMAGE}:local", pty=True)


@task(pre=[check])
def deploy(c: Context) -> None:
    """Build the site image and push it to Docker Hub as :latest and :<git sha>."""
    env = _env()
    user, token = env["DOCKERHUB_USER"], env["DOCKERHUB_TOKEN"]
    with c.cd(str(ROOT)):
        if c.run("git status --porcelain", hide=True).stdout.strip():
            raise Exit("working tree not clean: commit first, the tag is the git sha")
        sha = c.run("git rev-parse --short HEAD", hide=True).stdout.strip()
        repo = f"{user}/{IMAGE}"
        c.run(f"docker login -u {shlex.quote(user)} --password-stdin", in_stream=io.StringIO(token))
        c.run(f"docker build -t {repo}:latest -t {repo}:{sha} .", pty=True)
        c.run(f"docker push {repo}:{sha}", pty=True)
        c.run(f"docker push {repo}:latest", pty=True)
