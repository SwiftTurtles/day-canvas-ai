from krwordrank.sentence import summarize_with_sentences
from konlpy.tag import Kkma

class TextSummarizer:
  def __init__(self):
    self.kkma = Kkma()

  def summarize_text(self, text):
    try:
        texts = self.kkma.sentences(text)
        sentences_count = len(texts)
        min_count = 5
        num_keysents = 3

        if sentences_count < 16:
            min_count = 1
            num_keysents = 1
        elif sentences_count < 31:
            min_count = 2
        elif sentences_count < 46:
            min_count = 3
        elif sentences_count < 61:
            min_count = 4

        keywords, sents = summarize_with_sentences(texts, min_count=min_count, num_keysents=num_keysents)
        return sents

    except Exception as e:
        print(f"Error: {e}")
        return None
      
