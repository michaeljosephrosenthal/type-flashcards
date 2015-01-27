#!/usr/bin/python
# -*- coding: utf-8 -*-
# bottle deps
from bottle import TEMPLATE_PATH, route, jinja2_template as template, request, redirect
# Library deps
import json, csv, subprocess, random, os, io, psycopg2, urlparse
from models.models import Word, Translation
from sqlalchemy.orm import aliased
import config

TEMPLATE_PATH.append('./templates')

def get_cards(known, learning, db):
    second = aliased(Word)
    q = db.query(Word.text, second.text).\
            join(Translation, Word.id==Translation.word_a_id).\
            join(second, second.id==Translation.word_b_id).\
            filter(Word.lang==learning).\
            filter(second.lang==known)
    return [{learning: record[0], known: record[1]} for record in q]

def load_words(thai_wordlist):
    wordset = set(thai_wordlist)
    raw = open("volubilis.tsv", "r")
    volubilis = csv.DictReader(raw, delimiter='\t')
    for row in volubilis:
        if row["TH"] in wordset:
            add(thai = row["TH"], eng = row["EN"])

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
def add(db):
    thai = request.query.get('thai')
    eng = request.query.get('eng')
    thai_word = Word(lang='thai', text=thai)
    eng_word = Word(lang='eng', text=eng)
    db.add_all([thai_word, eng_word])
    db.commit()
    translation = Translation(word_a_id=thai_word.id, word_b_id=eng_word.id, score=1)
    db.add(translation)
    db.commit()
    redirect(request.query.get('redirect', "/eng/to/thai"))


@route('/')
def home():
    redirect(request.query.get('redirect', "/eng/to/thai"))

@route('/<first_lang>/to/<learning>')
def cards(first_lang, learning, db):
    context = {
            "wordlist": get_cards(first_lang, learning, db),
            "DEV": config.DEV,
            "known": first_lang,
            "learning": learning
            }
    return template('home.html', **context)
