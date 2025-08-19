FROM python:3.13.6-slim AS base

# Add metadata
LABEL maintainer="Ilia Boiarintsev <theilyaboyarintsev@gmail.com>"
LABEL description="Organizations Management System - Test Assignment Backend API"
LABEL version="0.1.0"

FROM base AS app_builder
COPY ./poetry.lock /src/poetry.lock
COPY ./pyproject.toml /src/pyproject.toml
WORKDIR /src
RUN pip install --no-cache-dir -U pip==24.2 poetry==1.8.3 \
    && python -m venv /env \
    && . /env/bin/activate \
    && poetry install --only main --no-root

FROM app_builder AS dev
RUN . /env/bin/activate \
    && poetry install
ENV PATH="/env/bin:${PATH}"

FROM base AS app
ARG VERSION
ENV VERSION=${VERSION:-0.1.0}
COPY --from=app_builder /env /env
COPY . /src
ENV PYTHONPATH=/src
ENV PATH="/env/bin:${PATH}"
WORKDIR /src
CMD ["uvicorn", "app.asgi:app", "--host", "0.0.0.0", "--proxy-headers", "--forwarded-allow-ips", "*"]
