$(".add-to-cart-btn").on("click", function(){
  let product_id = $(this).data("product-id");
  let quantity = $(".product_quantity_" + product_id).val();
  let product_name = $(".product_name_" + product_id).val();
  let product_price = $(".product_price").text();
  let this_val = $(this);

  $.ajax({
    url: '/store/cart/',
    data: {
      'id': product_id,
      'quantity': quantity,
      'product_name': product_name,
      'price': product_price
    },
    dataType: "json",
    success: function (response) {
      this_val.html("Added item to cart");
      let totalCartItems = response.total_cart_items;
      // $(".cart-count").text(totalCartItems);
      this_val.prop("disabled", true);
    }
  });
});











// add to cart functionality 
// $(".add-to-cart-btn").on("click", function(){
//   let quantity = $(".product_quantity").val()
//   let product_name = $(".product_name").val()
//   let product_id = $(".product_id").val()
//   let product_price = $(".product_price").text()
//   let this_val = $(this)

//   $.ajax({
//       url: '/store/cart/',
//       data: {
//           'id':product_id,
//           'quantity': quantity,
//           'product_name':product_name,
//           "price":product_price
//       },
//       dataType: "json",
//       success: function (response) {
//           this_val.html("Added item to cart")
//           let totalCartItems = response.total_cart_items;
//           $(".cart-count").text(totalCartItems);
//           this_val.prop("disabled", true);
//       }
//   });
// })

