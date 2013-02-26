<style>
    body{
        color: white;
        background-color:#555;        
    }
    div{
        padding: 50px;
        background-repeat: no-repeat;
        background-image:url('/index/images/programmer.png');        
        background-position: bottom right;
        min-height: 250px;
        min-width: 250px;
        display: block;
    }
    a{
        color:white;
    }
</style>
<body>
    <div>
        <h1>{{ data['error_title'] }}</h1>
        <p>{{ data['error_message'] }}</p>
    </div>
</body>