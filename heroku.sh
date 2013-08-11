# taken from https://gist.github.com/defnull/1224387 with some changes
# also visit https://devcenter.heroku.com/articles/python

wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

virtualenv --no-site-packages env
source env/bin/activate
pip install gunicorn
pip freeze > requirements.txt
 
chmod a+x heroku_app.py

echo "web: python heroku_app.py" > Procfile

heroku login
 
git init
git add . -A
git commit -m "Initial commit for heroku deployment"
 
heroku create
git push heroku master
