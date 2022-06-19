import pandas as pd

category_list = ["Arts & Entertainment:0", "Finance:1", "Food & Drink:2", "News:3", "Science:4", "Sports:5" ,"Other:6"]

all_tweets = pd.read_csv("out.csv")

col_headers = all_tweets.columns.to_list()
col_headers.append("category")

annotated_tweets = pd.DataFrame(columns=col_headers)

try:
    for index, row in all_tweets.iterrows():
        if row["language"] == "en":
            print("=======================================\n\n\n")
            print(row.tweet)
            print(category_list)
            inp_category = input("Which category is the tweet? \n")
            print(inp_category)
            if inp_category == "q":
                break
            elif inp_category == "":
                pass
            elif int(inp_category)<7 and int(inp_category) > -1:
                row["category"] = inp_category
                annotated_tweets = annotated_tweets.append(row, ignore_index=True)
            else:
                pass
        
except: 
    pass


annotated_tweets.to_csv("annotated_tweets.csv",index=False)