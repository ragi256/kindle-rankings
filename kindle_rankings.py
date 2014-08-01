#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/usrs/sd12425/usr/py-lib')
import os
import pickle
from flask import Flask, render_template

app = Flask(__name__)

f = open('rankings.txt', 'r')
rankings = pickle.load(f)


@app.route('/')
def index():
    return render_template('kindle_ranking.html', rankings=rankings)


@app.route('/ID')
def idpage():
    return os.getenv("ID")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
