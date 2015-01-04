
def presented_html_code(script):
    return script.replace('<','&lt;').\
        replace('>','&gt;').\
        replace(' ','&nbsp;').\
        replace('\r\n','<br />').\
        replace('\n','<br />')

def include_js(path):
    return '<script type="text/javascript" src="' + base_url(path) + '"></script>'


def include_css(path):
    return '<link rel="stylesheet" type="text/css" href="' + base_url(path) + '">'


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
    if new_class != '':
        if 'class' in kwargs:
            if isinstance(kwargs['class'], list):
                kwargs['class'].append[new_id]
            else:
                kwargs['class'] += ' ' + new_id
        else:
            kwargs['class'] = new_class
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
        html = '<' + tag_type + ' ' + attributes + ' />'
    else:
        html  = '<' + tag_type + ' ' + attributes + '>'
        html += children
        html += '</' + tag_type + '>'
    return html

def _extract_args(args, output_length, default_val=[]):
    output = []
    for i in range(output_length):
        default = default_val[i] if len(default_val) >= i+1 else ''
        output.append(default)
    i, j = -1, 0
    while j< min(len(args), output_length):
        output[i] = args[i]
        i, j = i-1, j+1
    new_args = []
    for i in range(output_length,len(args)):
        new_args.append(i)
    return (output, new_args)

def _simple_tag(tag_type, *args, **kwargs):
    '''
    usage:
    _simple_tag(tag_type, selector, **kwargs)
    _simple_tag(tag_type, selector, children, *args, **kwargs)
    '''
    ((selector, kwargs['children']), args) = _extract_args(args, 2)
    return tag(tag_type + selector, *args, **kwargs)

def _simple_input(tag_type, *args, **kwargs):
    '''
    usage:
    _simple_input(tag_type, name, **kwargs)
    _simple_input(tag_type, selector, name, **kwargs)
    _simple_input(tag_type, selector, name, value, **kwargs)
    _simple_input(tag_type, selector, name, value, placeholder, *args, **kwargs)
    '''
    if len(args) == 1:
        ((kwargs['name']), args) = _extract_args(args, 1)
        selector = ''
    elif len(args) == 2:
        ((selector, kwargs['name']), args) = _extract_args(args, 2)
    elif len(args) == 3:
        ((selector, kwargs['name'], kwargs['value']), args) = _extract_args(args, 3)
    else:
        ((selector, kwargs['name'], kwargs['value'], kwargs['placeholder']), args) = _extract_args(args, 4)
    return tag(tag_type + selector, *args, **kwargs)

def button(*args, **kwargs):
    ''' 
    usage:
    button(name, **kwargs)
    button(selector, name, **kwargs)
    button(selector, name, value, **kwargs)
    button(selector, name, value, placeholder, *args, **kwargs)

    example:
    button('#save.btn.btn-default', 'save', 'Save the data')

    produce:
    <button id="save" class="btn btn-default" name="save">Save the data</button>
    '''
    if len(args) == 1:
        ((kwargs['name']), args) = _extract_args(args, 1)
        selector = ''
    elif len(args) == 2:
        ((selector, kwargs['name']), args) = _extract_args(args, 2)
    else:
        ((selector, kwargs['name'], kwargs['children']), args) = _extract_args(args, 3)
    return tag('button' + selector, *args, **kwargs)


def textarea(*args, **kwargs):
    ''' 
    usage:
    textarea(name, **kwargs)
    textarea(selector, name, **kwargs)
    textarea(selector, name, value, **kwargs)
    textarea(selector, name, value, placeholder, *args, **kwargs)

    example:
    textarea('.richtext', 'data', 'Some HTML')

    produce:
    <textarea class="richtext" name="data">Some HTML</textarea>
    '''
    if len(args) == 1:
        ((kwargs['name']), args) = _extract_args(args, 1)
        selector = ''
    elif len(args) == 2:
        ((selector, kwargs['name']), args) = _extract_args(args, 2)
    elif len(args) == 3:
        ((selector, kwargs['name'], kwargs['children']), args) = _extract_args(args, 3)
    else:
        ((selector, kwargs['name'], kwargs['children'], kwargs['placeholder']), args) = _extract_args(args, 4)
    return tag('textarea' + selector, *args, **kwargs)


def select(*args, **kwargs):
    ''' 
    usage:
    select(name, **kwargs)
    select(selector, name, **kwargs)
    select(selector, name, options, **kwargs)
    select(selector, name, options, value, **kwargs)
    select(selector, name, options, value, multiple, *args, **kwargs)

    example:
    select('#color', 'favcolor', {'r':'red', 'g':'green', 'b':'blue'}, 'b')
    produce:
    <select id="color" name="favcolor">
        <option value="r">red</option>
        <option value="g">green</option>
        <option value="b" selected>blue</option>
    </select>

    another example:
    select('#color', 'favcolor', {'r':'red', 'g':'green', 'b':'blue'}, ['r','b'], True)
    produce:
    <select id="color" name="favcolor" multiple>
        <option value="r" selected>red</option>
        <option value="g">green</option>
        <option value="b" selected>blue</option>
    </select>
    '''
    if len(args) == 1:
        ((kwargs['name']), args) = _extract_args(args, 1)
        selector = ''
    elif len(args) == 2:
        ((selector, kwargs['name']), args) = _extract_args(args, 2)
    elif len(args) == 3:
        ((selector, kwargs['name'], kwargs['options']), args) = _extract_args(args, 3)
    elif len(args) == 4:
        ((selector, kwargs['name'], kwargs['options'], kwargs['value']), args) = _extract_args(args, 4)
    else:
        ((selector, kwargs['name'], kwargs['options'], kwargs['value'], kwargs['multiple']), args) = _extract_args(args, 5)
    
    options = kwargs.pop('options',{})
    multiple = kwargs.pop('multiple', False)
    if multiple:
        args.append('multiple')
    default_value = [] if multiple else ''
    default_value = kwargs.pop('value', default_value)

    # prepare children
    children = []
    if multiple:
        for val in default_value:
            children.append(tag('option', 'selected', value = val, children =  options[val]))
    # create option
    for key in options:
        o_args = []
        # add selected attribute. If it is multiple, selected option has been previously added, so
        # it is no need to add it again
        if multiple and (key in default_value):
            continue
        elif key == default_value:
            o_args.append('selected')
        # add other attributes
        o_kwargs = {'value' : key, 'children' : options[key]}
        # add option
        children.append(tag('option', *o_args, **o_kwargs))
    kwargs['children'] = children
    # return    
    return tag('select'+selector, *args, **kwargs)

def title(*args, **kwargs):
    ''' 
    usage:
    title('hello world')

    produce:
    <title>hello world</title>
    '''
    return _simple_tag('title', *args, **kwargs)


def head(*args, **kwargs):
    ''' 
    usage:
    head(title('hello world'))

    produce:
    <head><title>hello world</title></head>
    '''
    return _simple_tag('head', *args, **kwargs)


def body(*args, **kwargs):
    ''' 
    usage:
    body('hello world')

    produce:
    <body>hello world</body>
    '''
    return _simple_tag('body', *args, **kwargs)


def div(*args, **kwargs):
    ''' 
    usage:
    div('#content.col-md-6.col-xs-4', 'hello world')

    produce:
    <div id="content" class="col-md-6 col-xs-4">hello world</div>
    '''
    return _simple_tag('div', *args, **kwargs)


def span(*args, **kwargs):
    ''' 
    usage:
    span('#content.col-md-6.col-xs-4', 'hello world')

    produce:
    <span id="content" class="col-md-6 col-xs-4">hello world</span>
    '''
    return _simple_tag('span', *args, **kwargs)


def h1(*args, **kwargs):
    ''' 
    usage:
    h1('hello world')

    produce:
    <h1>hello world</h1>
    '''
    return _simple_tag('h1', *args, **kwargs)


def h2(*args, **kwargs):
    ''' 
    usage:
    h2('hello world')

    produce:
    <h2>hello world</h2>
    '''
    return _simple_tag('h2', *args, **kwargs)


def h3(*args, **kwargs):
    ''' 
    usage:
    h3('hello world')

    produce:
    <h3>hello world</h3>
    '''
    return _simple_tag('h3', *args, **kwargs)


def h4(*args, **kwargs):
    ''' 
    usage:
    h4('hello world')

    produce:
    <h4>hello world</h4>
    '''
    return _simple_tag('h4', *args, **kwargs)


def br(count = 1, *args, **kwargs):
    ''' 
    usage:
    br()
    br(count, args, **kwargs)

    example:
    br()
    produce:
    <br />

    another example:
    br(5)
    produce:
    <br /><br /><br /><br /><br />
    '''
    result, i = '', 0
    while i < count:
        result += tag('br', *args, **kwargs)
    return result


def hr(count = 1, *args, **kwargs):
    ''' 
    usage:
    hr()
    hr(count, *args, **kwargs)

    example:
    hr()
    produce:
    <hr />

    another example:
    hr(5)
    produce:
    <hr /><hr /><hr /><hr /><hr />
    '''
    result, i = '', 0
    while i < count:
        result += tag('hr', *args, **kwargs)
    return result


def general_input(*args, **kwargs):
    '''
    usage:
    general_input(name, **kwargs)
    general_input(selector, name, **kwargs)
    general_input(selector, name, value, **kwargs)
    general_input(selector, name, value, placeholder, **kwargs)

    example:
    general_input('#field-name.form-control', 'name', 'Gandalf', 'Your Name', type="text")

    produce:
    <input id="field-name" class="form-control" name="name" type="text" placeholder="Your Name" value="Gandalf" />
    '''
    return _simple_input('input', *args, **kwargs)


def input_text(*args, **kwargs):
    '''
    usage:
    input_text(name, **kwargs)
    input_text(selector, name, **kwargs)
    input_text(selector, name, value, **kwargs)
    input_text(selector, name, value, placeholder, **kwargs)

    usage:
    input_text('#field-name.form-control', 'name', 'Gandalf', 'Your Name')

    produce:
    <input id="field-name" class="form-control" name="name" type="text" placeholder="Your Name" value="Gandalf" />
    '''
    kwargs['type'] = 'text'
    return general_input(*args, **kwargs)


def input_hidden(*args, **kwargs):
    kwargs['type'] = 'hidden'
    return general_input(*args, **kwargs)


def input_password(*args, **kwargs):
    kwargs['type'] = 'password'
    return general_input(*args, **kwargs)


def input_file(*args, **kwargs):
    kwargs['type'] = 'file'
    return general_input(*args, **kwargs)

def input_checkbox(*args, **kwargs):
    '''
    usage:
    input_checkbox(name, **kwargs)
    input_checkbox(selector, name, **kwargs)
    input_checkbox(selector, name, value, **kwargs)
    input_checkbox(selector, name, value, checked, *args, **kwargs)
    '''
    kwargs['type'] = 'checkbox'
    if len(args) == 1:
        ((kwargs['name']), args) = _extract_args(args, 1)
        selector = ''
    elif len(args) == 2:
        ((selector, kwargs['name']), args) = _extract_args(args, 2)
    elif len(args) == 3:
        ((selector, kwargs['name'], kwargs['value']), args) = _extract_args(args, 3)
    else:
        ((selector, kwargs['name'], kwargs['value'], checked), args) = _extract_args(args, 4)
        if checked:
            args.append('checked')
    return tag('input' + selector, *args, **kwargs)


def a(*args, **kwargs):
    '''
    usage:
    a(children)
    a(href, children)
    a(selector, href, children)
    '''
    ((selector, kwargs['href'], kwargs['children']), args) = _extract_args(args, 3, ['', '#', ''])
    return tag('a'+selector, *args, **kwargs)

def a_name(*args, **kwargs):
    '''
    usage:
    a_name(children)
    a_name(name, children)
    a_name(selector, name, children)
    '''
    ((selector, kwargs['name'], kwargs['children']), args) = _extract_args(args, 3)
    return tag('a'+selector, *args, **kwargs)


def img(*args, **kwargs):
    '''
    usage:
    img(src)
    img(selector, src)
    '''
    ((selector, kwargs['src']), args) = _extract_args(args, 2)
    return tag('img'+selector, *args, **kwargs)

def table(*args, **kwargs):
    return _simple_tag('table', *args, **kwargs)

def thead(*args, **kwargs):
    return _simple_tag('thead', *args, **kwargs)

def tbody(*args, **kwargs):
    return _simple_tag('tbody', *args, **kwargs)

def tfoot(*args, **kwargs):
    return _simple_tag('tfoot', *args, **kwargs)

def tr(*args, **kwargs):
    return _simple_tag('tr', *args, **kwargs)

def td(*args, **kwargs):
    return _simple_tag('td', *args, **kwargs)

def th(*args, **kwargs):
    return _simple_tag('th', *args, **kwargs)

def label(*args, **kwargs):
    return _simple_tag('label', *args, **kwargs)

def ul(*args, **kwargs):
    return _simple_tag('ul', *args, **kwargs)

def ol(*args, **kwargs):
    return _simple_tag('ol', *args, **kwargs)

def li(*args, **kwargs):
    return _simple_tag('li', *args, **kwargs)