import importlib.metadata

try:
    __version__ = importlib.metadata.version("core")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
