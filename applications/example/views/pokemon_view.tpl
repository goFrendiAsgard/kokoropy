<h3>Pokemon List</h3>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Pokemon Name</th>
            <th>Image</th>
            <th colspan="2">Action</th>
        </tr>        
    </thead>
    <tbody>
        %for pokemon in pokemons:
        <tr>
            <td>{{ pokemon['name'] }}</td>
            <td>
                %if pokemon['image'] == '':
                <img src="{{ BASE_URL }}assets/example/images/pokemon-no-image.png" style="height:65px;" />
                %else:
                <img src="{{ BASE_URL }}assets/example/uploads/{{ pokemon['image'] }}" style="height:65px;" />
                %end
            </td>
            <td width="50px">
               <a class="btn btn-warning" href="{{ BASE_URL }}example/recommended/form_edit_pokemon/{{ pokemon['id'] }}" >
                   Edit
               </a>
            </td>
            <td width="50px">
               <form action="{{ BASE_URL }}example/recommended/pokemon" method="post" style="margin: 0 0 0 !important">
                  <input name="__private_code" value="{{ __private_code }}" type="hidden" />
                  <input name="pokemon_id" value="{{ pokemon['id'] }}" type="hidden" />
                  <input name="action" value="delete" type="hidden" />
                  <input class="btn btn-danger" name="btn_delete" value="Delete" type="submit" /> 
               </form> 
            </td>        
        </tr>
        %end        
    </tbody>      
</table>
<a class="btn btn-success" href="{{ BASE_URL }}example/recommended/form_add_pokemon" >
    Add
</a>
<br />
<ul>
    <li><a class="btn" href="{{ BASE_URL }}example/recommended/pokemon/pikachu">Access the same page with parameter "pikachu"</a></li>
    <li><a class="btn" href="{{ BASE_URL }}example/recommended/pokemon?keyword=pi">Access the same page with GET query "keyword=pi"</a></li>
</ul>
%rebase('example/views/base', title='Pokemon List')