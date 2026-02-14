install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install dist\project1_zamanov_renat_m25_555-0.1.0-py3-none-any.whl