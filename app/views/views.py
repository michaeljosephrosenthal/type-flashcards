#!/usr/bin/python
# -*- coding: utf-8 -*-
# bottle deps
from bottle import TEMPLATE_PATH, route, jinja2_template as template, request, redirect
# Library deps
import json, csv, subprocess, random, os, io, psycopg2, urlparse
from psycopg2 import extras
import config

url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor(cursor_factory=extras.DictCursor)

TEMPLATE_PATH.append('./templates')


def get_cards():
    cur.execute("select eng, thai from basic_card;")
    cards = [{"eng": w["eng"], "thai": str(w["thai"]).rstrip().encode('utf-8')}
             for w in cur.fetchall()]
    for w in cards: print w['thai'] 
    conn.commit()
    return cards

def create_card(thai, eng):
    cur.execute("insert into basic_card (thai, eng) values (%(str)s, %(str)s);", (thai, eng))
    conn.close()

def load_words(thai_wordlist):
    wordset = set(thai_wordlist)
    raw = open("volubilis.tsv", "r")
    volubilis = csv.DictReader(raw, delimiter='\t')
    for row in volubilis:
        if row["TH"] in wordset:
            create_card(thai = row["TH"], eng = row["EN"])

def trans(word):
    child = subprocess.Popen(['trans', '-b', word], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    eng = child.stdout.read().rstrip()
    child.communicate('')
    return eng

def save_words(f, lst):
    f.seek(0)
    f.write(json.dumps(lst))
    f.truncate()

def init_list():
    with open("wordlist.txt", "r") as thai_words, open('wordlist.json', 'r+') as json_file:
        translated = json.load(json_file)
        new_wordlist = [
                word.rstrip().decode('utf-8')
                for word in thai_words.readlines()
                if word.rstrip().decode('utf-8')
                not in [ w["thai"] for w in translated ]
            ]
        for word in new_wordlist:
            translated.append({
                "thai": word,
                "eng": trans(word)
                })
        save_words(json_file, translated)
        translated.reverse()
        return translated
    
@route('/add')
def add():
    thai = request.query.get('thai')
    eng = request.query.get('eng')
    create_card(thai, eng)
    redirect(request.query.get('redirect', "/eng/to/thai"))


@route('/')
def home():
    redirect(request.query.get('redirect', "/eng/to/thai"))

@route('/<first_lang>/to/<learning>')
def cards(first_lang, learning):
    context = {
            "wordlist": get_cards(),
            "DEV": config.DEV,
            "known": first_lang,
            "learning": learning
            }
    return template('home.html', **context)
