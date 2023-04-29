from flask import Flask, request
from textDecoder import TextDecoder


app = Flask(__name__)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    decoder = TextDecoder(file, 'y0_AgAAAAAw3mtVAATuwQAAAADh_eq_P0vo8E87R_q8ZbjPSR5UQJsxqr0', 'ajef1hm4nhnc2v60u2vc')
    iam_token = decoder.get_iam_token()
    decoder.image_to_json()
    decoder.make_request(iam_token)
    text = decoder.get_text('output.json')
    return text


if __name__ == '__main__':
    app.run(debug=True)