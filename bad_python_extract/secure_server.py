#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               Email: faisalkhan91@outlook.com                             #
#                               Created on October 8, 2019                                  #
#############################################################################################

# Importing modules

import os
import io
import errno
import zipfile
from werkzeug.utils import secure_filename
from flask import Flask, flash, request
from config import settings


def secure_unzip(zip_file, extractpath='.'):
    print("[INFO] Unzipping")
    try:
        files = []
        with zipfile.ZipFile(zip_file, 'r') as zf:
            for member in zf.infolist():
                filename = member.filename
                dat = zf.open(filename, "r")
                files.append(filename)
                abspath = os.path.abspath(os.path.join(extractpath, member.filename))
                print(abspath)
                zf.extract(member, extractpath)
                dat.close()
        return files
    except Exception as e:
        print("[ERROR] Unzipping Error " + str(e))


def html_escape(text):
    """Produce entities within text."""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


def allowed_file(filename):
    """Allowed File"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTS


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    """Handle Upload"""

    if request.method == 'POST':
        extraction_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "uploads")
        if 'file' not in request.files:
            flash('No file part')
            return "No File part!"
        file_uploaded = request.files['file']
        if file_uploaded.filename == '':
            flash('No selected file')
            return "No File Selected!"
        if 'file' and allowed_file(file_uploaded.filename):
            filename = secure_filename(file_uploaded.filename)
            write_to_file = os.path.join(extraction_path, filename)
            file_uploaded.save(write_to_file)
            secure_unzip(write_to_file, extraction_path)
            return "<b>Uploaded to</b> " + html_escape(write_to_file) + "<br>" + "<b>Content Extracted to</b> " + html_escape(extraction_path)


@app.route('/', methods=['GET'])
def main():
    """Home"""
    html = '''
    <form enctype="multipart/form-data" action="/upload" method="POST">
    Choose a file to upload:
    <input name="file" type="file" accept=".zip,.apk" />
    <input type="submit" value="Upload" />
    </form>
    '''
    return html


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(threaded=True, host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)

#############################################################################################
#                                       End of Program                                      #
#                                     Copyright (C) 2019                                    #
#############################################################################################
