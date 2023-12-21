from konlpy.tag import Kkma
from krwordrank.word import summarize_with_keywords

class KeywordExtractor:
    def __init__(self):
        self.kkma = Kkma()

    def extract_keys(self, dictionary, top_n=3):
        return list(sorted(dictionary.keys(), key=lambda x: dictionary[x], reverse=True)[:top_n])

    def extract_keyword(self, text, top_n=3):
        try:
            texts = self.kkma.sentences(text)
            sentences_count = len(texts)
            min_count = 5

            if sentences_count < 16:
                min_count = 1
                num_keysents = 1
            elif sentences_count < 31:
                min_count = 2
            elif sentences_count < 46:
                min_count = 3
            elif sentences_count < 61:
                min_count = 4

            keywords = summarize_with_keywords(self.compose_nouns(texts), min_count=min_count, max_length=10, beta=0.85, max_iter=10, verbose=True)

            # 중요도를 기준으로 상위 top_n개의 키를 추출
            top_keywords = self.extract_keys(keywords, top_n)

            return top_keywords

        except Exception as e:
            print(f"Error: {e}")

    def compose_nouns(self, texts):
        result = []
        for text in texts:
            if len(text) == 0:
                continue

            pos = self.kkma.pos(text)
            nouns = [word for word, pos in pos if pos == 'NNG']

            result.append(' '.join(nouns) + '.')

        return result
    
