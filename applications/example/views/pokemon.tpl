<h3>Pokemon List</h3>
<div class="pull-right">
    <a class="btn btn-success" href="{{ BASE_URL }}example/pokemon/form_add_pokemon" >
        <i class="glyphicon glyphicon-plus"></i> Add New Pokemon
    </a>
</div>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Pokemon Name</th>
            <th>Image</th>
            <th colspan="2">Action</th>
        </tr>
    </thead>
    <tbody>
        %for pokemon in pokemon_list:
        <tr>
            <td>{{ pokemon.name }}</td>
            <td>
                %if pokemon.image == '':
                <img src="{{ BASE_URL }}example/assets/images/pokemon-no-image.png" style="height:65px;" />
                %else:
                <img src="{{ BASE_URL }}example/assets/uploads/{{ pokemon.image }}" style="height:65px;" />
                %end
            </td>
            <td width="50px">
               <a class="btn btn-warning" href="{{ BASE_URL }}example/pokemon/form_edit_pokemon/{{ pokemon.id }}" >
                   Edit
               </a>
            </td>
            <td width="50px">
               <form action="{{ BASE_URL }}example/pokemon" method="post" style="margin: 0 0 0 !important">
                  <input name="__private_code" value="{{ __private_code }}" type="hidden" />
                  <input name="pokemon_id" value="{{ pokemon.id }}" type="hidden" />
                  <input name="action" value="delete" type="hidden" />
                  <input class="btn btn-danger" name="btn_delete" value="Delete" type="submit" />
               </form>
            </td>
        </tr>
        %end
    </tbody>
</table>

<br />
<div class="alert alert-info row" style="margin-top:40px;">
    <b>Also Try:</b>
    <ul>
        <li><a class="btn" href="{{ BASE_URL }}example/pokemon/pikachu">Access this page with parameter "pikachu"</a></li>
        <li><a class="btn" href="{{ BASE_URL }}example/pokemon?keyword=pi">Access this page with GET query "keyword=pi"</a></li>
    </ul>
</div>
%rebase('index/views/base', title='Pokemon List')