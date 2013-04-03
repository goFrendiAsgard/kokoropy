$(document).ready(function(){
    $('#btn-toggle-note').click(function(){
        $('div#note').toggle();
        if($('#btn-toggle-note').val() != 'Hide Note'){
            $('#btn-toggle-note').val('Hide Note');
        }else{
            $('#btn-toggle-note').val('Show Note');
        }
    });
});