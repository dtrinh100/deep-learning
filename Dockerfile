FROM astral-sh/uv:latest AS uv_bin
FROM python:3.15-slim

COPY --from=uv_bin /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev
COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]