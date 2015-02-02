begin;
--for local munging and inspection
create table volubilis_raw (
    THAIROM varchar,
    EASYTHAI varchar,
    ETYMO varchar,
    THAIPHON varchar,
    TH varchar,
    FR varchar,
    EN varchar,
    TYPE varchar default null,
    USAGE varchar default null,
    SCIENT varchar default null,
    PRONUN varchar default null,
    CLASSIF varchar default null,
    DOM varchar default null
);
copy volubilis_raw from '/Users/mjr/Documents/code/type-flashcards/volubilis.tsv' with csv header delimiter E'\t' quote E'\b';
create table basic_card (thai varchar, eng varchar);
  copy(select distinct on (w2.text) word.text, w2.text, word.category from word join translation on (word.id = translation.word_a_id or word.id = translation.word_b_id) join word w2 on (w2.id = translation.word_a_id or w2.id = translation.word_b_id) where word.lang = 'eng' and w2.lang = 'thai' and word.category ilike '%v.%' order by w2.text, length(word.text) asc) to stdout delimiter ';'
;
SELECT word.text AS word_text,
    word_1.text AS word_1_text,
    translation.score AS translation_score
FROM word JOIN translation
    ON word.id = translation.word_a_id OR word.id = translation.word_b_id
JOIN word AS word_1
    ON translation.word_a_id = word_1.id OR translation.word_b_id = word_1.id
JOIN wordlistitem
    ON translation.id = wordlistitem.translation_id
JOIN wordlist
    ON wordlist.id = wordlistitem.wordlist_id
WHERE wordlist.name = :name_1 AND word.lang = :lang_1 AND word_1.lang = :lang_2 ORDER BY translation.score DESC
end;
