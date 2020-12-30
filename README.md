# RKI Vaccination Monitoring

Project to archive the [state level vaccination data](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html) published by the Robert-Koch-Institut daily.

🏗️ A work in progress.

Experimental visualization: [Observable Notebook](https://observablehq.com/@n0rdlicht/vaccination-tracker-germany)

## Technical setup

1. Daily [GitHub Action](.github/workflows/main.yml) running a Frictionless Data Package Pipeline as defined in [pipeline-spec.yaml](pipeline-spec.yaml). Currently run manually, to be automated based on changes to [RKI website](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html)
1. Resulting in a [combined CSV](data/de-vaccinations.csv) and [current day CSV](data/de-vaccinations-current.csv)
1. D3.js visualization of data