.PHONY: lint
lint:
	pep8 ircddbrequest/ ./*.py
	pylint --rcfile=.pylintrc *.py
