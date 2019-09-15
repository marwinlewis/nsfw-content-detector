from flask import Flask, request
from flask_cors import CORS, cross_origin

import json
import os

from nsfw import classify_nsfw

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

CORS(app, resources={r"/api/*": {"origins": app.config['ALLOWED_DOMAINS']}})

@app.route('/')
def index():
    return 'server is working!'

@app.route('/api/nsfw', methods = ['POST'])
@cross_origin()
def upload():
    output = []
    if "images" in request.files:
        for image in request.files.getlist('images'):

            IMAGE_PATH = os.path.join(app.config['UPLOAD_PATH'], image.filename)
            
            image.save(IMAGE_PATH)

            output.append(classify_nsfw(IMAGE_PATH))

            #os.remove(IMAGE_PATH)

        return json.dumps([{'status':'success'},{"output": output}])
    else:
        return json.dumps({'status':'error'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')