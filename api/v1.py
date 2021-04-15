from frictionless import Package, Layout, transform, steps
from datetime import datetime, date
import json
from decimal import Decimal

from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)

data = Package("datapackage.json")
resources = data.resource_names


@app.route('/v1/<string:dataset>')
@app.route('/v1', defaults={'dataset': ''})
@cross_origin()
def api(dataset):
    try:
        per_page = int(request.args.get('per_page', 1000))
    except:
        per_page = 1000

    try:
        page = (int(request.args.get('page', 1))-1)*per_page
    except:
        page = 1

    if dataset == '':
        dataset = resources[-1]

    if dataset not in resources:
        return Response(
            json.dumps({
                "error": "Requested dataset %s does not exist." % (dataset),
                "dataset": dataset,
                "time": datetime.today().strftime('%Y-%m-%dT%H:%M:%S'),
                "last_update": None,
                "last_published": None,
                "applied_filter": None,
                "per_page": per_page,
                "page": page,
                "data": None
            }),
            mimetype='application/json',
            status=404)
    else:
        df = data.get_resource(dataset)
        print(df)
        last_update = df['last_update']
        last_published = df['last_published']
        dpf = []
        filter_strings = []
        for fld in df.schema.fields:
            fn = fld['name']
            try:
                q = request.args.get(fn)
            except:
                q = None

            if q is not None:
                q = q.strip()
                filter_strings.append("%s == '%s'" % (fn, q))
                dpf.append({fn: q})

        transform_steps = []
        if len(filter_strings) > 0:
            filter_expression = " and ".join(filter_strings)
            transform_steps.append(steps.row_filter(formula=filter_expression))

        transform_steps.append(steps.row_slice(
            start=page, stop=(page+per_page)))

        df = transform(df,
                       steps=transform_steps)

        rows = df.read_rows()
        print(rows)

        return Response(
            json.dumps({
                "dataset": dataset,
                "time": datetime.today().strftime('%Y-%m-%dT%H:%M:%S'),
                "last_update": last_update,
                "last_published": last_published,
                "applied_filter": dpf,
                "per_page": per_page,
                "page": page,
                "data": rows
            }, cls=DecimalEncoder),
            mimetype='application/json',
            headers={
                "Cache-Control": "s-maxage=300, stale-while-revalidate=59"
            },
            status=200)


class DecimalEncoder (json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
