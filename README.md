Kokoropy
=========

A 心から Educational MVC Python Web Framework.

In japanese, kokoro means heart.
I make Kokoropy because I can not find any python web-framework which I really comfort with.
Some are too verbose, while some others have too many "magic". Most of them force me to learn about the framework, and do not allow me to directly focus on my job.
Basically I expect an easy-to-use framework like CodeIgniter (with more features) in python.

If you are in the same boat with me, then kokoropy is also for you.

Kokoropy is built in top of Bottle.py (http://bottlepy.org/docs/dev/), a very great python micro-web-framework.
While bottle.py focus on how to make things as simple as possible, kokoropy focus on how to make things as easy as possible.

Kokoropy is built based on my experiences with some framework. Here are some comparison between kokoropy and other framework

* Kokoropy is explicit & transparent. There is no magic in kokoropy. If you need something, you need to import it.
* You can use route directive just like in `bottle.py` (http://bottlepy.org), since bottle.py is the core of kokoropy.
* Kokoropy is built based on HMVC pattern. You can make unlimited number of separated MVC triad. This is good to make your application maintainable.
* Kokoropy doesn't have any other dependencies beside python-standard-library. You can even run it without Apache or nginx.
* Kokoropy support many database system. Every model can has its own database.
* Kokoropy support REST.
* Kokoropy support both, automatic and manual routing.
* Kokoropy support SESSION and COOKIES out of the box

__PS:__ This is my pet-project, and might be not stable. It is not ready for production purpose (yet)

Kokoropy stands in the shoulder of the giants. Here are projects that make kokoropy possible:
* bottlepy 0.12 dev (https://github.com/defnull/bottle)
* sqlalchemy 0.9.0 dev (https://github.com/zzzeek/sqlalchemy)
* beaker 1.6.4 (https://github.com/bbangert/beaker)
* alembic
* jinja2

Also, kokoropy come with several third-party css & javascript framework (so you do not need to download them anymore):
* jquery 1.11.0
* jquery-ui 1.10.4
* jquery-mobile 1.4.0
* bootstrap 3.0.3
* colorbox 1.4.33
* chosen 1.0.0
* leaflet 0.7.2
* alertify.js 0.3.1.1
* jquery-ace 1.0.3

Documentation & Demo
====================
http://kokoropy.herokuapp.com

Who Kokoropy is for?
====================

Kokoropy is for you if you:

* Already familiar with PHP framework such as CodeIgniter but want to move to Python.
* Want to have a "educational" web framework that can be run everywhere.
* Desire explicity of framework, so that popular IDE such as eclipse can help in auto-completion (intellisense).
* Don't like complicated framework, you want a framework with small learning steep.

Change Log:
===========
* Provide `base_url` setting (done, tested, 2013/08/08)
* In debugging session (via `python start.py`), auto reload server when something changed (done, tested, 2013/08/08)
* Add request.BASE_URL to every view & link in the example (done, tested, 2013/08/09)

TODO:
====
* Make CRUD generator

Credits:
========
* Marcel Hellkamp (defnull): creator of bottlepy
* Rully Ramanda: Introducing relative import to me :)
* Creator of sqlalchemy, jquery, and anyone who let me make kokoropy easier
