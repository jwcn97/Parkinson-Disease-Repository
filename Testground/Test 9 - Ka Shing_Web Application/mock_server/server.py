# === Import ===
import os

from flask import Flask, render_template, redirect

import boto3
from botocore.exceptions import ClientError

# === AWS Keys ===
ACCESS_KEY = 'AKIAJNNNUQ62CYSN5ULQ'
SECRET_KEY = '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'
BUCKET = 'elasticbeanstalk-us-east-2-076733089560'

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

    # fp = open(app.config["FILE_CREATE"] + '/' + number_of_files + '.txt', mode='w+')
    # fp.write(number_of_files)
    # fp.close()

    # upload_file(str(number_of_files) + '.txt', BUCKET, '/files/' + str(number_of_files) + '.txt')
    s3_client = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        # aws_session_token=SESSION_TOKEN
    )

    s3_client.Object(
        BUCKET, 'files/' + str(number_of_files) + '.txt'
    ).put(Body=str(number_of_files) + '. testing testing 1 2 3 ')

    return redirect('/')


# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket

#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is used
#     :return: True if file was uploaded, else False
#     """

#     # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = file_name

#     # Upload the file
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=ACCESS_KEY,
#         aws_secret_access_key=SECRET_KEY,
#         # aws_session_token=SESSION_TOKEN
#     )
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True