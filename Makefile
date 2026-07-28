.PHONY: run install clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

run:
	$(PYTHON) bot.py serve

install:
	$(PYTHON) -m pip install -U pip
	$(PIP) install -r requirements.txt
	$(PYTHON) bot.py init DCACCOUNT:https://nine.testrun.org/new
	$(PYTHON) bot.py config displayname "Gallery Bot"
	$(PYTHON) bot.py link

clean:
	rm -rf gallery-dl/*
