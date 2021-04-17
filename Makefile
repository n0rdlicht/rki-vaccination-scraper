all: init update

update:
	poetry run python vaccination.py

init:
	poetry install