# JTL Syllabus build targets

version := `grep '^version =' pyproject.toml | sed 's/version = "\(.*\)"/\1/'`

# Show the current version
ver:
    @echo {{version}}

# Compile requirements.txt from pyproject.toml
compile:
    uv pip compile pyproject.toml -o requirements.txt

# Build the package
build:
    uv build

# Set up the virtual environment
setup:
    uv venv --link-mode symlink

# Commit, tag, and push the current version
push:
    git commit --allow-empty -a -m "Release version {{version}}"
    git push
    git tag v{{version}}
    git push --tags

# Build, compile deps, push, and publish to PyPI
publish: build compile push
    uv publish --token $UV_PUBLISH_TOKEN
