// VARIATION PRODUCT FUNCTION
$(document).on("change", "#color", function (e) {
  e.preventDefault();
  url = "../detail/";
  slug = $("#product_slug").val();
  console.log(slug);
  $.ajax({
    type: "GET",
    url: url + slug,
    data: {
      size_id: $("#size").val(),
      color_id: $("#color").val(),
      passkey: "get_variant",
    },

    success: function (response, status) {
      $("#p_detail-append").html(response.result);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

// ADD TO CART FUNCTION
$("#add_to_cart_btn").on("click", function (e) {
  $.ajax({
    type: "POST",
    url: "/../basket/add_basket",
    data: {
      product_slug: $("#product_slug").val(),
      size: $("#size").val(),
      color: $("#color").val(),
      product_qty: $("input[name=pro_qty]").val(),
      csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
    },

    success: function (response, status) {
      $(".cart_qty").html(response.qty);
      $(".header__cart__price").find("span").html(response.get_sub_total);
      $(".alert-msg").html(response.message);

      setTimeout(function () {
        $(".alert-msg").show();
        setTimeout(function () {
          $(".alert-msg").hide();
        }, 5000);
      }, 100);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

/*---------------- 
            WISHLIST  AJAX JS
            -----------------*/

/*----------------------
             ADD TO WISHLIST FUNCTION
             ----------------------*/
$("#add_to_wishlist_btn").on("click", function (e) {
  $.ajax({
    type: "POST",
    url: "/../basket/add_wishlist",
    data: {
      product_slug: $("#product_slug").val(),
      size: $("#size").val(),
      color: $("#color").val(),
      product_qty: $("input[name=pro_qty]").val(),
      csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
    },

    success: function (response, status) {
      $(".alert-msg").html(response.message);
      $(".wishlist-counter").html(response.count);
      if (response.wishlist_chk) {
        $(".icon_heart").addClass("icon_heart_selected");
      } else {
        $(".icon_heart").removeClass("icon_heart_selected");
      }

      setTimeout(function () {
        $(".alert-msg").show();
        setTimeout(function () {
          $(".alert-msg").hide();
        }, 5000);
      }, 100);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

/*------------------------ 
            WISHLIST ITEM REMOVE AJAX
            ------------------------*/
$("._wishlist_close").on("click", function () {
  if (confirm("Are you sure you want to delete this?")) {
    var product_id = $(this).attr("data-wishlst");
    $.ajax({
      type: "POST",
      url: "../basket/remove_wishlist",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
      },

      success: function (response, status) {
        window.location.reload();
      },
      error: function (response) {
        alert("error:" + response);
      },
    });
  } else {
    return false;
  }
});

$("#og-form-delete-btn").on("click", function () {
  _pk = $(this).val();
  $.ajax({
    type: "GET",
    url: "addressbook/del",
    data: { pk: _pk },

    success: function (response, status) {
      window.location.replace(response.url);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

$("#og-add-address-btn").on("click", function () {
  $.ajax({
    type: "GET",
    url: "../account/addressbook",
    data: { n_addresform: true },

    success: function (response, status) {
      // $('#AddAddressModalCenter .modal-body').html(response.result);
      $("#AddressModalCenter .modal-content").html(response.result);
      $("#og-address-form").attr("action", "../account/add/addressbook");
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

$(".user-address-edit").on("click", function () {
  var address = $(this).val();

  $.ajax({
    type: "GET",
    url: "../account/addressbook",
    data: { address: address },

    success: function (response, status) {
      $("#AddressModalCenter .modal-content").html(response.result);
      $("#og-address-form").attr("action", "../account/add/addressbook");
      // window.location.replace('');
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

$("#og-addresses").click(function () {
  $.ajax({
    type: "GET",
    url: "../account/user-addressbook",
    data: { shipping: "shipping" },

    success: function (response, status) {
      // console.log(response.result);
      $("#AddressModalCenter .modal-content").html(response.result);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});

$(".og-address-book-card").click(function () {
  var _pk = $(this).find("#form_address_id").val();

  $(".og-address-book-card").removeClass("og-address-book-card-active");
  $(this).addClass("og-address-book-card-active");

  $("#ship-address-confirm-btn").click(function () {
    $.ajax({
      type: "GET",
      url: "edit",
      data: { ship: _pk },

      success: function (response, status) {
        window.location.replace("");
        //  $('#og-address-detail').html(response.result);
        // $('#AddressModalCenter').attr("data-dismiss","modal");
      },
      error: function (response) {
        alert("error:" + response);
      },
    });
  });

  $("#bill-address-confirm-btn").click(function () {
    $.ajax({
      type: "GET",
      url: "edit",
      data: { bill: _pk },

      success: function (response, status) {
        window.location.replace("");
        //  $('#og-address-detail').html(response.result);
        // $('#AddressModalCenter').attr("data-dismiss","modal");
      },
      error: function (response) {
        alert("error:" + response);
      },
    });
  });
});

/*---------------------
            LISTING BILLING ADDRESS
            ----------------------*/
$("#og-billing-content span").on("click", function () {
  // alert($(this).text());
  $.ajax({
    type: "GET",
    url: "../account/user-addressbook",
    data: { billing: "billing" },

    success: function (response, status) {
      $("#AddressModalCenter .modal-content").html(response.result);
    },
    error: function (response) {
      alert("error:" + response);
    },
  });
});
