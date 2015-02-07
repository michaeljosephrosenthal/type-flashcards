#!/usr/bin/python
# -*- coding: utf-8 -*-
# bottle deps
import bottle
from bottle import TEMPLATE_PATH, route, post, put, get, delete, jinja2_template as template, request, redirect
# Library deps
import json, csv, subprocess, random, os, io, urlparse, itertools, re
from StringIO import StringIO
from models import Word, Translation, WordList, WordListItem
from sqlalchemy.orm import aliased
from sqlalchemy import or_, and_
import config, db
from util import uniqify
TEMPLATE_PATH.append('./templates')

def get_cards(known, learning):
    second = aliased(Word)
    session = db.create_session()
    q = session.query(Word.text, second.text, Translation.score).\
            join(Translation, or_(Word.id==Translation.word_a_id, Word.id==Translation.word_b_id)).\
            join(second, or_(second.id==Translation.word_a_id, second.id==Translation.word_b_id)).\
            filter(Word.lang==learning,
                   second.lang==known).\
            order_by(Translation.score.desc())
    translation_dict = {}
    for record in q:
        if translation_dict.has_key(record[0]):
            translation_dict[record[0]].append(record[1])
        else:
            translation_dict[record[0]] = [record[1]]
    session.commit()
    return [{learning: k, known: v} for k, v in translation_dict.items()]

def add_translations(words):
    session = db.create_session()
    translations = []
    for word in words:
        cat = word.pop('category')
        synced_words = []
        for lang, text in word.items():
            synced_words.append(Word(lang=lang, category=cat, text=text).sync_with(session))
        session.commit()
        translations.append(Translation(*[w.id for w in synced_words], score=1).sync_with(session))
    session.commit()
    return translations


@route('/add')
def add(route_db):
    thai = request.query.get('thai')
    phon = request.query.get('phon')
    eng = request.query.get('eng')
    category = request.query.get('cat')
    add_equal_wordlists('thai', category,
            thai = [{'text': thai, 'pronunciation': phon}], eng = [{'text': eng}])
    redirect(request.query.get('redirect', "/eng/to/thai"))

@route('/')
def home():
    redirect(request.query.get('redirect', "/eng/to/thai"))

@route('/api/<known>/to/<learning>')
def cards(known, learning, route_db):
    return {"words": get_cards(known, learning)}

@route('/<known>/to/<learning>')
def cards(known, learning, route_db):
    context = {
            "multi": True,
            "DEV": config.DEV,
            "known": known,
            "learning": learning }
    return template('base.html', **context)


@route('/wordlist/<name>/<known>/to/<learning>')
def wordlist_cards(name, known, learning, route_db):
    wordlist = route_db.\
            query(WordList).\
            filter(WordList.name == name).\
            one().materialize()
    context = {
            "wordlist": sorted(wordlist['items']),
            "multi": False,
            "name": wordlist['name'],
            "DEV": config.DEV,
            "known": known,
            "learning": learning }
    return template('type.html', **context)

@get('/create/wordlist')
def cwl():
    return template('add_wordlist.html')

@post('/create/wordlist')
def create_wordlist(route_db):
    form = dict(request.forms)
    header = [form['from'], form['to'], 'category']
    words = csv.DictReader(StringIO(form['words']), header, delimiter=form['delimiter'])
    translations = add_translations(list(words))
    lst = WordList(form['name'], translations, route_db)
    redirect("/".join(['', 'wordlist', lst.name, form['from'], 'to', form['to']]))
