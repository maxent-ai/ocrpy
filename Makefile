install:
	echo "Install dependencies and build ocrpy."
	pip install --upgrade pip && pip install .

format:
	black ocrpy/

lint:
	flake8 ocrpy/ 

build-package:
	hatch build

build-docs:
	cd docs && make clean html && cd ..

publish-package:
	hatch publish -user=${PYPI_USERNAME} --auth=${PYPI_PASSWORD}

enforce-quality: format lint
