import os
import datetime
import hashlib
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from uuid import uuid4
import json
import shutil
from process import convert
import requests

app = Flask(__name__)
upload_key = ''

@app.route("/")
def FUN_root():
    try:
        shutil.rmtree('./static/uploads') 
    except:
        print('No such file')    
    return render_template("index.html")


@app.route("/upload_1",methods = ['GET','POST'])
def upload_1():
    form = request.form
  

    # Create a unique "session ID" for this particular batch of uploads.
    

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "./static/uploads/"
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)   
    print(request.files)
    print("entering loop")
    for upload in request.files.getlist("file1"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, 'front.jpg'])
        print("Accept incoming file:", filename)
        print("inside loop")
        print("Save it to:", destination)
        upload.save(destination)

    print("outside loop")
    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return render_template("upload_back.html")

@app.route("/upload_2",methods = ['GET','POST'])
def upload_2():
    form = request.form
  

    # Create a unique "session ID" for this particular batch of uploads.
    

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "./static/uploads/"

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)   
    print(request.files)
    print("entering loop")
    for upload in request.files.getlist("file1"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, 'back.jpg'])
        print("Accept incoming file:", 'back.jpg')
        print("inside loop")
        print("Save it to:", destination)
        upload.save(destination)

    print("outside loop")
    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return render_template("upload_selfie.html")  

@app.route("/upload_3",methods = ['GET','POST'])
def upload_3():
    form = request.form
  

    # Create a unique "session ID" for this particular batch of uploads.
    

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "./static/uploads/"

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)   
    print(request.files)
    print("entering loop")
    for upload in request.files.getlist("file1"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, 'selfie.jpg'])
        print("Accept incoming file:", filename)
        print("inside loop")
        print("Save it to:", destination)
        upload.save(destination)

    print("outside loop")
    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return render_template("get_results.html")  

@app.route("/kyc_demo",methods = ['GET','POST'])
def kyc_demo():
    return render_template("kyc_demo.html")    

@app.route("/upload",methods = ['GET','POST'])
def upload():
    return "API KEY GENERATION WILL BE SOON AVAILABLE"   

@app.route("/upload_front",methods = ['GET','POST'])
def upload_front():
    return render_template("upload_front.html")

@app.route("/process_images",methods = ['GET','POST'])
def process_images():

    front = convert("./static/uploads/front.jpg")
    back = convert("./static/uploads/back.jpg")
    selfie = convert("./static/uploads/selfie.jpg")


    PARAMS = {'selfie':selfie,'cin_back':back,'cin_front':front,'data_type':'base64'}
    r = requests.get(url = "http://0.0.0.0:80/cin_kyc", json = PARAMS)

    response = r.json()
    print(response)
   
    
    return render_template("results.html", response = response)
           


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
