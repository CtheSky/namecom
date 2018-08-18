.PHONY: build_doc install install-dev test publish

build_doc:
	sphinx-build -E -b html docs docs/_build

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest -vx --cov=namecom tests

publish:
	bumpversion ${version}
	git push && git push --tags
	python setup.py sdist bdist_wheel
	twine upload dist/*