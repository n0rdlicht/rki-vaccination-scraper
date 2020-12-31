all: fetch update

fetch:
	dpp run ./vaccination

update:
	dpp run ./vaccination-archive
	#rm data/de-vaccinations-current-dated.csv

validate:
	goodtables validate datapackage.json