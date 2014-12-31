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