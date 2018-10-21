# coding: utf-8

import os.path
import json

import settings
from flask import Flask, render_template, Markup, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(settings.UPLOAD_FOLDER)
DATA_FOLDER = os.path.join(settings.DATA_FOLDER)
READER_DATA_FILE = os.path.join(settings.READER_DATA_FILE)

ALLOWED_EXTENSIONS = set(['txt', 'json'])


app = Flask(__name__, template_folder="templates")
app.secret_key = settings.SECRET_KEY

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER
app.config['READER_DATA_FILE'] = READER_DATA_FILE

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = settings.API_KEY

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    complete_path = os.path.join(root_dir(), app.config['DATA_FOLDER'], data_filename)

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

@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        if 'fname' not in request.form and 'data-out-json' not in request.form:
            flash("No file to save")
            return redirect(url_for('drawing'))

        data = json.loads(request.form['data-out-json'])

        fpath = os.path.join(app.config['DATA_FOLDER'], secure_filename(request.form['fname']))

        with open(fpath, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        flash("File {} saved".format(fpath))

    return redirect(url_for('drawing'))

@app.route('/drawing', methods=['GET', 'POST'])
def drawing():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5,
        fname=None,
        data=None
    )

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            data = json.load(file)

            map_params['data'] = data
            map_params['fname'] = filename

            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return render_template('drawing.html', **map_params)

@app.route('/reader')
def reader():
    data = read_data(app.config['READER_DATA_FILE'])

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
