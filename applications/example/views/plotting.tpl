<link rel="stylesheet" type="text/css" href="{{ BASE_URL }}assets/index/static_libraries/jquery-ui-1.10.3/themes/base/minified/jquery-ui.min.css" />
<h4>You should have matplotlib and StringIO installed</h4>
<div>
    <label>Range : </label>
    <input type="text" name="range" id="range" class="spinner" value="6.28" />    
</div>
<br />
<div id="plot">
    <img src="{{ BASE_URL }}example/plotting/plot" />
</div>
<script type="text/javascript" src="{{ BASE_URL }}assets/index/static_libraries/jquery-ui-1.10.3/ui/minified/jquery-ui.min.js"></script>
<script type="text/javascript">
    $(document).ready(function(){
        $('.spinner').spinner()({
            step: 0.01,
            numberFormat: "n"
        });    
    });    
</script>
%rebase('example/base',title='Plot')