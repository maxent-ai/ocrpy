install:
	echo "Install dependencies and build ocrpy."
	pip install --upgrade pip && pip install .

format:
	echo "Format the code."
	black ocrpy/

lint:
	echo "Lint the code."
	flake8 ocrpy/ 

build-package:
	echo "Build the package."
	hatch build

build-docs:
	echo "Build the documentation."
	cd docs && make clean html && cd ..

publish-package:
	echo "Publish the package."
	hatch publish --user=${PYPI_USERNAME} --auth=${PYPI_PASSWORD}

enforce-quality: format lint
