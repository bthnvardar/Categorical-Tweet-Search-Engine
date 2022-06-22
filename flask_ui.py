from flask import Flask,flash, render_template, request, redirect
from wtforms import Form, StringField, SelectField
from luceneQuery import lucene_query



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
tweet_searcher = lucene_query()



class_dict = {"World": 0, "Sports" : 1, "Business": 2, "Science" : 3, "All" : 4}


class TweetSearchForm(Form):
    choices = [('All', 'All'),
               ('World', 'World'),
               ('Sports', 'Sports'),
               ('Business', 'Business'),
               ('Science', 'Science'),]
    select = SelectField("Categories",choices=choices)
    search = StringField('')

@app.route('/', methods=['GET', 'POST'])
def index():
    search = TweetSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)
@app.route('/search')
def search_results(search):
    results = []
    search_string = search.data['search']
    search_choice = search.data["select"]
    if search_string == '':
        return render_template('index.html', results=results, form = TweetSearchForm(request.form))
    results = tweet_searcher.search(search_string, class_dict[search_choice])
    return render_template('index.html', results=results, form = TweetSearchForm(request.form))
if __name__ == '__main__':
    app.run(debug= True)