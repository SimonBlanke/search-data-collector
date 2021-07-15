dist:
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install:
	pip install .

develop:
	pip install -e .

reinstall:
	pip uninstall -y hyperactive_data_storage
	rm -fr build dist hyperactive_data_storage.egg-info
	python setup.py bdist_wheel
	pip install dist/*

test:
	python -m pytest -x -p no:warnings -rfEX tests/ \