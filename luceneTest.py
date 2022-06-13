import pandas as pd
import string
import re


tweets = pd.read_csv("out.csv")

tweetArr = tweets[tweets.language == "en"].tweet

tweetArr = tweetArr.apply(lambda x: x.lower())

cnt = 1
for row in tweetArr:
    with open('./docs/'+str(cnt), 'w') as f:
        f.write(re.sub(r'\W+', ' ',row))
    cnt+=1