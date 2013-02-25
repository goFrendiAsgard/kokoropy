<html>
<head>
    <link rel="stylesheet" type="text/css" href="/example/css/style.css" />
    <title>{{ title or 'Kokoropy' }}</title>
</head>
<body>
    <h1>Kokoro py</h1>
    <h2>A pythonic MVC Web Framework</h2>
    <p id="links">
        <a href="/hello">A normal hello without parameter</a>
        <a href="/hello?name=Rina">Hello with query</a>
        <a href="/hello/Haruna">Hello with parameter</a>
        <a href="/pokemon">Pokemon</a>
    </p>
    <p id="content">
        %include
    </p>
    <footer>GoFrendiAsgard &copy; 2013<footer>
</body>
</html>