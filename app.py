# coding: utf-8

import os.path
import json

import settings
from flask import Flask, render_template, Markup

app = Flask(__name__, template_folder="templates")

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = settings.API_KEY


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)


def read_data(data_filename):
    complete_path = os.path.join(root_dir(), settings.DATA_DIR, data_filename)

    json_data = get_file(complete_path)

    data = json.loads(json_data)

    return data


@app.route('/')
def fullmap():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5
    )
    return render_template('fullmap.html', **map_params)

@app.route('/drawing')
def drawing():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5
    )
    return render_template('drawing.html', **map_params)

@app.route('/reader')
def reader():
    data = read_data('test-data.json')

    map_params = dict(
        identifier="reader",
        varname="reader",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5,
        data=data
    )
    return render_template('reader.html', **map_params)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
