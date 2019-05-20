#!/usr/bin/env python
# from pprint import pformat
import os

import requests
import api
import random
from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "G59Q#m$HWvhMYs#Kuw#nT7eeKF%@ofoBhUBz4MZrF0UUvN5s#*8CB4l!B#Uz9Ob@xW4m#8VRf88"

RAVELRY_USERNAME = os.environ.get('RAVELRY_USERNAME')
RAVELRY_PASSWORD = os.environ.get('RAVELRY_PASSWORD')

class Pattern:
    url = 'https://www.ravelry.com/patterns/library/'

    def __init__(self, pattern_id):
        pattern_info = api.get_pattern_by_id(pattern_id)
        self.name = pattern_info['name']
        self.permalink = pattern_info['permalink']
        self.url = self.url + self.permalink
        self.photos = []
        for photo in pattern_info['photos']:
            self.photos.append(photo['medium2_url'])
        # self.photo_url = pattern_info['photos'][0]['medium2_url'] #grabs first photo


@app.route("/")
def homepage():
    """ Render homepage. """

    return render_template('homepage.html')

@app.route("/rav-data")
def get_users_rav_data():
    """ Grab user's personal ravelry data"""
    username = request.args.get('username')

    if api.user_is_valid(username):
        user_patts = []
        user_data_functions = [api.get_user_favs(username),
                            api.get_user_queue(username),
                            api.get_user_library(username)]
        for funct in user_data_functions:
            patts = funct
            user_patts.append(patts)
        session['user_patts'] = user_patts
        return redirect('/search')
    else:
        flash(f'"{username}" is not a valid ravelry account. Please try again.')
        return redirect('/')


@app.route("/search")
def render_search_page():

    yarns = ['lace', 'fingering', 'sport', 'dk', 'worsted', 'bulky']
    pattern_types = ['slippers', 'socks', 'hat', 'gloves', 'mittens', 
                    'fingerless gloves','purse', 'cowl', 'scarf', 'shawl', 
                    'blanket', 'pullover', 'cardigan']

    return render_template('search.html',
                            yarns=yarns,
                            pattern_types=pattern_types,
                            )


@app.route("/search-rav")
def display_search_rav():

    yarn_type = request.args.get('yarn')
    pattern_type = request.args.get('pattern_type')

    search_params = {'craft': 'knitting',
                    'weight': yarn_type, 
                    'pc': pattern_type,
                    }
    print(search_params)
    search_results = api.search_rav(search_params)
    pattern_ids = random.choices(search_results, k=6)
    patterns = []

    for patt in pattern_ids:
        patt = Pattern(patt)
        patterns.append(patt)

    return render_template('search-results.html', patterns=patterns)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    # DebugToolbarExtension(app)
