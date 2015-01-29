#!/usr/bin/python
# -*- coding: utf-8 -*-
# bottle deps
from bottle import TEMPLATE_PATH, route, jinja2_template as template, request, redirect
# Library deps
import json, csv, subprocess, random, os, io, urlparse, itertools, re
from models.models import Word, Translation
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
            filter(and_(Word.lang==learning, second.lang==known)).\
            order_by(Translation.score.desc())
    translation_dict = {}
    for record in q:
        if translation_dict.has_key(record[0]):
            translation_dict[record[0]].append(record[1])
        else:
            translation_dict[record[0]] = [record[1]]
    session.commit()
    return [{learning: k, known: v} for k, v in translation_dict.items()]

def get_word_id(word):
    session = db.create_session()
    record = session.query(Word.id).\
            filter(Word.lang==word.lang,
                   Word.text==word.text,
                   Word.category==word.category
                   ).first()
    word.id = record[0] if record else None
    session.commit()
    return word

def get_translation_id(translation):
    session = db.create_session()
    record = session.query(Translation.id).\
            filter(Translation.word_a_id==translation.word_a_id,
                   Translation.word_b_id==translation.word_b_id
                   ).first()
    session.commit()
    translation.id = record[0] if record else None
    return translation

def add_equal_wordlists(base_lang, category, **lang_to_lists):
    session = db.create_session()
    db_lists = dict()
    for lang, wlist in lang_to_lists.items():
        db_lists[lang] = [
                get_word_id(Word(lang=lang, category=category, **w))
                for w in uniqify(wlist)]
        session.add_all([word for word in db_lists[lang] if word.id is None])
    session.commit()
    base_list = db_lists.pop(base_lang)
    for llang, wlist in db_lists.items():
        translations = [get_translation_id(
            Translation(word_a_id=base.id,
            word_b_id=target.id, score=1))
         for base, target in itertools.product(base_list, wlist)]
        session.add_all([t for t in translations if t.id is None])
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

@route('/<first_lang>/to/<learning>')
def cards(first_lang, learning, route_db):
    context = {
            "wordlist": get_cards(first_lang, learning),
            "DEV": config.DEV,
            "known": first_lang,
            "learning": learning
            }
    return template('home.html', **context)
