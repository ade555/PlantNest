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
      this_val.prop("disabled", true);
    }
  });
});



$(".add-to-wish-btn").on("click", function(){
  let product_id = $(this).data("product-id");
  let product_name = $(".product_name_" + product_id).val();
  let this_val = $(this);

  $.ajax({
    url: '/store/wish/',
    data: {
      'id': product_id,
      'product_name': product_name,
    },
    dataType: "json",
    success: function (response) {
      this_val.html("Added item to wish");
      this_val.prop("disabled", true);
    },
    error: function (xhr) {
      if (xhr.responseJSON && xhr.responseJSON.error === "Item already exists in the wishlist") {
        alert("This item is already in your wishlist.");
      } else {
        alert("An error occurred while processing your request.");
      }
    }
  });
});

$(".remove-from-wishlist-btn").on("click", function() {
  let product_id = $(this).data("product-id");
  let this_val = $(this);

  $.ajax({
      url: '/store/remove_from_wishlist/', 
      data: {
          'id': product_id,
      },
      dataType: "json",
      success: function(response) {
          this_val.html("Removed from Wish List");
          this_val.prop("disabled", true);
      },
      error: function(xhr) {
          alert("An error occurred while processing your request.");
      }
  });
});


$(".wishlist-add-to-cart").on("click", function(){
  let product_id = $(this).data("product-id");
  let quantity = $(".product_quantity_" + product_id).val();
  let product_name = $(".product_name_" + product_id).val();
  let this_val = $(this);

  $.ajax({
    url: '/store/cart/',
    data: {
      'id': product_id,
      'quantity': quantity,
      'product_name': product_name,
    },
    dataType: "json",
    success: function (response) {
      this_val.html("Added item to cart");
      this_val.prop("disabled", true);
      // Now, also remove the item from the wishlist
      $.ajax({
        url: '/store/remove_from_wishlist/',
        data: {
          'id': product_id,
        },
        dataType: "json",
        success: function (response) {
          // Optionally, you can provide feedback to the user that the item has been removed from the wishlist
          this_val.html("Removed item from wishlist");
        },
        error: function (xhr) {
          console.log("Error removing item from wishlist");
        }
      });
    }
  });
});


$(".empty-cart-btn").on("click", function(e) {
  e.preventDefault();  // Prevent the default link behavior

  // Show a confirmation dialog
  if (confirm("Are you sure you want to empty your cart?")) {
    window.location.href = $(this).attr("href");  // Proceed to the empty_cart URL
  }
});
