from flask import Flask, request, jsonify
from textDecoder import TextDecoder
from flask_cors import CORS
from solution import ask_gpt

app = Flask(__name__)
CORS(app)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['image']
    decoder = TextDecoder(file, 'y0_AgAAAAAw3mtVAATuwQAAAADh_eq_P0vo8E87R_q8ZbjPSR5UQJsxqr0', 'ajef1hm4nhnc2v60u2vc')
    iam_token = decoder.get_iam_token()
    decoder.image_to_json()
    decoder.make_request(iam_token)
    text = decoder.get_text('output.json')
    answer = ask_gpt(text)
    response = {
        'text': format_response(text, answer),
    }
    return jsonify(response)


@app.route('/process_text', methods=['POST'])
def process_text():
    text_input = request.json['text_input']
    if len(text_input) > 200:
        response = {
            'text': 'Запрос превысил лимит символов'
        }
        return jsonify(response)
    answer = ask_gpt(text_input)
    response = {
        'text': format_response(text_input, answer)
    }
    return jsonify(response)


def format_response(text, answer):
    full_answer = '<h4>Вопрос</h4>' + text + '<br>' + '<h4>Ответ</h4>' + answer
    return full_answer


if __name__ == '__main__':
    app.run(host='192.168.0.106', debug=True, port=7001)
