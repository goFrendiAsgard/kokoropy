<html>
<head>
    <link rel="stylesheet" type="text/css" href="/css/style.css" />
    <title>{{ title or 'Kokoropy' }}</title>
</head>
<body>
    <h1>Kokoro py</h1>
    <h2>A pythonic MVC Web Framework</h2>
    <p id="links">
        <a href="/hello_world">A simple hello world (without view)</a>
        <a href="/auto">Another auto routing</a>
        <a href="/hello">Manual routing</a>
        <a href="/hello/Haruna">Another manual routing</a>
        <a href="/hello?name=Rina">One more another manual routing</a>        
        <a href="/pokemon">Pokemon</a>
    </p>
    <p id="content">
        %include
    </p>
    <footer>GoFrendiAsgard &copy; 2013<footer>
</body>
</html>