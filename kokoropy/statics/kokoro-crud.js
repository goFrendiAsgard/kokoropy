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