import boto3
from album_queue import request_album
from uuid import uuid4
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

bucket_address = '167885'


@app.route("/")
def index():
  return render_template('upload_form.html')


@app.route("/upload", methods=['POST'])
def upload():
  files = request.files
  album = {
    'photos': []
  }

  for f in files.getlist('file'):
    destination_name = generate_filename(f)
    album['photos'].append('%s/%s' % (bucket_address, destination_name))
    upload_s3(f, destination_name)

  return jsonify(album)


@app.route("/request-album", methods=['POST'])
def request_album_creation():
  email = request.form['email']
  photosCount = len(request.form)
  urls = []
  for index in range(0, photosCount-1):
    key = 'photos_%s' % index
    urls.append(request.form[key])

  album = {
    'sent_to': email,
    'photos': urls
  }
  request_album(album)

  return jsonify()

def upload_s3(source_file, destination_filename):
  s3 = boto3.resource('s3')
  bucket = s3.Bucket(bucket_address)
  bucket.put_object(Key=destination_filename, Body=source_file, ACL='public-read')

def generate_filename(source_file):
  destination_filename = "photos/%s/%s" % (uuid4().hex, source_file.filename)
  return destination_filename

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)