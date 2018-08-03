.PHONY: build_doc install install-dev

build_doc:
	sphinx-build -E -b html docs docs/_build

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -v tests