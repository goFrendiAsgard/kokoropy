<strong>Here is your requested pokemon list:</strong>
<ul>
%for pokemon in pokemons:
    <li>{{pokemon}}</li>
%end
</ul>
Also try this:
<ul>
    <li><a class="btn" href="/example/recommended/pokemon/pikachu">Access the same page with parameter "pikachu"</a></li>
    <li><a class="btn" href="/example/recommended/pokemon?keyword=pi">Access the same page with GET query "keyword=pi"</a></li>
</ul>
%rebase example/base title='Pokemon List'