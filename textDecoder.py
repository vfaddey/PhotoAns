import base64
import json
from requests import post
from nested_lookup import nested_lookup
import os


class TextDecoder:
    def __init__(self, file, oauth_token=None, folder_id=None):
        self.file = file
        self.oauth_token = oauth_token
        self.folder_id = folder_id

    def encode_file(self, file):
        file_content = file.read()
        return base64.b64encode(file_content).decode('utf-8')

    def get_iam_token(self):
        iam_url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

        response = post(iam_url, json={"yandexPassportOauthToken": self.oauth_token})
        json_data = json.loads(response.text)
        if json_data is not None and 'iamToken' in json_data:
             return json_data['iamToken']
        return None

    def image_to_json(self):
        outfile = self.encode_file(self.file)
        out = {
            "folderId": "b1gq9lq6ihi5068iq6bs",
            "analyze_specs": [{
                "content": outfile,
                "features": [{
                    "type": "TEXT_DETECTION",
                    "text_detection_config": {
                        "language_codes": ["*"]
                    }
                }]
            }]
        }
        with open('body.json', 'w') as f:
            json.dump(out, f)

    @staticmethod
    def make_request(iam_token):
        os.system(f"export IAM_TOKEN={iam_token}")
        os.system(f'curl -X POST \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer {iam_token}" \
            -d "@body.json" \
            https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze > output.json')

    @staticmethod
    def get_text(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        ans = []
        for i, block in enumerate(nested_lookup('blocks', content)):
            ans.append([])
            for j, line in enumerate(nested_lookup('lines', block)):
                ans[i].append(' '.join(nested_lookup('text', line)) + '\n')
            ans[i] = ' '.join(ans[i]) + '\n\n'
        text = ''.join(ans)
        return text


