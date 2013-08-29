<form action="{{ BASE_URL }}example/recommended/pokemon" method="post" class="form-horizontal" role="form">
  <div class="form-group">
    <label for="pokemon_name" class="col-lg-2 control-label">Pokemon Name</label>
    <div class="col-lg-10">
      <input type="text" class="form-control" id="pokemon_name" name="pokemon_name" placeholder="Pokemon Name" value="{{ pokemon_name }}" />
    </div>
  </div>
  <div class="form-group">
    <label for="pokemon_name" class="col-lg-2 control-label">Image</label>
    <div class="col-lg-10">
      <input type="file" class="form-control" id="pokemon_image" name="pokemon_image" placeholder="Image" />
    </div>
  </div>
  <div class="form-group">
    <div class="col-lg-offset-2 col-lg-10">
      <input class="btn btn-primary" name="btn_edit" value="Save" type="submit" />
      <input name="__private_code" value="{{ __private_code }}" type="hidden" />
      <input name="pokemon_id" value="{{ pokemon_id }}" type="hidden" />
      <input name="action" value="edit" type="hidden" />
    </div>
  </div>
</form>
%rebase('example/base', title='Pokemon List')