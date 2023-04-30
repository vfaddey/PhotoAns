import openai
openai.api_key = "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"


def ask_gpt(question):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': f'{question}'
            }
        ],
    )
    answer = response.choices[0].message.content.replace('\n', '<br>')
    return answer

