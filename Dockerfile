FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

LABEL maintainer="MathieuAudibert"
LABEL contact="mathieu.audibert@edu.devinci.fr"

RUN apt-get update && apt-get install -y --no-install-recommends \
    passwd \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r ml-flow-group && useradd -r -g ml-flow-group -m -d /home/ml-flow-user ml-flow-user

WORKDIR /app 
COPY pyproject.toml ./

RUN uv pip install --no-cache-dir --system -e .

COPY . .

RUN chown -R ml-flow-user /app
USER ml-flow-user

RUN localstack start
CMD ["fastapi", "run", "src/main.py"]