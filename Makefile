all: build 

# TODO: Add `unittests` & `coverage` report targets
# TODO: Build using skipper - so the package could be build using CleanBuild

build: clean
	python setup.py sdist

clean:
	# Clean any generated files
	rm -rf build dist zadarapy.egg-info .coverage .cache reports

install: build
	sudo pip install -U .

package: build
	artifactor --artifacts-file artifacts.yaml submit
	packager pack artifacts.yaml --auto-push

pylint:
	mkdir -p reports/
	PYLINTHOME=reports/ pylint -r n zadarapy upgrade

flake8:
	flake8 upgrade_tools --max-line-length=145


.PHONY: build flake8 pylint install clean
