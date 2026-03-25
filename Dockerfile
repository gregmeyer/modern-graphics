FROM mcr.microsoft.com/playwright/python:v1.58.0-noble

WORKDIR /app

COPY pyproject.toml README.md ./
COPY modern_graphics modern_graphics/

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["modern-graphics"]
CMD ["--help"]
