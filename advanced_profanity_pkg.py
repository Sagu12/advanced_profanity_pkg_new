import pandas as pd
from wordsegment import load, segment
from detoxify import Detoxify
from pywsd.utils import lemmatize_sentence
import requests
import io
url= "https://raw.githubusercontent.com/Sagu12/advanced_profanity_pkg/main/en.csv"
s=requests.get(url).content
df=pd.read_csv(io.StringIO(s.decode('utf-8')) , error_bad_lines=False)
load()

class profanity():
    sentence= str
    def censor_profanity(sentence):
        wordlist = list(df["en_bad_words"])
        sentence = sentence.lower()
        sentence= " ".join(lemmatize_sentence(sentence))
        sentence= " ".join(segment(sentence))
        for word in sentence.split():
            if word in wordlist:            
                sentence = sentence.replace(word, "******")
        return sentence
    def advanced_profanity(sentence):
        sentence = sentence.lower()
        sentence= " ".join(lemmatize_sentence(sentence))
        sentence= " ".join(segment(sentence))
        res= Detoxify('original').predict(sentence)
        res= res.items()
        dict_iterator = iter(res)
        first_pair = next(dict_iterator)
        first_pair= str(first_pair)
        first_pair= first_pair.replace("toxicity", "profanity level")
        first_pair= first_pair.replace(",", ":")
        return [first_pair, profanity.censor_profanity(sentence)]