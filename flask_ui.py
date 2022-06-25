from flask import Flask,flash, render_template, request, redirect
from wtforms import Form, StringField, SelectField
from lucene_query import lucene_query



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
tweet_searcher = lucene_query()



class_dict = {"Business": 0, "Entertainment" : 1, "Politics": 2, "Sport" : 3, "Tech" : 4, "All" : 5}


class TweetSearchForm(Form):
    choices = [('All', 'All'),
               ('Business', 'Business'),
               ('Entertainment', 'Entertainment'),
               ('Politics', 'Politics'),
               ('Sport', 'Sport'),
               ('Tech', 'Tech'),]
    select = SelectField("Categories",choices=choices)
    search = StringField('')

@app.route('/', methods=['GET', 'POST'])
def index():
    search = TweetSearchForm(request.form)
    fuzzy_flag = False
    try:
        if "I'm feeling lucky" == request.form["qname"]:
            fuzzy_flag = True
        if request.method == 'POST':
            return search_results(search,fuzzy_flag)
    except:
        pass
    return render_template('index.html', form=search)
@app.route('/search')
def search_results(search, fuzzy_flag):
    results = []
    ids = []
    date = []
    search_string = search.data['search']
    if fuzzy_flag:
        search_string = search_string.strip()
        search_string = ' '.join(search_string.split())
        search_string = search_string.replace(" ", "~ ")
        search_string = search_string + "~"

    search_choice = search.data["select"]
    if search_string == '':
        return render_template('index.html', results=results, form = TweetSearchForm(request.form))
    results, ids, date = tweet_searcher.search(search_string, class_dict[search_choice])
    return render_template('index.html', results=results, ids = ids, dates = date , form = TweetSearchForm(request.form))
if __name__ == '__main__':
    app.run(debug= True)