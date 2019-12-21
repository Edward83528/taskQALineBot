import re
import pickle
from sklearn.feature_extraction.text import HashingVectorizer
from nltk.stem.porter import PorterStemmer
import warnings
warnings.filterwarnings("ignore")

#加載停用詞
stop = pickle.load(open("pkl/stopwords.pkl","rb"))

#删除HTML標記和標點符號，去除停用詞
def tokenizer(text):
    #去除HTML標記
    text = re.sub("<[^>]*>","",text)
    #獲取所有表情符
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text.lower())
    #删除標點符號
    text = re.sub("[\W]+"," ",text.lower())+" ".join(emoticons).replace("-","")
    #删除停用詞
    tokenized = [word for word in text.split() if word not in stop]
    #提取詞干
    porter = PorterStemmer()
    #返回去除停用詞之後的單詞列表
    return [porter.stem(word) for word in tokenized]
#通過HashingVectorizer獲取到評論的特徵向量
vect = HashingVectorizer(decode_error="ignore",n_features=2**21,
                         preprocessor=None,tokenizer=tokenizer)