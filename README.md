Type Flashcards
===============

Utility to practice Thai

Dev setup is done with [vagrant](http://www.vagrantup.com/downloads.html). 
After installing vagrant, `cd vagrant/local; vagrant up` should install the development VM, provision the database, and populate it with the test data in `./dat/`. After this completes run the following to start the server:

```
vagrant ssh 
source venv/bin/activate
cd /type-flashcards/
honcho start web
```
the Bottle app should now be `Listening on http://0.0.0.0:5000/`, which means you can go to `localhost:5000` to see it. This directory (`type-flashcards`) is shared between the host machine and the vagrant VM from the root directory, which, in tandem with Bottle's development mode's code reloading, means any changes to the app you make locally will be automatically applied to the running application.

The VM does not currently `gulp` for you. You'll have to go into `./scripts` locally and run `gulp` if you want live-reloading less.

To generate a migration based on changes to the models:
`honcho run alembic revision --autogenerate -m "some migration method"`
it should generate some file in `alembic/versions/`, for example:
`alembic/versions/2585aaf880e7_create_update_timestamps_constraints.py`
go in to the file and make sure it's safe/does what you want it to do, then
`honcho run alembic upgrade head` to apply the migration
