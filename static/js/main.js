/*  ---------------------------------------------------
    Template Name: Ogani
    Description:  Ogani eCommerce  HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");

        /*------------------
            Gallery filter
        --------------------*/
        $('.featured__controls li').on('click', function () {
            $('.featured__controls li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.featured__filter').length > 0) {
            var containerEl = document.querySelector('.featured__filter');
            var mixer = mixitup(containerEl);
        }
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    //Humberger Menu
    $(".humberger__open").on('click', function () {
        $(".humberger__menu__wrapper").addClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").addClass("active");
        $("body").addClass("over_hid");
    });

    $(".humberger__menu__overlay").on('click', function () {
        $(".humberger__menu__wrapper").removeClass("show__humberger__menu__wrapper");
        $(".humberger__menu__overlay").removeClass("active");
        $("body").removeClass("over_hid");
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*-----------------------
        Categories Slider
    ------------------------*/
    $(".categories__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 4,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            0: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 3,
            },

            992: {
                items: 4,
            }
        }
    });


    $('.hero__categories__all').on('click', function(){
        $('.hero__categories ul').slideToggle(400);
    });

    /*--------------------------
        Latest Product Slider
    ----------------------------*/
    $(".latest-product__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 1,
        dots: false,
        nav: true,
        navText: ["<span class='fa fa-angle-left'><span/>", "<span class='fa fa-angle-right'><span/>"],
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------------
        Product Discount Slider
    -------------------------------*/
    $(".product__discount__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {

            320: {
                items: 1,
            },

            480: {
                items: 2,
            },

            768: {
                items: 2,
            },

            992: {
                items: 3,
            }
        }
    });

    /*---------------------------------
        Product Details Pic Slider
    ----------------------------------*/
    var p_img = $('#p_count_images').val();
    $(".product__details__pic__slider").owlCarousel({
        loop: true,
        margin: 20,
        items: p_img,
        dots: true,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true
    });

    /*-----------------------
		Price Range Slider
	------------------------ */
    var rangeSlider = $(".price-range"),
        minamount = $("#minamount"),
        maxamount = $("#maxamount"),
        minPrice = rangeSlider.data('min'),
        maxPrice = rangeSlider.data('max');
    rangeSlider.slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            minamount.val('$' + ui.values[0]);
            maxamount.val('$' + ui.values[1]);
        }
    });
    minamount.val('$' + rangeSlider.slider("values", 0));
    maxamount.val('$' + rangeSlider.slider("values", 1));

    /*--------------------------
        Select
    ----------------------------*/
    $("select").niceSelect();

    /*------------------
		Single Product
	--------------------*/
    $('.product__details__pic__slider img').on('click', function () {

        var imgurl = $(this).data('imgbigurl');
        var bigImg = $('.product__details__pic__item--large').attr('src');
        if (imgurl != bigImg) {
            $('.product__details__pic__item--large').attr({
                src: imgurl
            });
        }
    });

    /*-------------------
		Quantity change
	--------------------- */
    var proQty = $('.pro-qty');
    proQty.prepend('<span class="dec qtybtn">-</span>');
    proQty.append('<span class="inc qtybtn">+</span>');
    proQty.on('click', '.qtybtn', function () {
        var $button = $(this);
        var oldValue = $button.parent().find('input').val();
        if ($button.hasClass('inc')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        $button.parent().find('input').val(newVal);
        
           
             }); 
    
})(jQuery);
$('.alert-msg').hide()



            /*-------------- 
            AJAX UPDATE CART 
            ---------------*/

            var proQty = $('.shopcart_qty');
            proQty.on('click', '.qtybtn', function () {
            var $button = $(this);
                
            var product_id = $button.siblings('._shopping_cart_qty').attr('data-productId');
            var quantity = $button.siblings('._shopping_cart_qty').val();

             $.ajax({
                 type: "POST",
                 url: "../basket/edit_basket", 
                 data:{
                     'product_id':  product_id,
                     'product_qty': quantity,
                     'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                     
                 },
               
             success: function(response,status){
               $('.cart_qty').html(response.data.total_qty);
               $('.alert-msg').html(response.message);
               $('.shoping__checkout').find('ul li span').first().html(Number(response.data.gross_amount).toFixed(2));
               $('.shoping__checkout').find('ul li span').last().html(Number(response.data.total_amount).toFixed(2));
               $('.header__cart__price span').text(response.data.gross_amount)
               $('#total_price_'+product_id+'').text(response.data.total_price); 
                    setTimeout(function(){
                   $('.alert-msg').show();
                   setTimeout(function(){
                     $('.alert-msg').hide();
                   }, 5000);
                 }, 100);
             },
             error:function(response){
                 alert('error:'+response);
     
             }
        
             });

            });

            /*------------------------ 
            CART ITEM REMOVE AJAX
            ------------------------*/
    $('._cart_close').on('click',function(){
        if(confirm("Are you sure you want to delete this?")){
            var product_id = $(this).attr('data-productId');
           
        $.ajax({
            type: "POST",
            url: "../basket/remove_basket", 
            data:{
                'product_id':  product_id,
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
                
            },
          
        success: function(response,status){
            window.location.reload();
           
        },
        error:function(response){
            alert('error:'+response);

        }
   
        });
    }
    else{
        return false;
    }
    });



            /*------------------------ 
            RESTRICTION QUANTITY INPUT
            ------------------------*/
function restrict_qty_input(evt){
    var x = evt.which || evt.keycode;
        if( x > 48 &&  x <= 57 ){
            return true;
        }
        else{
            return false
        }
    
}


$('.og-form-addresstag').on('click',function(){
           
    var btn = $(this);

    $('*').removeClass('checked')
    var data = btn.find('input[name=label_tags]').attr("checked", "checked") ? (btn.find('label').addClass('checked')) : (btn.find('label').removeClass('checked'));
    
    });