import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, Response
from werkzeug.utils import secure_filename

#-*- coding: utf-8 -*-  
from random import shuffle
from string import printable
chars=["क","ख","ग","घ","ङ","च","छ","ज","झ","ण","त","थ","द","ध","न","प","फ","ब","भ","म","य","र","ल","व","स","श","ष","ह","ञ","ै","ौ","ृ","ु","ू","ि","ी","ो","ा","े"]

def Convert(string): 
    list1=[] 
    list1[:0]=string 
    return list1 

printablefin = Convert(printable) + chars

keys=list(printablefin)
shuffled_keys=list(printablefin)
shuffle(shuffled_keys)


maps=dict(zip(keys,shuffled_keys))
reversed_maps=dict(zip(shuffled_keys,keys))

def encrypt(message):
    cipher=[]    
    for c in message:
            cipher.append(maps[c])
    return"".join(cipher)

def decrypt(cipher):
    plain_text = []
    for c in cipher:
            plain_text.append(reversed_maps[c])
    return''.join(plain_text)

def encryptFilehandler(fileName):
    f = open(fileName , "r") 
    message = f.read()  
    f.close()
    f = open(fileName , "w") 
    f.write(encrypt(message))
    f.close()

def decryptFilehandler(fileName):
    f = open(fileName , "r") 
    message = f.read()  
    f.close()
    f = open(fileName , "w") 
    f.write(decrypt(message))
    f.close()
    

app = Flask(__name__)

app.config['UPLOAD_PATH'] = '/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/uploads'
app.config['UPLOAD_PATH_I']= '/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/decrypted'
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
# manoj_sir/flaskIntro/uploads
@app.route('/')
def index():
    return render_template('index.html')
# for encrption page
@app.route('/encryptResult', methods=['POST'])
def upload_files():
    if request.method == 'POST':
        plainText = request.form.get("plainText")
        test = encrypt(plainText)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
                return render_template('rules.html')
            # dump()
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            files = os.listdir(app.config['UPLOAD_PATH'])
            filename = uploaded_file.filename
            encryptFilehandler("/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/uploads/"+uploaded_file.filename)  
            return render_template('encryptResult.html',cipher = test , files=files)
        return render_template('encryptResult.html',cipher = test )
    else:
        return render_template('index.html')

@app.route('/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)

@app.route("/getPlotCSV/<filename>")
def getPlotCSV(filename):
    with open('/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/uploads/'+filename) as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=uploads"+filename})

# for decryption page 
@app.route('/decryptResult', methods=['POST'])
def upload_filesI():
    if request.method == 'POST':
        cipher = request.form.get("cipher")
        plaintext = decrypt(cipher)
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
                return render_template('rules.html')
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH_I'], filename))
            files = os.listdir(app.config['UPLOAD_PATH_I'])
            filename = uploaded_file.filename
            decryptFilehandler("/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/decrypted/"+uploaded_file.filename)
            return render_template('decryptResult.html',plainText = plaintext , files=files)
        return render_template('decryptResult.html',plainText = plaintext )
    else:
        return render_template('index.html')

@app.route('/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/decrypted/<filename>')
def uploadI(filename):
    return send_from_directory(app.config['UPLOAD_PATH_I'], filename)


@app.route("/getPlot/<filename>")
def getPlotCSVI(filename):
    with open('/home/gautam/Documents/Studies/Advance programming/manoj_sir/flaskIntro/decrypted/'+filename) as fp:
        csv = fp.read()
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=decrypted"+filename})


if __name__ == '__main__':
   app.run(debug = True)

