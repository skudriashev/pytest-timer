generate-dist:
	python setup.py sdist bdist_wheel

upload-dist:
	twine upload dist/*

check-dist:
	twine check dist/*

clean-dist:
	rm dist/*
