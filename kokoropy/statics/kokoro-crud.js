function _block_form(selector){
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').prop("readonly", true);
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').prop("disabled", "disabled");
    $(selector + ' a._new_row').addClass("disabled");

    if(typeof(CKEDITOR) != 'undefined' && 'instances' in CKEDITOR){
        for(id in CKEDITOR.instances){
            editor = CKEDITOR.instances[id]
            if('setReadOnly' in editor){
                editor.setReadOnly(true);
            }
        }
    }

    $(selector + ' ._code-textarea').each(function(){
        ace = $(this).data('ace').editor.ace;
        if("setReadOnly" in ace){
            ace.setReadOnly(true);
        }
    });
}

function _unblock_form(selector){
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').removeProp("readonly");
    $(selector + ' input, ' + selector + ' textarea, #__main_form select').removeProp("disabled");
    $(selector + ' a._new_row').removeClass("disabled");

    if(typeof(CKEDITOR) != 'undefined' && 'instances' in CKEDITOR){
        for(id in CKEDITOR.instances){
            editor = CKEDITOR.instances[id]
            if('setReadOnly' in editor){
                editor.setReadOnly(false);
            }
        }
    }

    $(selector + ' ._code-textarea').each(function(){
        ace = $(this).data('ace').editor.ace;
        if("setReadOnly" in ace){
            ace.setReadOnly(false);
        }
    });
}