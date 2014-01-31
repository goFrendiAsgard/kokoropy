# Visit https://devcenter.heroku.com/articles/python

# get and install heroku toolbelt
# wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

# init a git repo
git init

# login to heroku (make sure you already have an account on heroku.com)
heroku login

# if need scipy etc, we should use a buildpack
heroku create --buildpack https://github.com/dbrgn/heroku-buildpack-python-sklearn/

# if you already make an heroku app without specifying buildpack, please don't worry, use this command
# heroku config:set BUILDPACK_URL=https://github.com/dbrgn/heroku-buildpack-python-sklearn/

# make heroku_app.py installable
chmod a+x heroku_app.py

# make Procfile to run heroku_app.py
echo "web: python heroku_app.py" > Procfile

# make runtime.txt
echo "python-2.7.4" > runtime.txt

# detect all changes and deploy by using commit & push
git add . -A
git commit -m "Initial commit for heroku deployment"
git push heroku master
