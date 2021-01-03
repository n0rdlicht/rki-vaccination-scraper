from pandas_datapackage_reader import read_datapackage
from datetime import datetime
import json

from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app)

data = read_datapackage("")
resources = list(data.keys())

def get_paginated_json(df, per_page, page):
    return df[page:page+per_page].to_json(orient='records',date_format='iso')

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
        df = data.copy()[dataset]
        last_update = df._metadata['last_update']
        last_published = df._metadata['last_published']
        dpf = []
        for fld in df._metadata['schema']['fields']:
            fn = fld['name']
            try:
                q = request.args.get(fn)
            except:
                q = None
            if q is not None:
                try:
                    q = q.strip()
                    df = df.loc[df[fn] == q]
                    dpf.append({fn:q})
                except:
                    pass

        return Response(
            json.dumps({
                "dataset": dataset,
                "time": datetime.today().strftime('%Y-%m-%dT%H:%M:%S'),
                "last_update": last_update,
                "last_published": last_published,
                "applied_filter": dpf, 
                "per_page": per_page, 
                "page": page,
                "data": json.loads(get_paginated_json(df,per_page,page))
                }),
            mimetype='application/json',
            status=200)