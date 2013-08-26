<form action="{{ BASE_URL }}example/recommended/pokemon" method="post" style="margin: 0 0 0 !important">
    <input name="action" value="add" type="hidden" />
    <input name="pokemon_name" value="" type="text" />
    <input class="btn btn-primary" name="btn_new" value="New" type="submit" /> 
</form> 
%rebase('example/base', title='Pokemon List')