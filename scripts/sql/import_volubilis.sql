begin;
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
end;
