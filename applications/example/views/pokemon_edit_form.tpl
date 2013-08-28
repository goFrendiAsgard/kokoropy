<form action="{{ BASE_URL }}example/recommended/pokemon" method="post" style="margin: 0 0 0 !important">
    <input name="pokemon_id" value="{{ pokemon_id }}" type="hidden" />
    <input name="action" value="edit" type="hidden" />
    <input name="pokemon_name" value="{{ pokemon_name }}" type="text" />
    <input class="btn btn-primary" name="btn_edit" value="Save" type="submit" /> 
</form> 
%rebase('example/base', title='Pokemon List')