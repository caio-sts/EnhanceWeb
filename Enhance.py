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

            path_img = 'static/uploads/{} img.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_img, img)
            
            imgHE = enhanceLib.he(img)
            path_HE = 'static/processeds/{} imgHE.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_HE, imgHE)
            psnrHE = round(metricsLib.PSNR(imgHE, metricsLib.MSE(img, imgHE)), 3)
            ssimHE = round(metricsLib.SSIM(img, imgHE), 3)

            imgDHE = enhanceLib.dhe(img)
            path_DHE = 'static/processeds/{} imgDHE.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_DHE, imgDHE)
            psnrDHE = round(metricsLib.PSNR(imgDHE, metricsLib.MSE(img, imgDHE)), 3)
            ssimDHE = round(metricsLib.SSIM(img, imgDHE), 3)

            imgYing = enhanceLib.Ying_2017_CAIP(img)
            path_Ying = 'static/processeds/{} imgYing.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_Ying, imgYing)
            psnrYing = round(metricsLib.PSNR(imgYing, metricsLib.MSE(img, imgYing)), 3)
            ssimYing = round(metricsLib.SSIM(img, imgYing), 3)

            imgGamma = enhanceLib.iagc(img)
            path_Gamma = 'static/processeds/{} imgGamma.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_Gamma, imgGamma)
            psnrGamma = round(metricsLib.PSNR(imgGamma, metricsLib.MSE(img, imgGamma)), 3)
            ssimGamma = round(metricsLib.SSIM(img, imgGamma), 3)


            imgLime = enhanceLib.enhance_image_exposure(img)
            path_Lime = 'static/processeds/{} imgLime.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_Lime, imgLime)
            psnrLime = round(metricsLib.PSNR(imgLime, metricsLib.MSE(img, imgLime)), 3)
            ssimLime = round(metricsLib.SSIM(img, imgLime), 3)

            imgUnderwater = enhanceLib.rghs(img)
            path_Underwater = 'static/processeds/{} imgUnderwater.png'.format(len(os.listdir("static\\uploads")))
            imageio.imwrite(path_Underwater, imgUnderwater)
            psnrUnderwater = round(metricsLib.PSNR(imgUnderwater, metricsLib.MSE(img, imgUnderwater)), 3)
            ssimUnderwater = round(metricsLib.SSIM(img, imgUnderwater), 3)
            

            return render_template("enhance.html", image = path_img, HE = path_HE, psnrHE=psnrHE,\
                ssimHE=ssimHE, DHE=path_DHE, psnrDHE=psnrDHE, ssimDHE=ssimDHE, Ying=path_Ying,\
                psnrYing=psnrYing, ssimYing=ssimYing, Gamma=path_Gamma, psnrGamma=psnrGamma,\
                ssimGamma = ssimGamma, Lime=path_Lime, psnrLime=psnrLime, ssimLime=ssimLime,\
                Underwater=path_Underwater, psnrUnderwater=psnrUnderwater, ssimUnderwater=ssimUnderwater)
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