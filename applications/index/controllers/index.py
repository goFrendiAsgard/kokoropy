from kokoropy import route, base_url, template, remove_trailing_slash

# modify this file as you want
@route('/')
@route(remove_trailing_slash(base_url()))
@route(base_url())
def index():    
    # return string
    return template('index/index.tpl')