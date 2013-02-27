<head>
    <style>
        body{
            color: white;
            background-color:#555;
            padding-left: 50px;
            padding-top: 20px;        
        }
        div#error-container{        
            background-repeat: no-repeat;
            background-image:url('/index/images/programmer.png');        
            background-position: bottom right;
            min-height: 70%;
            min-width: 100%px;
            display: block;
        }
        a{
            color:white;
            text-decoration:none;
            font-size: 35;
        }
        footer{
            font-size:small;
        }
        h1#error-title{
            font-size:70;
            font-family: ubuntu, 'Lucida Grande', 'Lucida Sans Unicode', Lucida, Arial, Helvetica,;
            max-width:70%;
        }
        p#error-message{
            font-size:40;
            font-family: ubuntu, 'Lucida Grande', 'Lucida Sans Unicode', Lucida, Arial, Helvetica,;
            max-width:70%;            
        }
        p#goback-message{
            font-size:30;
            font-family: ubuntu, 'Lucida Grande', 'Lucida Sans Unicode', Lucida, Arial, Helvetica,;
            max-width:70%;                        
        }
    </style>
    <title>{{ data['error_title'] }}</title>
</head>
<body>
    <div id="error-container">
        <h1 id="error-title">{{ data['error_title'] }}</h1>
        <p id="error-message">{{ data['error_message'] }}</p>
        <p id="goback-message">Nothing you can do here. So just <a href="/"><strong>go back</strong></a> and forget what you've see</p>
    </div>
    <footer>This cool error message is provided by kokoropy. &copy; GoFrendiAsgard, 2013</footer>
</body>