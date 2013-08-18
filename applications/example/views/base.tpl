<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="stylesheet" type="text/css" href="{{ BASE_URL }}assets/static_libraries/bootstrap/css/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="{{ BASE_URL }}assets/example/css/style.css" />
        <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
        <!--[if lt IE 9]>
          <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
        <![endif]-->
        <style type="text/css">
            div#layout-content {
                min-height: 250px;
                background-repeat: no-repeat;
                background-image:url('{{ BASE_URL }}assets/example/images/programmer.png');
                background-position: bottom right;
            }
        </style>
        <script type="text/javascript" src="{{ BASE_URL }}assets/static_libraries/jquery.tools.min.js"></script>
        <script type="text/javascript" src="{{ BASE_URL }}assets/static_libraries/bootstrap/js/bootstrap.min.js"></script>
        <script type="text/javascript" src="{{ BASE_URL }}assets/example/js/script.js"></script>
        <title>{{ title or 'Kokoropy' }}</title>
    </head>
    <body>
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar">&nbsp;</span>
                        <span class="icon-bar">&nbsp;</span>
                        <span class="icon-bar">&nbsp;</span>
                    </button>
                    <a class="brand" href="#">Kokoropy</a>
                    <div class="nav-collapse collapse">
                        <ul class="nav">
                            <li><a href="{{ BASE_URL }}example/simple/hello_world">Simple route</a></li>
                            <li><a href="{{ BASE_URL }}example/recommended/index">Recommended route</a></li>
                            <li><a href="{{ BASE_URL }}example/advance/hello">Advance route</a> </li>
                            <li><a href="{{ BASE_URL }}example/recommended/pokemon">Database</a></li>
                            <li><a href="{{ BASE_URL }}example/recommended/upload">Test upload file</a></li>
                            <li><a href="{{ BASE_URL }}example/plotting/index">Matplotlib</a></li>
                        </ul>
                    </div><!--/.nav-collapse -->
                </div>
            </div>
        </div>

        <div id="content-container" class="container">
            <div class="row-fluid">
                <div id="layout-banner" class="well hidden-phone span12">
                    <div class="span2">
                        <img src ="{{ BASE_URL }}assets/images/kokoropy.png" />
                    </div>
                    <div class="span10">
                        <h1>Kokoropy</h1>
                        <p>心から Educational MVC Python Web Framework</p>
                    </div>
                </div>
                <div id="layout-content" class="span12">
                    <p id="content">                       
                        %include
                    </p>
                </div><!--/#layout-content-->
            </div><!--/row-->
            <hr>
            <footer>GoFrendiAsgard &copy; 2013</footer>
        </div><!--/.fluid-container-->

    </body>
</html>