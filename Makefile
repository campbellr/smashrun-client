
.PHONY: clean

clean:
	git clean -X

test:
	tox

build:
	python setup.py sdist
