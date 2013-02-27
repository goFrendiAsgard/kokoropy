<style>
    body{
        color: white;
        background-color:#555;
        padding-left: 50px;
        padding-top: 20px;        
    }
    div{        
        background-repeat: no-repeat;
        background-image:url('/index/images/programmer.png');        
        background-position: bottom right;
        min-height: 300px;
        min-width: 250px;
        display: block;
    }
    a{
        color:white;
    }
    footer{
        font-size:small;
    }
</style>
<body>
    <div>
        <h1>{{ data['error_title'] }}</h1>
        <p>{{ data['error_message'] }}</p>
    </div>
    <footer>This cool error message is provided by kokoropy. &copy; GoFrendiAsgard, 2013</footer>
</body>