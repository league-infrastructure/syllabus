from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
import os
import tomllib

__version__ = "unknown"
try:
    # First attempt: Try to get version from installed package metadata
    dist_name = "jtl-syllabus"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    # Second attempt: Try to read from pyproject.toml directly
    try:
        # Find the project root by walking up from this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = current_dir
        while not os.path.exists(os.path.join(project_root, "pyproject.toml")):
            parent_dir = os.path.dirname(project_root)
            if parent_dir == project_root:  # We've reached the filesystem root
                break
            project_root = parent_dir
        
        # Read pyproject.toml if found
        pyproject_path = os.path.join(project_root, "pyproject.toml")
        if os.path.exists(pyproject_path):
            with open(pyproject_path, "rb") as f:
                project_data = tomllib.load(f)
                __version__ = project_data.get("project", {}).get("version", "unknown")
    except (OSError, ValueError, KeyError) as e:
        # More specific exceptions: file access issues, TOML parsing errors, or missing keys
        pass
finally:
    del version, PackageNotFoundError