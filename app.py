from flask import Flask, jsonify, request
from TextSummarizer  import TextSummarizer
from KeywordExtractor import KeywordExtractor
from Translator import Translator
import access_token
import model_path
from kobert import kobert_emotion_classifier as kec

# REST API 호출, 이미지 파일 처리에 필요한 라이브러리
from PyKakao import Karlo
import requests, json, urllib, uuid
from PIL import Image

app = Flask(__name__)

@app.route("/image", methods=['POST'])
def image():
    text = request.get_data()

    #텍스트 요약
    summary = ', '.join(summarize(text))
    
    #키워드 추출
    keyword = ', '.join(extract_keyword(text)) if len(text) > 1 else text[0]

    #감정 분석
    emotion = kec.predict(model_path.MODEL_PATH, summary)

    #텍스트 번역
    prompt = translate(summary + ', ' + keyword + ', ' + emotion)

    #이미지 생성
    response = make_image(prompt)
    # 응답의 첫 번째 이미지 생성 결과 출력하기
    result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
    
    ########################################################################################
    # 추후 S3로 변경 
    result.show()    # @Todo 추후 삭제 

    image_url = str(uuid.uuid1())+'.png'
    result.save(image_url)
    return image_url
    #########################################################################################


def make_image(prompt):
    positive_prompt = 'Create an image in the style of Claude Monet, mordern, oil paint, no english, without any accompanying text, without textual description'
    negative_prompt = 'any accompanying text, textual description, object out of frame, out of frame, body out of frame, bad anatomy, distortion, disfigured, poorly drawn face, watermark'
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            'prompt': prompt + positive_prompt,
            'negative_prompt': negative_prompt
        },
        headers = {
            'Authorization': f'KakaoAK {access_token.REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response


def summarize(text):
    try:
        # TextSummarizer 클래스로 요약 수행
        text_summarizer = TextSummarizer()
        result = text_summarizer.summarize_text(text)

        if result is not None:
            return result
        else:
            raise Exception('요약에 실패하였습니다.')
    except Exception as e:
        # 예외 처리
        return jsonify({'error': str(e)})


def extract_keyword(text):
    # TextSummarizer 클래스로 요약 수행
    keyword_extractor = KeywordExtractor()
    result = keyword_extractor.extract_keyword(text)

    # 결과 출력 및 반환
    if result is not None:
        return result
    else:
        raise Exception('키워드 추출에 실패하였습니다.')


def translate(text):
    translator = Translator(access_token.CLIENT_ID, access_token.CLIENT_SECRET)
    try:
        result = translator.translate(text)

        if result is not None:
            return result
        else:
            raise Exception('번역에 실패하였습니다.')
    except Exception as e:
        print(f"Translation failed. Error {e}")
    
    
if __name__ == '__main__':
    app.run()
  
