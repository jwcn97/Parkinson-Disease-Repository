# === Import ===
import os

from flask import Flask, render_template, redirect

# === Vars ===
file_num = 0
path = ''

# === Flask ===
# Start application
app = Flask(__name__)
application = app

# App configurations
app.config["FILE_CREATE"] = './files' # Folder within which to create .txt files

# === HTML ===
@app.route('/', methods=["GET", "POST"])
def home_page():
    """
    Function to handle the home page. 
    Has a single button, 'Create file'
    When button is clicked, creates a .txt file
    Content of .txt file is the name of the .txt file.
    """
    # return render_template("home.html")
    return """<form action='/create-file' method="POST"> 
    <button>Create file</button>
</form>
<br>
""" + "<div>" + str(file_num) + "</div>" + "<br><div>" + str(path) + "</div>"


@app.route('/create-file', methods=["POST"])
def create_file():
    """
    Creates a file based on the names of the files already in the folder.
    """
    global file_num, path

    number_of_files = os.listdir(os.getcwd() + '/files')
    number_of_files = str(len(number_of_files))

    print(number_of_files)

    file_num = number_of_files
    path = os.getcwd()

    fp = open(app.config["FILE_CREATE"] + '/' + number_of_files + '.txt', mode='w+')
    fp.write(number_of_files)
    fp.close()

    return redirect('/')
