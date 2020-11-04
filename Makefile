#! /usr/bin/make -f
APP			?= ./*.py

help:  		## This help dialog.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

bashtests:  	## Run bash scripts tests
	bash ./.devbin/shtests.sh

pyttests:  	## Run applications python tests
	chmod -R 755 ./*
	python3 -m pytest pytests/
	bash ./.devbin/pylint.sh

commit:  	## Deploy, test, commit changes to git and push on github
	bash ./.devbin/bigcommit.sh

deploy:		## Copy script to ~/bin
	cp ./stext.py ~/bin && chmod 755 ~/bin/stext.py
