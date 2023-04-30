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
    answer = response.choices[0].message.content
    return answer

