

$(document).ready(function(){ //wait for the document to load  

    var del_form = $('#deleteForm') //we need to only update on the delete form
    function update_type_choices() { //our function to update choices
        var design = del_form.find('select[name="design_id"]'); //get the design id select field
        $.ajax({ //send ajax request to make it dynamic
            url: SCRIPT_ROOT + 'get_types',
            type: 'GET',
            contentType: 'application/json',
            data: { //send it the design id
                design_id: design.val()
            },
            success: function(response) { //if it suceeded
                var types = del_form.find('select[name="type_id"]'); //get the types returned
                types.empty(); //empty the select field options
                

                if(response) { //if we got a response (there may not be if they don't exist in the db)
                    $.each(response, function (ind, obj){ //loop through the response
                        //manually create the option values
                        var appendVal = '<option value="' + String(obj['id']) + '">' + String(obj['type']) + '</option>';
                        types.append(appendVal); //insert them into the select field
                    })
                }
            update_prod_choices();
            }
            
        })
    }

    function update_prod_choices() {
        var select = del_form.find('select[name="type_id"]');
        $.ajax({
            url: SCRIPT_ROOT + "get_prods",
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
            url: SCRIPT_ROOT + "get_customs",
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
            url: SCRIPT_ROOT + "get_options",
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

    //when the select fields change call their relative function
    del_form.find('select[name="design_id"]').change(function() {
        update_type_choices();
    })

    del_form.find('select[name="type_id"]').change(function() {
        update_prod_choices();
    })

    del_form.find('select[name="product_id"]').change(function(){
        update_cust_choices();
    })

    del_form.find('select[name="custom_id"]').change(function() {
        update_option_choices();
    })


    //get document elements needed to change between adding and deleting
    var addDelete = $("#addDeleteForm")
    var addDeleteField = $('input[name="addDelete"]:checked');
    var addForm = $('#addForm');
    var deleteForm = $('#deleteForm');

    var formTextBox = $('#form_text')
    var FORMTEXTVALUE = formTextBox.html()

    //when add or delete is selected
    addDelete.change(function(data) {
        //determine whether we are becoming add or delete
        addDeleteField = $('input[name="addDelete"]:checked');
        if (addDeleteField.val() == 'Add') { //if we need to add
            addForm.removeClass('hidden') //make addform not hidden
            deleteForm.addClass('hidden') //hide the delete form

            formTextBox.html(FORMTEXTVALUE) //update the instructions ("add/delete item")
        // if deleting
        } else if (addDeleteField.val() == 'Delete') { 
            deleteForm.removeClass('hidden') //make deleteform not hidden
            addForm.addClass('hidden') //hide the add form
            //update instructions
            formTextBox.html("Choose which element to delete")

        }
    });
    

});

