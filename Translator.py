import requests
import json

class Translator:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = 'https://openapi.naver.com/v1/papago/n2mt'
        self.headers = {
            'Content-Type': 'application/json',
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret
        }

    def translate(self, text, source_lang='ko', target_lang='en'):
        try:
            data = {'source': source_lang, 'target': target_lang, 'text': text}
            response = requests.post(self.api_url, json.dumps(data), headers=self.headers)
            response.raise_for_status()   # 오류 발생한 경우 예외 발생
            translated_text = response.json()['message']['result']['translatedText']
            return translated_text
        except requests.exceptions.RequestException as e:
            print(f"Translator Error: {e}")
            return None
          
