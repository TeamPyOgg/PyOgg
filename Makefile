all: clean wheel delocate

wheel:
	python setup.py build bdist_wheel

delocate:
	delocate-wheel -v dist/*.whl	

clean:
	rm -rf dist
	rm -rf build
