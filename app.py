from flask import Flask, request, jsonify, render_template
from textDecoder import TextDecoder
from flask_cors import CORS
from solution import ask_gpt

app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/home')
def main():
    return render_template('index.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Дает ответ на вопросы на картинке

    OAuth-token Яндекс и folder-id используете свои из Yandex.cloud
    """
    # Получаем картинку и читаем текст на ней с помощью Yandex.vision
    file = request.files['image']
    decoder = TextDecoder(file, oauth_token='YOUR OAuth-token Yandex', folder_id='YOUR YANDEX-FOLDER-ID')
    iam_token = decoder.get_iam_token()
    decoder.image_to_json()
    decoder.make_request(iam_token)
    text = decoder.get_text('output.json')

    # Получаем ответ GPT на заданные вопросы
    try:
        answer = ask_gpt(text)
    except:
        answer = 'GPT не смог  дать ответ'

    # Возвращаем текст ответа
    response = {
        'text': format_response(text, answer),
    }
    return jsonify(response)


@app.route('/process_text', methods=['POST'])
def process_text():
    """
    Дает ответ от GPT на заданный вопрос
    """

    # Читаем текст и проверяем на длину
    text_input = request.json['text_input']
    if len(text_input) > 300:
        response = {'text': 'Запрос превысил лимит символов'}
        return jsonify(response)
    elif len(text_input) < 10:
        response = {'text': 'Запрос слишком короткий'}
        return response

    # Получаем ответ от GPT
    try:
        answer = ask_gpt(text_input)
    except:
        answer = 'GPT не смог  дать ответ'

    # Возвращаем текст ответа
    response = {
        'text': format_response(text_input, answer)
    }
    return jsonify(response)


def format_response(text, answer):
    """
    Форматирует текст для html
    """
    full_answer = '<h4>Вопрос</h4>' + text + '<br>' + '<h4>Ответ</h4>' + answer
    return full_answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7000)
