from app import app,getImage
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from secrets import *
from FaceMat.UNET import *
#FaceMatter
#Api to Upload a Image with face
#send to backend
#preprocess --> load --> predict --> return mask,Matted face




ALLOWED_EXTENSIONS = {'png','jpg'}



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            return redirect(url_for('process_files',filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>

    </form>
    '''


@app.route('/process_files/<filename>')
def process_files(filename=None):
    
    f,b=getImage(filename)



    return f,b








