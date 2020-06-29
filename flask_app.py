# Markus Schiffer © June 2020
# This site is the API for the site WeatherGuide

from flask import Flask
from flask import request
from flask import abort
from flask_cors import CORS
import json

app = Flask(__name__)
app.config["DEBUG"] = False

# Only allow my website to use this API, no one else.
cors = CORS(app, resources = {
    r"/*": {
        "origin": "https://weather-global.netlify.app/"
    }
})

# Python instance of json data, used for the responses.
data = {}
with open('/home/markusschiffer/mysite/database/posts.json') as json_file:
    data = json.load(json_file)

# Main API route, doesn't do anything.
@app.route('/')
def home():
    return 'Welcome to the WeatherGuide API!'

# The client wants a list of all blog posts:
@app.route('/get-posts')
def get_posts():
    return data

# The client is informing us of a new blog post. Let's save it.
@app.route('/new-post')
def new_post():
    # process query string
    args = request.args

    # validate query string, create new post (as dictionary)
    next_post = {}
    if not 'title' in args:
        abort(400)
    else:
        next_post['title'] = args['title']
    if not 'author' in args:
        abort(400)
    else:
        next_post['author'] = args['author']
    if not 'time' in args:
        abort(400)
    else:
        next_post['time'] = args['time']
    if not 'content' in args:
        abort(400)
    else:
        next_post['content'] = args['content']

    # add the post to the local data structure and file database
    data['posts'].insert(0, next_post)
    with open('/home/markusschiffer/mysite/database/posts.json', 'w') as \
    outfile:
        json.dump(data, outfile)
    return 'Success', 200
