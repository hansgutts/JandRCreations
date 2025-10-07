

$(document).ready(function(){ //wait for the document to load  
    var del_form = $('#deleteForm')
    function update_type_choices() {
        var design = del_form.find('select[name="design_id"]');
        $.ajax({
            url: 'get_types',
            type: 'GET',
            contentType: 'application/json',
            data: {
                design_id: design.val()
            },
            success: function(response) {
                var types = del_form.find('select[name="type_id"]');
                types.empty();
                

                if(response) {
                    $.each(response, function (ind, obj){
                        var appendVal = '<option value="' + String(obj['id']) + '">' + String(obj['type']) + '</option>';
                        types.append(appendVal);
                    })
                }
            update_prod_choices();
            }
            
        })
    }

    function update_prod_choices() {
        var select = del_form.find('select[name="type_id"]');
        $.ajax({
            url: "get_prods",
            type: 'GET',
            contentType: 'application/json',
            data: {
                type_id: select.val()
            },
            success: function(response) {
                var prods = del_form.find('select[name="product_id"]')
                prods.empty();
                if(response) {
                    $.each(response, function (ind, obj){
                        var appendVal = '<option value="' + String(obj['id']) + '">' + String(obj['prod']) + '</option>';
                        prods.append(appendVal);
                    })
                }
            update_cust_choices()
            }
        })
    } 

    function update_cust_choices() {
        var select = del_form.find('select[name="product_id"]');
        $.ajax({
            url: "get_customs",
            type: "GET",
            contentType: 'application/json',
            data: {
                prod_id: select.val()
            },
            success: function(response) {
                var custom = del_form.find('select[name="custom_id"]');
                custom.empty()

                if(response) {
                    $.each(response, function(ind, obj) {
                        var appendVal = '<option value="' + String(obj['id']) + '">' + String(obj['custom']) + '</option>';
                        custom.append(appendVal);
                    })
                }
            update_option_choices()
            }
        })
    }

    function update_option_choices() {
        var select = del_form.find('select[name="custom_id"]');
        $.ajax({
            url: "get_options",
            type: "GET",
            contentType: 'application/json',
            data: {
                custom_id: select.val()
            },
            success: function(response) {
                var option = del_form.find('select[name="option_id"]');
                option.empty()

                if(response) {
                    $.each(response, function(ind, obj) {
                        var appendVal = '<option value="' + String(obj['id']) + '">' + String(obj['option']) + '</option>';
                        option.append(appendVal);
                    })
                }
            }
        })
    }

    del_form.find('select[name="design_id"]').change(function() {
        update_type_choices();
        //update_prod_choices();
    })

    del_form.find('select[name="type_id"]').change(function() {
        update_prod_choices();
        //update_cust_choices();
    })

    del_form.find('select[name="product_id"]').change(function(){
        update_cust_choices();
        //update_option_choices();
    })

    del_form.find('select[name="custom_id"]').change(function() {
        update_option_choices();
    })



    var addDelete = $("#addDeleteForm")
    var addDeleteField = $('input[name="addDelete"]:checked');
    var addForm = $('#addForm');
    var deleteForm = $('#deleteForm');

    var formTextBox = $('#form_text')
    var FORMTEXTVALUE = formTextBox.html()

    addDelete.change(function(data) {
        addDeleteField = $('input[name="addDelete"]:checked');
        if (addDeleteField.val() == 'Add') {
            addForm.removeClass('hidden')
            deleteForm.addClass('hidden')

            formTextBox.html(FORMTEXTVALUE)

        } else if (addDeleteField.val() == 'Delete') { 
            deleteForm.removeClass('hidden')
            addForm.addClass('hidden')

            formTextBox.html("Choose which element to delete")

        }
    });
    

});

