Tic tac toe code challenge
==========================

This basic Django app implements an AI tic-tac-toe player who will not lose.

To play, to go [saytheidea.org/tictactoe](http://saytheidea.org/tictactoe).

Code
----
Written with Django 1.2.3. Uses [django-picklefield](http://djangopackages.com/packages/p/django-picklefield/) to store game state in a SQLite3 database.

Deployment
----------
Running on gunicorn behind ngnix on a personal rackspace instance.

Design
------
All style is CSS. No javascript at all.

Attribution
-----------
All of the code and design is my original work. I do, however, cite a stackoverflow post on tic-tac-toe algorithms that gave me the hint I needed to finish my code.

Bonus
-----
The game is more or less playable in w3m from the commandline.
