clean-code:
	isort .
	black .
	flake8
	flake8 --radon-max-cc 10
	mypy .
