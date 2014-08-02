NomosDB is a database for any institution working in the education sector. It arose from practical difficulties in my work as a Lecturer in the Law Department at Canterbury Christ Church University, but its ultimate aim is to be usable (and used) by Universities, FE colleges, schools and other educational institutions

# Aims

This project has been started by a lecturer in law, who also happens to be an open source enthusiast and a hobby programmer ([more here](http://www.tobiaskliem.de)). In my day job I realised that almost every university seems to rely on horribly complicated proprietary database systems that were not designed with the teacher in mind. This results in most of the data management being done by the teachers themselves on their own computers - in the form of the worst menace to humankind: spreadsheets.

Almost every teacher knows the problem of having a folder on their computer (or, even more often, on their Desktop) with a variety of spreadsheets in it that are difficult to distinguish: accounting101-marks.xls, accounting101-marks-final.xls, accounting101-marks-latest.xls accounting101-marks-corrected-version.xls and so on. Depending on the institution, this can go on like this for attendance, tutorial notes and so on.

This is were NomosDB comes in: the NO MOre Spreadsheets DataBase. Instead of having a variety of unconnected spreadsheets on each teachers computer and an illegible and unusable commercial University database solution programmed in 1986 by people that hate their lives, NomosDB helps to have an easy to use database structure that helps teachers and admin staff to focus on their real jobs.

The aim of this system is to have an easy to use database application that relies on open standards and makes it very easy to get the data out in machine readable formats should the user want to switch after all. Currently, almost everything is exportable in pretty PDF files, but soon it should be easy to get your data in csv and json files as well, so that even a typical, non-technical teacher can save a backup they can open with Microsoft Excel or similar soul-destroying applications.

This application is not trying to be a huge Virtual Learning Environment that allows you to post slides, videos, upload assessments or let the students create Wikis. Instead, it is supposed to stay focused on its main goal - to make the teacher's life easier by automating repetetive tasks, offering a quick way to access records for modules and students and a simple solution to share assessment feedback and marks with the students.

<!---
# Installation

The database is based on [Django](http://www.djangoproject.org), a very versatile webframework based on Python. You will need the following dependencies:

* Python (version 3.x) and the Python-markdown package (available in most Linux distributions)
* [Django](http://www.djangoproject.org)
* Apache (or any other webserver you want to use, but I haven't tested with anything else)
* SQLite or any other database that works with Django, in case you want to use anything else, you need to adapt `nomosdb/settings.py`
* [Reportlab](http://www.reportlab.com/software/opensource/) for generating PDF files

Once you have all of that, get the repository, set up your initial database with `python manage.py syncdb`, create a superuser during that process if you want to, and you are ready to go. You can start the testserver with `python manage.py runserver`, and you can access the website itself over `localhost:8000` and the Django admin interface over `localhost:8000/admin`.

By default, there already is a superuser set up, and you can access both the website itself and the admin interface with the username `admin` and the password `admin`. Don't forget to change the password or delete that user later!

If you want to use this in production, you will need to run `python manage.py collectstatic`, and to set up your webserver to display the website and to deliver the static files (CSS, Javascript, pictures etc). There are loads of guides on how to do configure whichever webserver you want to use with Django ([for example this one for Apache](https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/)).

This project is still a work in progress, so if you want to use it for production, make sure you have lots of backups...

# Outstanding Tasks

* TESTS, TESTS, TESTS!
* making the application easier to adapt for other institutions and programmes
* making sure the templates are mobile responsive, so that the application can be used on phones
* exporting data into machine-readable formats: csv, json, etc
* clean up my potentially awful (hobby programmer) coding style, ask me to add comments where you don't understand the functions etc

If you find any problems or bugs, or if you have any questions, use the issues form here or contact me at [tobi@tobiaskliem.de](mailto:tobi@tobiaskliem.de).

--->
