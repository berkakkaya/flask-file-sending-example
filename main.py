import blurhash
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from blurhash import encode
from os.path import isdir, isfile
from os import listdir, mkdir, remove

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 megabytes

@app.route("/file", methods=["GET"])
def send_the_file():
    if not isdir("files"):
        return "File is not submitted yet.", 404
    elif len(listdir(path="files/")) == 0:
        return "File is not submitted yet", 404
    
    filename = listdir(path="files/")[0]
    
    return send_file(f"files/{filename}")

@app.route("/file", methods=["POST"])
def get_file():
    file: FileStorage = request.files["file"]
    filename = secure_filename(file.filename)
    
    if len(filename) < 4:
        return "Invalid filename", 400
    
    if filename.split(".")[-1] not in ["jpg", "png", "jpeg"]:
        return "Filetype not allowed", 400
    
    if not isdir("files"):
        mkdir("files")
        
    files = listdir("files/")
    
    if len(files) != 0:
        remove(f"files/{files[0]}")
    
    if isfile("blurhash_str.txt"):
        remove("blurhash_str.txt")
    
    file.save(f"files/{filename}")
    
    del file
    
    blurhash_str = blurhash.encode(f"files/{filename}", x_components=4, y_components=3)
    
    with open("blurhash_str.txt", "w") as f:
        f.write(blurhash_str)
    
    return "File was successfully submitted."

@app.route("/blurhash", methods=["GET"])
def send_blurhash():
    if not isfile("blurhash_str.txt"):
        return "Blurhash string not exists", 404
    
    with open("blurhash_str.txt", "r") as f:
        content = f.read()
    
    return content

