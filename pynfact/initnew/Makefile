# Makefile :: Py'nFact
#
# Modify this file to your convenience

SHELL = /bin/bash

BIN = /usr/bin/env python3 ./pynfact/cli.py
PORT = 4000 # test port when serving on local machine.

.PHONY: build serve test


all:
	make build
#	make upload

build:
	${BIN} build

serve:
	${BIN} serve ${PORT}

test:
	make build
	make serve

#upload:
#	rsync -e 'ssh' -a _build/ http://your.site.com/
#	@echo "Done."

