$(document).ready(function(){ //wait for the document to load    

    selects = $('.cust_name') //get all select fields
    

    selects.each(function(i, obj){ //for each select field
        
        var selector = $(this); //get this select field
        var selector_prev = selector.val(); //set the previous value of our selector fields (the default value)
        
        selector.data("prev", selector_prev); //set the prev value using data functionality
        

        let priceformatting = new Intl.NumberFormat('en-US', { //formatting to USD for the price
            style: 'currency',
            currency: 'USD',
        });

        var price_element = $('#prod_price'); //get the price of the product
        var newprice = parseFloat(price_element.text().substring(1)) + parseFloat(selector.val()); //get the price in float format
        
        price_element.html(priceformatting.format(newprice)); //set the starting price
        
        
    });

    //we need to update the price of the item when choosing different elements
    selects.change(function(data) { //now when we change the selected option
        var selector = $(this); //get the element that changed

        var price_element = $('#prod_price'); //get the price of the product
        var newprice = parseFloat(price_element.text().substring(1)); //get the price in float format

        //updat the value of our product to only reflect currently selected options
        newprice = newprice - selector.data("prev") //need to remove value of previous option
        newprice = parseFloat(newprice) + parseFloat(selector.val())  //add value of current option

        selector.data("prev", selector.val()); //we need to set the new previous value        

        let priceformatting = new Intl.NumberFormat('en-US', { //format the price in USD
            style: 'currency',
            currency: 'USD',
        });

        price_element.html(priceformatting.format(newprice)); //set the new price

    });

}
);