.PHONY: run install clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

run:
	$(PYTHON) bot.py serve

install:
	$(PYTHON) -m pip install -U pip
	$(PIP) install -r requirements.txt

clean:
	rm -rf gallery-dl/*
