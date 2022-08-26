import blurhash
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from os.path import isdir, isfile, join
from os import mkdir

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 megabytes

# Constants
FILENAME = "image"
BLURHASH_PATH = join("files", "blurhash.txt")


def read_blurhash_file():
    """Reads the blurhash file and returns filename and blurhash string from it.

    Returns
    -------
    list[str]
        List that consist of two parts: filename and blurhash string.
        Data is stored in the same order.
    """

    # Read data from the blurhash file 
    with open(BLURHASH_PATH, "r") as f:
        content = f.read()
    
    # Our file consists of two parts: [filename] [blurhash string]
    # Parts are splitted by space, so we have to use the split function
    # to access those parts separately.
    return content.split(" ")


@app.route("/file", methods=["GET"])
def send_the_file():
    # We store filename in the blurhash string file, so we read
    # that file first.

    # Check if the blurhash string file exists. If not, return 404
    if not isfile(BLURHASH_PATH):
        return "File is not submitted yet", 404
    
    # Read the blurhash file and obtain the filename from it
    content = read_blurhash_file()
    filename = content[0]

    # Check if the image still exists
    filepath = join("files", filename)
    if not isfile(filepath):
        return "File is not submitted yet", 404
    
    # Send the image
    return send_file(filepath)


@app.route("/file", methods=["POST"])
def get_the_file():
    # Get the file from request
    file: FileStorage = request.files["file"]
    filename = secure_filename(file.filename)
    
    # Split the filename as base and extension
    filename_splitted = filename.split(".")

    # Return 400 for invalid filenames
    if len(filename_splitted) != 2 or filename_splitted[0] == "":
        return "Invalid filename", 400

    # Also block every file other than "jpg", "png" and "jpeg"
    if filename_splitted[-1] not in ["jpg", "png", "jpeg"]:
        return "Filetype not allowed", 400
    
    # NOTE: For demonstration, files will be stored inside local storage.
    # Create the data directory, if not exists
    if not isdir("files"):
        mkdir("files")
    
    # Change the filename to proper one and save the image
    filename = f"{FILENAME}.{filename_splitted[-1]}"
    image_path = join("files", filename)
    file.save(image_path)
    
    # Create a blurhash string for the image
    blurhash_str = blurhash.encode(image_path, x_components=4, y_components=3)

    # Save the string to a file
    with open(BLURHASH_PATH, "w") as f:
        # File will consist of two parts: [filename] [blurhash string]
        data = f"{filename} {blurhash_str}"

        f.write(data)

    return "File was successfully submitted."


@app.route("/blurhash", methods=["GET"])
def send_blurhash():
    # Check if the blurhash file exists
    if not isfile(BLURHASH_PATH):
        return "File is not submitted yet", 404
    
    # Read the blurhash string from the file
    content = read_blurhash_file()
    blurhash_str = content[1]

    return blurhash_str
