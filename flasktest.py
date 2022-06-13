from flask import Flask,flash, render_template, request, redirect
from wtforms import Form, StringField, SelectField
from luceneQuery import lucene_query


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
tweet_searcher = lucene_query()



class TweetSearchForm(Form):
    choices = [('All', 'All'),
               ('Category1', 'Category1'),
               ('Category2', 'Category2')]
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
    results = tweet_searcher.search(search_string)
    results.insert(0, str(len(results)) + " tweets have been listed.")
    """
    if search.data['search'] == '':
        pass
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
    """
    return render_template('index.html', results=results, form = TweetSearchForm(request.form))
if __name__ == '__main__':
    app.run(debug= True)