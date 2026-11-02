# Build: resolve the script deps into a venv. Same Alpine base as runtime, so musl wheels match.
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS build
WORKDIR /app
COPY site/app.py site/app.py
RUN uv export --script site/app.py --no-hashes --no-header > requirements.txt \
    && uv venv /venv \
    && uv pip install --no-cache --python /venv/bin/python -r requirements.txt

# Serve: no uv, no build tools.
FROM python:3.12-alpine
COPY --from=build /venv /venv
WORKDIR /app
COPY . .
USER nobody
EXPOSE 8000
CMD ["/venv/bin/python", "site/app.py", "--host", "0.0.0.0", "--port", "8000"]
