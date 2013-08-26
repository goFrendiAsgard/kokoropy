<strong>Here is your requested pokemon list:</strong>
<table>
    <tr>
        <th>Pokemon Name</th>
        <th colspan="2">Action</th>
    </tr>
%for pokemon in pokemons:
    <tr>
        <td>{{ pokemon['name'] }}</td>
        <td>
           <a class="btn btn-warning btn-edit" record_id="{{ pokemon['id] }}" >
               Edit
           </a>
        </td>
        <td>
           <form action="{{ BASE_URL }}example/recommended/pokemon" method="post" style="margin: 0 0 0 !important">
              <input name="pokemon_id" value="{{ pokemon['id'] }}" type="hidden" />
              <input name="action" value="delete" type="hidden" />
              <input class="btn btn-danger" name="btn_delete" value="Delete" type="submit" /> 
           </form> 
        </td>        
    </tr>
%end    
</table>
Also try this:
<ul>
    <li><a class="btn" href="{{ BASE_URL }}example/recommended/pokemon/pikachu">Access the same page with parameter "pikachu"</a></li>
    <li><a class="btn" href="{{ BASE_URL }}example/recommended/pokemon?keyword=pi">Access the same page with GET query "keyword=pi"</a></li>
</ul>
%rebase('example/base', title='Pokemon List')