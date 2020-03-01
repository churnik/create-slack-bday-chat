import os


SERVICE_PORT = os.environ.get("SERVICE_PORT", 3000)
WORKERS = os.environ.get("GUNICORN_WORKERS", 3)
THREADS = os.environ.get("GUNICORN_THREADS", 3)

bind = f"0.0.0.0:{SERVICE_PORT}"

chdir = "/code/"

workers = WORKERS
worker_class = "gthread"
threads = THREADS

# This flag makes gunicorn import package only once
# so that it could fail fast if something is wrong with imported package.
preload_app = True
