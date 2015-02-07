import csv, re, db, sys, itertools
from util import uniqify
from models import Word, Translation
def vob_split(field, kind='word'):
    if kind == 'word':
        return re.split(r'\xc2\xa0; | ; ', field)
    elif kind == 'category':
        return re.split(r'\. *', field)[:-1]
    else: return field


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

def import_words(listfile):
    with open(listfile, "r") as thai_words:
        new_wordlist = [word.rstrip() for word in thai_words.readlines()]
        load_words(new_wordlist)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    listfile = sys.argv[1]
    print "importing words from " + listfile
    import_words(listfile)
