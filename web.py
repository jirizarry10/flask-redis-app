import json
import redis
from flask import Flask, render_template, request


rdata = redis.StrictRedis(host='localhost', port=6379, db=0)
with open('movies.json',encoding="utf8") as data_file:
    test_data = json.load(data_file)
    for x in test_data:
        rdata.set(str(x['Title']), str(x['IMDB_Rating']))


app = Flask(__name__)


@app.route('/')
def index():
    outdat = "Spencer's Movie Database"
    return render_template('home.html', displaytext = outdat)

@app.route('/', methods=['POST'])
def my_form_post():
    movie = request.form['moviet']
    imdb = request.form['imdbr']
    option = request.form['command']
    if option == "Search":
        rating = rdata.get(movie)
        if rating is None:
            x = ("Invalid. Try Again.")
            return render_template('home.html', displaytext = x)
        else:
            x = ("Movie name: ", movie , "IMDB rating: ", rating)
            return render_template('home.html', displaytext = x)

    elif option == "Update":
        rating = rdata.get(movie)
        if imdb is None:
            x = ("Rating requires a value.")
            return render_template('home.html', displaytext = x)
        else:
            if rating is None:
                rdata.set(movie, imdb)
                x = ("Movie name: ", movie , "IMDB rating: ", rating, ". record added successfully")
                return render_template('home.html', displaytext = x)
            else:
                rdata.set(movie, imdb)
                x = ("Movie name: ", movie , "IMDB rating: ", imdb, ". Record updated successfully.")
                return render_template('home.html', displaytext = x)

    elif option == "Delete":
        rating = rdata.get(movie)
        if rating is None:
            x = ("incorrect entry. Please try again")
            return render_template('home.html', displaytext = x)
        else:
            rdata.delete(movie, imdb)
            x = ("Movie name: ", movie , "IMDB rating: ", rating, ". has been deleted from redis database successfully.")
            return render_template('home.html', displaytext = x)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, threaded=True)
