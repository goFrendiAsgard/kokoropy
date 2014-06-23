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
        # override kwargs if selector is used as tag_type
        status = ''
        new_tag_type = ''
        new_id = ''
        new_class = ''
        for char in tag_type:
            if char == '#':
                if new_id != '':
                    new_id += ' '
                status = '#'
            elif char == '.':
                if new_class != '':
                    new_class += ' '
                status = '.'
            elif status == '':
                new_tag_type += char
            elif status == '#':
                new_id += char
            elif status == '.':
                new_class += char
        # by default, tag type should be div
        if new_tag_type == '':
            new_tag_type = 'div'
        new_tag_type = new_tag_type.replace(' ', '')
        # override tag_type
        tag_type = new_tag_type
        # override kwargs['id']
        if new_id != '':
            if 'id' in kwargs:
                if isinstance(kwargs['id'], list):
                    kwargs['id'].append[new_id]
                else:
                    kwargs['id'] += ' ' + new_id
            else:
                kwargs['id'] = new_id
        # override kwargs['class']
        if new_id != '':
            if 'id' in kwargs:
                if isinstance(kwargs['class'], list):
                    kwargs['class'].append[new_id]
                else:
                    kwargs['class'] += ' ' + new_id
            else:
                kwargs['class'] = new_id
        # define attribute list & children based on args & kwargs
        attribute_list = []
        children = ''
        # define attributes
        for item in args:
            attribute_list.append(item)
        for key in kwargs:
            val = kwargs[key]
            if key == 'children':
                children = val
                if isinstance(children, list):
                    children = ''.join(children)
            else:
                if isinstance(val, list):
                    val = ' '.join(val)
                if val is None:
                    val = ''
                val = str(val)
                attribute_list.append(key + ' = "'+ str(val) +'"')
        attributes = ' '.join(attribute_list)
        # build html
        if tag_type in ['br', 'hr', 'input', 'img'] and children == '':
            html = '<' + tag_type + attributes + ' />'
        else:
            html  = '<' + tag_type + attributes + '>'
            html += children
            html += '</' + tag_type + '>'
        return html
    
    @staticmethod
    def input(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['name'] = args[0]
        if len(args) > 1:
            kwargs['value'] = args[1]
        if len(args) > 2:
            kwargs['placeholder'] = args[2]
        return HTML.tag('input'+selector, *args, **kwargs)
    
    @staticmethod
    def button(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['name'] = args[0]
        if len(args) > 1:
            kwargs['children'] = args[1]
        if len(args) > 2:
            kwargs['placeholder'] = args[2]
        return HTML.tag('button'+selector, *args, **kwargs)
    
    @staticmethod
    def textarea(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['name'] = args[0]
        if len(args) > 1:
            kwargs['children'] = args[1]
        if len(args) > 2:
            kwargs['placeholder'] = args[2]
        return HTML.tag('textarea'+selector, *args, **kwargs)
    
    @staticmethod
    def select(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['name'] = args[0]
        options = kwargs.pop('options',{})
        children = []
        default_value = kwargs.pop('value','')
        for key in options:
            o_args = []
            if key == default_value:
                o_args.append('selected')
            o_kwargs = {'value' : key, 'children' : options['key']}
            children.append(HTML.tag('option', *o_args, **o_kwargs))
        kwargs['children'] = children
        return HTML.tag('select'+selector, *args, **kwargs)
    
    @staticmethod
    def text_input(selector, *args, **kwargs):
        kwargs['type'] = 'text'
        return HTML.input(selector, *args, **kwargs)
    
    @staticmethod
    def hidden_input(selector, *args, **kwargs):
        kwargs['type'] = 'hidden'
        return HTML.input(selector, *args, **kwargs)
    
    @staticmethod
    def password_input(selector, *args, **kwargs):
        kwargs['type'] = 'password'
        return HTML.input(selector, *args, **kwargs)
    
    @staticmethod
    def a(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['href'] = args[0]
        if len(args) > 1:
            kwargs['children'] = args[1]
        return HTML.tag('a'+selector, *args, **kwargs)
    
    @staticmethod
    def img(selector, *args, **kwargs):
        if len(args) > 0:
            kwargs['src'] = args[0]
        return HTML.tag('img'+selector, *args, **kwargs)