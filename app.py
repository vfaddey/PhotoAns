from flask import Flask, request
from textDecoder import TextDecoder


app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    decoder = TextDecoder(file, 'YOUR YANDEX OAUTH-TOKEN', 'YOUR YANDEX-CLOUD FOLDER-ID')
    iam_token = decoder.get_iam_token()
    decoder.image_to_json()
    decoder.make_request(iam_token)
    text = decoder.get_text('output.json')
    return text


if __name__ == '__main__':
    app.run(debug=True)
