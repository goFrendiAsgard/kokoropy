<p>{{message}}</p>
<form action="/example/recommended/upload" method="post" enctype="multipart/form-data">
  Select a file: <input type="file" name="upload" />
  <input type="submit" value="Start upload" />
</form>
%rebase example/base title='Upload'