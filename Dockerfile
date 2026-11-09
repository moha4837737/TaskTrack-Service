# ---- Stage 1: build (install dependencies) ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: runtime (small final image) ----
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    DB_PATH=/data/tasks.db
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ .
RUN useradd --create-home appuser && mkdir /data && chown appuser /data
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
