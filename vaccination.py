# -*- coding: utf-8 -*-

from pprint import pprint
from frictionless import Package, Resource, Layout, Schema, extract, describe_schema, validate, transform, steps
from frictionless.plugins.excel import ExcelDialect

import petl
from datetime import datetime, timedelta
from dateutil import parser

import requests


r = requests.get(
    'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile')
publishdate = parser.parse(r.headers["Last-Modified"])
datadate = publishdate - timedelta(1)

impfquote = Resource(
    'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile', dialect=ExcelDialect(sheet=2), layout=Layout(header_rows=[1, 2, 3, 4], header_join='_', limit_rows=18), schema=Schema("data/de-vaccinations-raw-quote.schema.yaml"), )
impfquote.write('data/de-vaccinations-raw-quote.csv')

impfquote = transform(
    impfquote,
    steps=[
        # Normalize
        steps.table_normalize(),

        # Simplify naming

        # Add metadata
        steps.field_add(name=f'geo', type='string',
                        function=lambda x: 'Germany' if x['Bundesland'] == 'Gesamt' else x['Bundesland']),

        # 1. sums
        steps.field_add(name=f'sum', type='integer',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Gesamtzahl bisher verabreichter Impfungen']),
        steps.field_add(name=f'sum_initial', type='integer',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Gesamtzahl einmalig geimpft']),
        steps.field_add(name=f'sum_booster', type='integer',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Gesamtzahl vollständig geimpft']),
        steps.field_add(name=f'quote_initial', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_Gesamt']),
        steps.field_add(name=f'quote_initial_age_60+', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_60+ Jahre']),
        steps.field_add(name=f'quote_initial_age_<60', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_<60 Jahre']),
        steps.field_add(name=f'quote_booster', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_Gesamt']),
        steps.field_add(name=f'quote_booster_age_60+', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_60+ Jahre']),
        steps.field_add(name=f'quote_booster_age_<60', type='number',
                        function=lambda x: x['Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_<60 Jahre']),

        # 2. centers
        steps.field_add(name=f'sum_initial_age_60+_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_eine Impfung_60+ Jahre']),
        steps.field_add(name=f'sum_initial_age_<60_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_eine Impfung_<60 Jahre']),
        steps.field_add(name=f'sum_booster_age_60+_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_vollständig geimpft_60+Jahre']),
        steps.field_add(name=f'sum_booster_age_<60_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_vollständig geimpft_<60 Jahre']),

        # 3. doctors
        steps.field_add(name=f'sum_initial_age_60+_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_60+ Jahre']),
        steps.field_add(name=f'sum_initial_age_<60_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_<60 Jahre']),
        steps.field_add(name=f'sum_booster_age_60+_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_60+Jahre']),
        steps.field_add(name=f'sum_booster_age_<60_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_<60 Jahre']),

        # Cleanup
        steps.field_remove(names=[
                           "RS", "Bundesland", "Insgesamt über alle Impfstellen_Gesamtzahl bisher verabreichter Impfungen", "Insgesamt über alle Impfstellen_Gesamtzahl einmalig geimpft", "Insgesamt über alle Impfstellen_Gesamtzahl vollständig geimpft", "Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_Gesamt", "Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_60+ Jahre", "Insgesamt über alle Impfstellen_Impfquote mit einer Impfung_<60 Jahre", "Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_Gesamt", "Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_60+ Jahre", "Insgesamt über alle Impfstellen_Impfquote vollständig geimpft_<60 Jahre", "Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_eine Impfung_60+ Jahre", "Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_eine Impfung_<60 Jahre", "Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_vollständig geimpft_60+Jahre", "Impfungen in Impfzentren, Mobilen Teams und Krankenhäusern_vollständig geimpft_<60 Jahre", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_60+ Jahre", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_<60 Jahre", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_60+Jahre", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_<60 Jahre"]),

        # Pivot
        steps.table_melt(field_name="geo", to_field_names=["key", "value"]),

        steps.field_add(name=f'iso-cc', type='string',
                        formula='"DE"'),
        steps.field_add(name=f'geotype', type='string',
                        function=lambda x: 'nation' if x['geo'] == 'Germany' else 'state'),
        steps.field_move(name="iso-cc", position=2),
        steps.field_move(name="geotype", position=3),
    ],
)

impfquote.schema.primary_key = ["geo", "iso-cc", "key"]

impfstoff = Resource(
    'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile', dialect=ExcelDialect(sheet=3, fill_merged_cells=True), layout=Layout(header_rows=[1, 2, 3, 4], header_join='_', limit_rows=18), schema=Schema("data/de-vaccinations-raw-totals.schema.yaml"))
impfstoff = impfstoff.write('data/de-vaccinations-raw-totals.csv')

impfstoff = transform(
    impfstoff,
    steps=[
        # Normalize
        steps.table_normalize(),

        # Simplify naming

        # Add metadata
        steps.field_add(name=f'geo', type='string',
                        function=lambda x: 'Germany' if x['Bundesland'] == 'Gesamt' else x['Bundesland']),

        # 1. Centers
        steps.field_add(name=f'sum_initial_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_Gesamt']),
        steps.field_add(name=f'sum_initial_biontech_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_BioNTech']),
        steps.field_add(name=f'sum_initial_moderna_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_Moderna']),
        steps.field_add(name=f'sum_initial_astrazeneca_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_AstraZeneca']),
        steps.field_add(name=f'delta_vortag_initial_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Differenz zum Vortag']),

        steps.field_add(name=f'sum_booster_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_Gesamt']),
        steps.field_add(name=f'sum_booster_biontech_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_BioNTech']),
        steps.field_add(name=f'sum_booster_moderna_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_Moderna']),
        steps.field_add(name=f'sum_booster_astrazeneca_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_AstraZeneca']),
        steps.field_add(name=f'delta_vortag_booster_centers', type='number',
                        function=lambda x: x['Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Differenz zum Vortag']),

        # 1. Doctors
        steps.field_add(name=f'sum_initial_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_Gesamt']),
        steps.field_add(name=f'sum_initial_biontech_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_BioNTech']),
        steps.field_add(name=f'sum_initial_moderna_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_Moderna']),
        steps.field_add(name=f'sum_initial_astrazeneca_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_AstraZeneca']),
        steps.field_add(name=f'delta_vortag_initial_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Differenz zum Vortag']),

        steps.field_add(name=f'sum_booster_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_Gesamt']),
        steps.field_add(name=f'sum_booster_biontech_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_BioNTech']),
        steps.field_add(name=f'sum_booster_moderna_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_Moderna']),
        steps.field_add(name=f'sum_booster_astrazeneca_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_AstraZeneca']),
        steps.field_add(name=f'delta_vortag_booster_doctors', type='number',
                        function=lambda x: x['Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Differenz zum Vortag']),

        steps.field_add(
            name="delta_vortag_initial", function=lambda x: sum(filter(None, [x['delta_vortag_initial_centers'], x['delta_vortag_initial_doctors']]))),
        steps.field_add(
            name="delta_vortag_booster", function=lambda x: sum(filter(None, [x['delta_vortag_booster_centers'], x['delta_vortag_booster_doctors']]))),
        steps.field_add(
            name="delta_vortag", function=lambda x: sum(filter(None, [x['delta_vortag_initial'], x['delta_vortag_booster']]))),
        steps.field_add(
            name="delta_vortag_centers", function=lambda x: sum(filter(None, [x['delta_vortag_initial_centers'], x['delta_vortag_booster_centers']]))),
        steps.field_add(
            name="delta_vortag_doctors", function=lambda x: sum(filter(None, [x['delta_vortag_initial_doctors'], x['delta_vortag_booster_doctors']]))),

        steps.field_add(
            name="sum_initial_biontech", function=lambda x: sum(filter(None, [x['sum_initial_biontech_centers'], x['sum_initial_biontech_doctors']]))),
        steps.field_add(
            name="sum_booster_biontech", function=lambda x: sum(filter(None, [x['sum_booster_biontech_centers'], x['sum_booster_biontech_doctors']]))),
        steps.field_add(
            name="sum_biontech", function=lambda x: sum(filter(None, [x['sum_initial_biontech'], x['sum_booster_biontech']]))),

        steps.field_add(
            name="sum_initial_moderna", function=lambda x: sum(filter(None, [x['sum_initial_moderna_centers'], x['sum_initial_moderna_doctors']]))),
        steps.field_add(
            name="sum_booster_moderna", function=lambda x: sum(filter(None, [x['sum_booster_moderna_centers'], x['sum_booster_moderna_doctors']]))),
        steps.field_add(
            name="sum_moderna", function=lambda x: sum(filter(None, [x['sum_initial_moderna'], x['sum_booster_moderna']]))),

        steps.field_add(
            name="sum_initial_astrazeneca", function=lambda x: sum(filter(None, [x['sum_initial_astrazeneca_centers'], x['sum_initial_astrazeneca_doctors']]))),
        steps.field_add(
            name="sum_booster_astrazeneca", function=lambda x: sum(filter(None, [x['sum_booster_astrazeneca_centers'], x['sum_booster_astrazeneca_doctors']]))),
        steps.field_add(
            name="sum_astrazeneca", function=lambda x: sum(filter(None, [x['sum_initial_astrazeneca'], x['sum_booster_astrazeneca']]))),

        # Cleanup
        steps.field_remove(names=[
                           "RS", "Bundesland", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_Gesamt", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_BioNTech", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_Moderna", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Impfungen kumulativ_AstraZeneca", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_eine Impfung_Differenz zum Vortag", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_Gesamt", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_BioNTech", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_Moderna", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Impfungen kumulativ_AstraZeneca", "Impfungen in Impfzentren, Mobilen Teams, Krankenhäusern_vollständig geimpft_Differenz zum Vortag",

                           "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_Gesamt", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_BioNTech", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_Moderna", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Impfungen kumulativ_AstraZeneca", "Impfungen der niedergelassenen Ärzteschaft_eine Impfung_Differenz zum Vortag", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_Gesamt", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_BioNTech", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_Moderna", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Impfungen kumulativ_AstraZeneca", "Impfungen der niedergelassenen Ärzteschaft_vollständig geimpft_Differenz zum Vortag"]),

        # Pivot
        steps.table_melt(field_name="geo", to_field_names=["key", "value"]),

        steps.field_add(name=f'iso-cc', type='string',
                        formula='"DE"'),
        steps.field_add(name=f'geotype', type='string',
                        function=lambda x: 'nation' if x['geo'] == 'Germany' else 'state'),
        steps.field_move(name="iso-cc", position=2),
        steps.field_move(name="geotype", position=3),
    ],
)

impfstoff.schema.primary_key = ["geo", "iso-cc", "key"]
# impfstoff.write('data/de-vaccinations-raw-totals-normalized.csv')

petl.tocsv(petl.transform.basics.cat(
    impfquote.to_petl(), impfstoff.to_petl()), 'data/de-vaccinations-current.csv')

population = Resource('data/de-population-current.csv')
population.infer()

quote = Resource('data/de-vaccinations-current.csv')
quote = transform(
    quote,
    steps=[
        steps.row_filter(formula="key == 'quote_booster'"),
        steps.field_add(name="quote", formula="value"),
        steps.field_remove(names=["iso-cc", "geotype", "key", "value"]),
    ]
)

current = Resource('data/de-vaccinations-current.csv')
current.infer()

current = transform(
    current,
    steps=[
        steps.table_normalize(),
        steps.row_sort(field_names=["geo"]),
        steps.table_join(resource=population, field_name="geo"),
        steps.table_join(resource=quote, field_name="geo")
    ]
)

current.write('data/de-vaccinations-current.csv')

today = datetime.now()

log = transform(
    current,
    steps=[
        steps.field_add(
            name="date", formula=f'"{datadate.date().isoformat()}"')
    ]
)

last_entry = transform(
    Resource("data/de-vaccinations.csv"),
    steps=[
        steps.row_slice(tail=1),
    ]
).read_rows()

if len(last_entry) > 0 and "date" in last_entry[0].keys() and last_entry[0]["date"] < datadate.date():
    print(f"New entries for {datadate.date()}")
    petl.appendcsv(log.to_petl(), 'data/de-vaccinations.csv')
else:
    print(f"No new entries")

# Create final Data Package

pkg = Package()
pkg.contributors = [{
    "path": "https://github.com/n0rdlicht",
    "role": "maintainer",
    "title": "Thorben Westerhuys"
}]
pkg.homepage = "https://github.com/n0rdlicht/rki-vaccination-scraper"
pkg.keywords = ["COVID-19",
                "RKI",
                "Germany",
                "Vaccination"]
pkg["license"] = "ODC-PDDL-1.0"
pkg.licenses = [{"name": "ODC-PDDL-1.0",
                 "path": "http://opendatacommons.org/licenses/pddl/", "title": "Open Data Commons Public Domain Dedication and License v1.0"}]
pkg.name = "covid19-vaccinations-germany"

pkg.resources = [
    Resource("data/de-population-current.csv", hashing="sha256"),
    Resource("data/de-vaccinations-raw-indikation.csv", hashing="sha256"),
    Resource("data/de-vaccinations-raw-quote.csv", hashing="sha256"),
    Resource("data/de-vaccinations-raw-totals.csv", hashing="sha256"),
    Resource("data/de-vaccinations-current.csv", hashing="sha256"),
    Resource("data/de-vaccinations.csv", hashing="sha256"),
]

for r in pkg.resources:
    r.infer(stats=True)
    r.expand()

pkg.get_resource("de-vaccinations").schema.get_field("value").type = "number"

pkg.get_resource(
    "de-vaccinations-raw-indikation")["last_published"] = publishdate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-raw-indikation")["last_update"] = datadate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-raw-quote")["last_published"] = publishdate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-raw-quote")["last_update"] = datadate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-raw-totals")["last_published"] = publishdate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-raw-totals")["last_update"] = datadate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-current")["last_published"] = publishdate.date().isoformat()
pkg.get_resource(
    "de-vaccinations-current")["last_update"] = datadate.date().isoformat()
pkg.get_resource(
    "de-vaccinations")["last_published"] = publishdate.date().isoformat()
pkg.get_resource(
    "de-vaccinations")["last_update"] = datadate.date().isoformat()

pkg.sources = [{
    "path": "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquoten-Tab.html",
    "title": "RKI Digitales Impfquotenmonitoring"
}]
pkg.title = "COVID-19 Vaccination Rates in Germany"

pkg.to_json('datapackage.json')

# Validate

print("Validating package")

report = validate(pkg)

print(report.errors)
assert len(report.errors) == 0
