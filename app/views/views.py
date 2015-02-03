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

def get_wordlist_cards(name, known, learning):
    second = aliased(Word)
    session = db.create_session()
    wordlist = session.query(WordList).filter(WordList.name == name).one().materialize()
    return wordlist

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


def add_equal_wordlists(base_lang, category, **lang_to_lists):
    session = db.create_session()
    db_lists = dict()
    for lang, wlist in lang_to_lists.items():
        db_lists[lang] = [
                Word(lang=lang, category=category, **w).sync_with(session)
                for w in uniqify(wlist)]
    session.commit()
    base_list = db_lists.pop(base_lang)
    for llang, wlist in db_lists.items():
        translations = [Translation(base.id, target.id, score=1).sync_with(session)
                for base, target in itertools.product(base_list, wlist)]
        session.commit()

def vob_split(field, kind='word'):
    if kind == 'word':
        return re.split(r'\xc2\xa0; | ; ', field)
    elif kind == 'category':
        return re.split(r'\. *', field)[:-1]
    else: return field

def load_words(thai_wordlist):
    wordset = set(thai_wordlist)
    raw = open("volubilis.tsv", "r")
    volubilis = csv.DictReader(raw, delimiter='\t')
    for row in volubilis:
        if set(row["TH"].split('\xc2\xa0; ')) & wordset:
            thai_words = vob_split(row['TH'])
            thai_phon = vob_split(row['THAIPHON'])
            thai = [{"text": word, "pronunciation": phon}
                    for word, phon in zip(thai_words, thai_phon)]
            eng_words = [{"text": w} for w in vob_split(row['EN'])]
            category = row['TYPE']
            add_equal_wordlists('thai', category,
                    thai = thai, eng = eng_words)

def init_list(listfile):
    with open(listfile, "r") as thai_words:
        new_wordlist = [
                word.rstrip() for word in thai_words.readlines()
                #if word.rstrip().decode('utf-8')
                #not in [ w["thai"] for w in translated ]
            ]
        load_words(new_wordlist)
    
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

@route('/<known>/to/<learning>')
def cards(known, learning, route_db):
    context = {
            "wordlist": get_cards(known, learning),
            "multi": True,
            "DEV": config.DEV,
            "known": known,
            "learning": learning }
    return template('type.html', **context)


@route('/wordlist/<name>/<known>/to/<learning>')
def wordlist_cards(name, known, learning, route_db):
    lst = get_wordlist_cards(name,known,learning)
    context = {
            "wordlist": lst['items'],
            "multi": False,
            "name": lst['name'],
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
