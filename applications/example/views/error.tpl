<head>
    <link rel="stylesheet" type="text/css" href="{{ BASE_URL }}assets/static_libraries/bootstrap/css/bootstrap.min.css" />
    <style>
        body{
            color: white;
            background-color:#555;
            padding-top: 5px;
            padding-left: 20px;
            padding-right: 20px;
        }
        div#error-container{
            background-repeat: no-repeat;
            background-image:url('{{ BASE_URL }}assets/example/images/programmer.png');
            background-position: bottom right;
            min-height: 70%;
            min-width: 100%;
        }
        footer{
            font-size:small;
        }
        #error-title{
            margin-bottom: 30px;
        }
        #error-message{
            margin-bottom: 30px;
            padding: 30px;
        }
        #goback-message{
            font-size: 20;
            padding: 10px;
        }
        #error-title, #error-message, #goback-message{
            max-width: 70%;
        }
        div#layout-banner{
            margin-top: 10px;
            background-color:#222;
            border:none;
        }
    </style>
    <title>{{ data['error_title'] }}</title>
</head>
<body>
    <div id="error-container">
        <div id="layout-banner" class="well">
            <h1 id="error-title">{{ data['error_title'] }}</h1>
        </div>
        <h2 id="error-message">{{ data['error_message'] }}</h2>
        <p id="goback-message">Nothing you can do here. So just <a class="btn btn-primary" href="/"><strong>go back</strong></a> and forget what you've see</p>
    </div>
    <footer>This cool error message is provided by kokoropy. &copy; GoFrendiAsgard, 2013</footer>
</body>