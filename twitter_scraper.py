import twint
import threading
import os
import time

def scrape_func(location):
    while True:
        c = twint.Config()
        c.Near = location
        c.Lang = "en"
        c.Limit = 400
        c.Hide_output = True
        c.Pandas = True
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        if os.path.exists("./out2.csv"):
            Tweets_df.to_csv('out2.csv',mode = 'a', index=False, header=False)
        else:
            Tweets_df.to_csv('out2.csv',index=False)
        twint.storage.panda.clean()
        time.sleep(1)

def scrape_func_df(location):
        c = twint.Config()
        c.Near = location
        c.Lang = "en"
        c.Limit = 400
        c.Hide_output = True
        c.Pandas = True
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df
        return Tweets_df

        
if __name__ == "__main__":
    t1 = threading.Thread(target=scrape_func,args=("america",))

    t1.start()

    t1.join()
