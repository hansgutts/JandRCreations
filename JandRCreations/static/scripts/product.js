$(document).ready(function(){ //wait for the document to load    

    selects = $('.cust_name')

    selects.each(function(i, obj){
        var temp = $(this);
        var tempprev = temp.val();

        temp.data("prev", tempprev);
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

        let priceformatting = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        });
        selector.data("price", priceformatting.format(newprice));

        price_element.html(priceformatting.format(newprice));

    });

}
);