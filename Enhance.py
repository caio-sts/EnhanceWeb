import os, imageio
from time import time
import numpy as np
from PIL import Image
import enhanceLib
import metricsLib
from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            img = Image.open(request.files['file'])
            img = img.resize((240, 180))
            img = np.array(img)

            path_img = 'static\\processeds\\img.png'
            imageio.imwrite(path_img, img)
            
            imgHE = enhanceLib.he(img)
            psnrHE = round(metricsLib.PSNR(imgHE, metricsLib.MSE(img, imgHE)), 3)
            ssimHE = round(metricsLib.SSIM(img, imgHE), 3)

            """
            imgDHE = enhanceLib.dhe(img)
            psnrDHE = metricsLib.PSNR(imgDHE, metricsLib.MSE(img, imgDHE))
            ssimDHE = metricsLib.SSIM(img, imgDHE)

            imgYing = enhanceLib.Ying_2017_CAIP(img)
            psnrYing = metricsLib.PSNR(imgYing, metricsLib.MSE(img, imgYing))
            ssimYing = metricsLib.SSIM(img, imgYing)
            """

            return render_template("enhance.html", image = path_img, psnrHE=psnrHE, ssimHE=ssimHE)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>'''

if __name__ == "__main__":
    app.run(debug=True)