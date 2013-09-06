from kokoropy import route, base_url, template, remove_trailing_slash

# modify this file as you want
@route('/')
@route(remove_trailing_slash(base_url()))
@route(base_url())
def index():    
    # return string
    return template('index/index.tpl')
    html_response  = '<title>Kokoropy</title>'
    html_response += '<h1>It works. The kokoropy is running well as expected !!!</h1>'
    html_response += 'Now, <a href="'+base_url('example/recommended')+'">Check the examples</a> or <a href="https://github.com/goFrendiAsgard/kokoropy">Check the tutorials</a>'
    return html_response