all: update

update:
	dpp run ./de-vaccinations

validate:
	goodtables validate datapackage.json