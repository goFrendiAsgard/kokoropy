from kokoropy import base_url

def default_style():
    url = base_url()
    generated_css = '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/assets/css/bootstrap.min.css">' +\
        '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/css/custom-theme/jquery-ui-1.10.3.custom.css">' +\
        '<!--<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/css/custom-theme/jquery-ui-1.10.3.theme.css">-->' +\
        '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/assets/css/font-awesome.min.css">' +\
        '<!--[if IE 7]>' +\
        '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/assets/css/font-awesome-ie7.min.css">' +\
        '<![endif]-->' +\
        '<!--[if lt IE 9]>' +\
        '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/css/custom-theme/jquery.ui.1.10.3.ie.css">' +\
        '<![endif]-->' +\
        '<link rel="stylesheet" href="' + url + 'assets/jquery-ui-bootstrap/assets/js/google-code-prettify/prettify.css">' +\
        '<link href="' + url + 'assets/jquery-ui-bootstrap/third-party/jQuery-UI-FileInput/css/enhanced.css" rel="Stylesheet">' +\
        '<!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->' +\
        '<!--[if lt IE 9]>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/html5shiv.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/respond.min.js" type="text/javascript"></script>' +\
        '<![endif]-->' +\
        '<!-- Le fav and touch icons -->' +\
        '<link rel="apple-touch-icon-precomposed" sizes="144x144" href="' + url + 'assets/jquery-ui-bootstrap/assets/ico/apple-touch-icon-144-precomposed.png">' +\
        '<link rel="apple-touch-icon-precomposed" sizes="114x114" href="' + url + 'assets/jquery-ui-bootstrap/assets/ico/apple-touch-icon-114-precomposed.png">' +\
        '<link rel="apple-touch-icon-precomposed" sizes="72x72" href="' + url + 'assets/jquery-ui-bootstrap/assets/ico/apple-touch-icon-72-precomposed.png">' +\
        '<link rel="apple-touch-icon-precomposed" href="' + url + 'assets/jquery-ui-bootstrap/assets/ico/apple-touch-icon-57-precomposed.png">'
    return generated_css

def default_script():
    url = base_url()
    generated_script = '<!--[if lt IE 9]>' + \
        '<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>' + \
        '<![endif]-->' + \
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/jquery-1.9.1.min.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/jquery-migrate-1.2.1.min.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/bootstrap.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/holder.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/vendor/jquery-ui-1.10.3.custom.min.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/assets/js/google-code-prettify/prettify.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/third-party/jQuery-UI-FileInput/js/enhance.min.js" type="text/javascript"></script>' +\
        '<script src="' + url + 'assets/jquery-ui-bootstrap/third-party/jQuery-UI-FileInput/js/fileinput.jquery.js" type="text/javascript"></script>' +\
        '<script type="text/javascript">' +\
            'function _mutate_input(){' +\
                '$( "._date-input" ).datepicker({' +\
                    'defaultDate: null,' +\
                    'changeMonth: true,' +\
                    'changeYear: true,' +\
                    'numberOfMonths: 1,' +\
                    'dateFormat: "yy-mm-dd",' +\
                    'yearRange: "c-50:c+50",' +\
                '});' +\
                '$("._file-input").customFileInput({' +\
                    'button_position : "right"' +\
                '});' +\
                '$("._integer-input").spinner();' +\
            '}' + '\n' +\
            '$(document).ready(function(){'+\
                '_mutate_input();' +\
                '$("._new_row").live("click", function(event){' +\
                    '_mutate_input();' +\
                '});' +\
            '});' +\
        '</script>'
    return generated_script

def include_js(path):
    return '<script type="text/javascript" src="' + base_url(path) + '"></script>'

def include_css(path):
    return '<link rel="stylesheet" type="text/css" href="' + base_url(path) + '">'