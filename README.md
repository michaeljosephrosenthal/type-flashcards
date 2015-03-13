Type Flashcards
===============

Utility to practice Thai

to generate a migration based on changes to the models:
`honcho run alembic revision --autogenerate -m "some migration method"`
it should generate some file in `alembic/versions/`, for example:
`alembic/versions/2585aaf880e7_create_update_timestamps_constraints.py`
go in to the file and make sure it's safe/does what you want it to do, then
`honcho run alembic upgrade head` to apply the migration
