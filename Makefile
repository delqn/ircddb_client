.DEFAULT_GOAL := all

.PHONY: all
all: install-prepush lint

.PHONY: lint
lint:
	pep8 ircddbrequest/ ./*.py
	pylint --rcfile=.pylintrc *.py

.PHONY: install-prepush
install-prepush:
	@-if [ -d .git ] && [ ! -h .git/hooks/pre-push ] ; then \
		ln -s ../../prepush .git/hooks/pre-push; \
	fi
