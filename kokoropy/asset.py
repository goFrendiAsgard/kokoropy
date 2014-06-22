import os
from bottle import template
from kokoro import file_get_contents, base_url

def _partial(path):
    content = file_get_contents(os.path.join(os.path.dirname(__file__), 'partial_view', path))+'\n'
    return template(content, base_url = base_url())

JQUI_BOOTSTRAP_STYLE    = _partial('jqui_bootstrap_style.html')
JQUI_BOOTSTRAP_SCRIPT   = _partial('jqui_bootstrap_script.html')
KOKORO_CRUD_STYLE       = _partial('kokoro_crud_style.html')
KOKORO_CRUD_SCRIPT      = _partial('kokoro_crud_script.html')

###################################################################################################
# HTML Builder
###################################################################################################
class HTML:
    
    @staticmethod
    def include_js(path):
        return '<script type="text/javascript" src="' + base_url(path) + '"></script>'
    
    @staticmethod
    def include_css(path):
        return '<link rel="stylesheet" type="text/css" href="' + base_url(path) + '">'
    
    @staticmethod
    def tag(tag_type, *args, **kwargs):
        attribute_list = []
        cdata = ''
        # define attributes
        for item in args:
            attribute_list.append(item)
        for key in kwargs:
            val = kwargs[key]
            if key == 'cdata':
                cdata = val
                if isinstance(cdata, list):
                    cdata = ''.join(cdata)
            else:
                if isinstance(val, list):
                    val = ' '.join(val)
                attribute_list.append(key + ' = "'+ str(val) +'"')
        attributes = ' '.join(attribute_list)
        # build html
        if tag_type in ['br', 'hr', 'input', 'img'] and cdata == '':
            html = '<' + tag_type + attributes + ' />'
        else:
            html  = '<' + tag_type + attributes + '>'
            html += cdata
            html += '</' + tag_type + '>'
        return html
    
    @staticmethod
    def input(*args, **kwargs):
        return HTML.tag('input', *args, **kwargs)
    
    @staticmethod
    def button(*args, **kwargs):
        return HTML.tag('button', *args, **kwargs)
    
    @staticmethod
    def textarea(*args, **kwargs):
        return HTML.tag('textarea', *args, **kwargs)
    
    @staticmethod
    def select(*args, **kwargs):
        options = kwargs.pop('options',{})
        cdata = []
        default_value = kwargs.pop('value','')
        for key in options:
            o_args = []
            if key == default_value:
                o_args.append('selected')
            o_kwargs = {'value' : key, 'cdata' : options['key']}
            cdata.append(HTML.tag('option', *o_args, **o_kwargs))
        return HTML.tag('select', *args, **kwargs)
    
    @staticmethod
    def text_input(*args, **kwargs):
        kwargs['type'] = 'text'
        return HTML.input(*args, **kwargs)
    
    @staticmethod
    def hidden_input(*args, **kwargs):
        kwargs['type'] = 'hidden'
        return HTML.input(*args, **kwargs)
    
    @staticmethod
    def password_input(*args, **kwargs):
        kwargs['type'] = 'password'
        return HTML.input(*args, **kwargs)