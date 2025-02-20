
.PHONY: setup build publish compile


VERSION := $(shell grep '^version =' pyproject.toml | sed 's/version = "\(.*\)"/\1/')


ver:
	@echo $(VERSION)

compile:
	uv pip compile pyproject.toml -o requirements.txt

push:
	git commit --allow-empty -a -m "Release version $(VERSION)"
	git push
	git tag v$(VERSION) 
	git push --tags

publish: build compile push
	uv publish --token $$UV_PUBLISH_TOKEN

build:
	uv build

setup:
	uv venv --link-mode symlink

