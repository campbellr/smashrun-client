
.PHONY: clean

clean:
	git clean -fdX

test:
	tox

build:
	python setup.py sdist

release:
	python setup.py register sdist bdist_wheel upload
