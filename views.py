
import os
import json

from flask import render_template, Markup, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from app import app
from utils import DataManager

ALLOWED_EXTENSIONS = set(['txt', 'json'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/save', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        if 'fname' not in request.form and 'data-out-json' not in request.form:
            flash("No file to save")
            return redirect(url_for('drawing'))

        data = json.loads(request.form['data-out-json'])

        fpath = os.path.join(app.config['DATA_FOLDER'], secure_filename(request.form['fname']))

        DataManager.write_data(fpath, data)

        flash("File {} saved".format(fpath))

    return redirect(url_for('drawing'))

@app.route('/drawing', methods=['GET', 'POST'])
def drawing():
    map_params = dict(
        identifier="editor",
        varname="editor",
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
    
    return render_template('drawing.html', **map_params)

@app.route('/reader')
def reader():
    data_file_path = os.path.join(app.config['DATA_FOLDER'], app.config['READER_DATA_FILE'])
    data = DataManager.read_data(data_file_path)

    map_params = dict(
        identifier="reader",
        varname="reader",
        lat=48.383022,
        lng=31.1828699,
        zoom=6.5,
        data=data
    )
    return render_template('reader.html', **map_params)

@app.route('/')
def fullmap():
    map_params = dict(
        identifier="fullmap",
        varname="fullmap",
        lat=48.383022,
        lng=31.1828699,
        zoom=6,
        minZoom=6
    )
    return render_template('fullmap.html', **map_params)