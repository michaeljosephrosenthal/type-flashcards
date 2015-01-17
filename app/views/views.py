#!/usr/bin/python
# -*- coding: utf-8 -*-
from bottle import TEMPLATE_PATH, route, jinja2_template as template, DEBUG
import json, subprocess, random, os, io, config

TEMPLATE_PATH.append('./templates')

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
    

@route('/')
def home():
    return template('home.html', wordlist=init_list(), DEV=config.DEV)
