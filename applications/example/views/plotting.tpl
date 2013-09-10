<link rel="stylesheet" type="text/css" href="{{ BASE_URL }}assets/index/static_libraries/jquery-ui-1.10.3/themes/base/minified/jquery-ui.min.css" />
<h4>Matplotlib and StringIO should be installed on server</h4>
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
        // mutate normal text into spinner
        var range_spinner = $('.spinner').spinner({
            step: 0.01,
            numberFormat: "n",
            max: (8.0*22.0/7.0).toFixed(2),
            min: (0.5*22.0/7.0).toFixed(2),
        }); 
        
        // hack to trigger input change whenever spinner button clicked:
        $('.ui-spinner-button').click(function() { $(this).siblings('input').keyup(); });   
        
        $('#range').keyup(function(){
           range = range_spinner.spinner('value');
           // change image
           if(range!==null){
                $('#plot').html('<img src="{{ BASE_URL }}example/plotting/plot?range='+range+'" />');
           }
        });
    });    
</script>
%rebase('example/views/base',title='Plot')