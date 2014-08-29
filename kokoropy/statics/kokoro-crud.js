function _mutate_input(){
    $( "._date-input" ).datepicker({
        defaultDate: null,
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "yy-mm-dd",
        yearRange: "c-50:c+50",
    });
    $("._file-input").customFileInput({
        button_position : "right"
    });
    $("._integer-input").spinner();
}
function _block_form(selector){
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').prop("readonly", true);
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').prop("disabled", "disabled");
    $(selector + ' a._new_row').addClass("disabled");
}

function _unblock_form(selector){
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').removeProp("readonly");
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').removeProp("disabled");
    $(selector + ' a._new_row').addClass("disabled");
}

$(document).ready(function(){
    _mutate_input();
    $("._new_row").live("click", function(event){
        _mutate_input();
    });
});