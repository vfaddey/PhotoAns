import openai
import config
openai.api_key = config.api_key


def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': f'Представь, что ты сдаешь экзамен и тебе нужно решить этот тест: \n {question}'
            }
        ],
    )
    answer = response.choices[0].message.content.replace('\n', '<br>')
    return answer
