<!DOCTYPE html>
<html>
    <head>
        <link rel="icon" href="{{BASE_URL}}index/assets/index/favicon.ico" />
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="stylesheet" type="text/css" href="{{ BASE_URL }}index/assets/static_libraries/bootstrap-3.0.0/css/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="{{ BASE_URL }}example/assets/css/style.css" />        
        <style type="text/css">        
            #layout-content {
                min-height: 250px;
                background-repeat: no-repeat;
                background-color:rgba(100, 100, 100, 0.1);
                padding:10px;
                border-radius: 10px;
            }
        </style>              
        <title>{{ title or 'Kokoropy' }}</title>
    </head>
    <body>
        <!-- Menu -->
        <div class="navbar navbar-inverse navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="icon-bar">&nbsp;</span>
                <span class="icon-bar">&nbsp;</span>
                <span class="icon-bar">&nbsp;</span>
              </button>
              <a class="navbar-brand" href="#">Kokoropy</a>
            </div>
            <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="{{ BASE_URL }}example/recommended/pokemon">Database &amp; Upload Demo</a></li>
                <li><a href="{{ BASE_URL }}example/plotting/index">Matplotlib Demo</a></li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown">Session &amp; Routing Demo<b class="caret">&nbsp;</b></a>
                  <ul class="dropdown-menu">
                    <li><a href="{{ BASE_URL }}example/simple/hello_world">Simple</a></li>
                    <li><a href="{{ BASE_URL }}example/recommended/index">Recommended (use this)</a></li>
                    <li><a href="{{ BASE_URL }}example/advance/hello">Advance</a> </li>
                  </ul>
                </li>
              </ul>
              <form class="navbar-form navbar-right" action="{{ BASE_URL }}example/recommended/pokemon" method="get">
                <div class="form-group">
                  <input type="text" placeholder="Pokemon name" name="keyword" class="form-control">
                </div>
                <button type="submit" class="btn btn-success">Search</button>
              </form>
            </div><!--/.navbar-collapse -->
          </div>
        </div>
        
        <!-- Github ribbon -->
        <a href="https://github.com/goFrendiAsgard/kokoropy"><img style="position: absolute; top: 40px; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_orange_ff7600.png" alt="Fork me on GitHub"></a>
       
        <!-- Jumbotron -->
        <div class="jumbotron hidden-phone">
          <div class="container">
            <div class="col-md-2">
                <img src ="{{ BASE_URL }}index/assets/images/kokoropy.png" />
            </div>
            <div class="col-md-10">
                <h1>Kokoropy</h1>
                <p>心から Educational MVC Python Web Framework</p>
            </div>
          </div>
        </div>
        
        
        <div class="container">
            <!-- content -->
            <div  id="layout-content">
                <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
                <!--[if lt IE 9]>
                  <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
                <![endif]-->
                <script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/jquery-2.0.3.min.js"></script>
                <script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/bootstrap-3.0.0/js/bootstrap.min.js"></script>
                <script type="text/javascript" src="{{ BASE_URL }}example/assets/js/script.js"></script>
                % setdefault('base', 'nothing')  
                {{!base}}
            </div>
            
            <!-- footer -->
            <hr>              
            <footer>
              <p>&copy; Go Frendi Gunawan 2013</p>
            </footer>
        </div>        
    </body>
</html>
