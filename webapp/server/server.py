import os
import re
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import os
from pca import userplot, checkformat
from PIL import Image
import matplotlib
matplotlib.use('Agg')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Logging')

UPLOAD_FOLDER = '/app/webapp/server/static_files/files'
IMAGE_FOLDER = '/app/webapp/server/static_files/files/images'
ALLOWED_EXTENSIONS = {'csv'}
STATIC_FILES = '/app/webapp/server/static_files'

# static folder contains the js/css/img files to be distributed to client
# template folder contains the html templates to be rendered by Flask
app = Flask(__name__, static_folder='../static/dist',
            template_folder='../static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1000 * 1000
app.config['STATIC_FILES'] = STATIC_FILES
CORS(app)


@app.route('/')
def index():
    return render_template('index.html', pyvar='hello')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    if request.method == "POST":
        if 'newFile' not in request.files:
            logger.info("No file part")
            return redirect(request.url)
        logger.info("reading file")
        file = request.files['newFile']
        if file.filename == "":
            logger.info("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logger.info("Upload successful!")
            # return redirect(url_for('download_file', name=filename))
            return redirect(f"render/{filename}", code=303)
    return {
        "result": False,
        "message": "File not uploaded"
    }


@app.route('/render/<name>', methods=["GET"])
def render_notebook(name):
    logger.info("Rnder Notebooke ------Line------")
    logger.info(name)
    file = os.path.join(app.config["UPLOAD_FOLDER"], name)
    logger.info("File path: ")
    logger.info(file)
    name = re.findall(r"(.+).csv", name)[0]
    name = name + ".jpg"
    # logger.info(checkformat(file))
    logger.info("Name: ")
    logger.info(name)
    if checkformat(file) == False:
        return redirect(request.url, code=406)
    fig = userplot(file)
    fig.savefig(os.path.join(
        app.config["IMAGE_FOLDER"], name))
    # return redirect(url_for(app.config['STATIC_FILES'], filename="files/images/" + name))
    return send_from_directory(app.config['STATIC_FILES'], "files/images/" + name)


@app.route('/uploads/<name>', methods=["GET"])
def retrieve(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/downloads/<name>', methods=["GET"])
def downloads(name):
    name = re.findall(r"(.+).csv", name)[0]
    name = name + ".jpg"
    return send_from_directory(app.config["IMAGE_FOLDER"], name, as_attachment=True)


@app.route('/render/initial', methods=["GET"])
def initial_chart():
    # return redirect(url_for(app.config['STATIC_FILES'], filename="files/images/TOPdata_webfig_20221212.jpg"))
    return send_from_directory(app.config['STATIC_FILES'], "files/images/TOPdata_webfig_20221212.jpg")


@app.route("/upload/<name>", methods=["DELETE"])
def delete(name):
    file = os.path.join(app.config["UPLOAD_FOLDER"], name)
    os.remove(file)
    return {
        "result": True,
        "message": "File deleted"
    }


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0')
