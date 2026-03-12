from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("jtl-syllabus")
except PackageNotFoundError:
    __version__ = "unknown"
