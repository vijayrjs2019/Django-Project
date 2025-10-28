jQuery(document).ready(function($) {
    //Contact US Form validation
    $("#subscribeFrom").validate({ 
        rules: {
            email: {
                required: true,
                email: true
            } 
        },
        messages: {
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            }
        },
        submitHandler: function(form) {
            $('#save_butt').hide();
            $('#loader_butt').show();
            form.submit();
        }
    });

    //Contact US Form validation
    $("#contact_us").validate({ 
        rules: {
            user_name: {
                required: true
            },
            user_email: {
                required: true,
                email: true
            },
            user_phone: {
                required: true,
                digits: true,  
                minlength: 10, 
                maxlength: 10  
            },
            user_message: {
                required: true
            } 
        },
        messages: {
            user_name: {
                required: "Please enter  name", 
            },
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },
            user_phone: {
                required: "Please enter Phone No",
                digits: "Please enter only numbers",  
                minlength: "Phone No must be 10 digits",  
                maxlength: "Phone No must not exceed 10 digits" 
            },
            user_message: {
                required: "Please enter message", 
            }
        },
        submitHandler: function(form) {
            $('#save_butt').hide();
            $('#loader_butt').show();
            form.submit();
        }
    });

    //Check out Form validation
    $("#processToPayment_form").validate({ 
        rules: {
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            phone_no: {
                required: true,
                digits: true,  
                minlength: 10, 
                maxlength: 10  
            },
            country: {
                required: true
            },
            state: {
                required: true
            },
            city: {
                required: true
            },
            zip_code: {
                required: true
            },
            delivery_address: {
                required: true
            }  
        },
        messages: {
            first_name: {
                required: "Please enter first name", 
            },
            last_name: {
                required: "Please enter last name", 
            },
            email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },
            phone_no: {
                required: "Please enter Phone No",
                digits: "Please enter only numbers",  
                minlength: "Phone No must be 10 digits",  
                maxlength: "Phone No must not exceed 10 digits" 
            },
            country: {
                required: "Please enter country", 
            },
            state: {
                required: "Please enter state", 
            },
            city: {
                required: "Please enter city", 
            },
            zip_code: {
                required: "Please enter zip code", 
            },
            delivery_address: {
                required: "Please enter delivery address", 
            }
        },
        submitHandler: function(form) {
            $('#save_butt').hide();
            $('#loader_butt').show();
           // form.submit();
            $.ajax({
                url: '/processToPayment',  // Your Django URL here
                type: 'POST',
                data: $(form).serialize(),
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    console.log(response);
                    if (response.payment_method === 'Razorpay') {
                        // window.location.href = response.redirect_url;
                        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
                        var options = {
                            "key": response.razorpay_key_id,
                            "amount": parseInt(response.amount * 100),
                            "currency": "INR",
                            "name": "Your Store Name",
                            "description": "Purchase",
                            "order_id": response.order_id,
                            "handler": function (res) {
                                // Make AJAX to confirm payment
                                fetch('/razorpay-success', {
                                    method: 'POST',
                                    headers: {'X-CSRFToken': csrfToken},
                                    body: JSON.stringify({
                                        delivery_id: response.delivery_id,
                                        razorpay_payment_id: res.razorpay_payment_id,
                                        razorpay_order_id: res.razorpay_order_id,
                                        razorpay_signature: res.razorpay_signature
                                    })
                                }).then(res => res.json()).then(data => {
                                    window.location.href = data.redirect_url;
                                });
                            }
                        };
                        var rzp1 = new Razorpay(options);
                        rzp1.open();
                    } else if (response.payment_method === 'Cash On Delivery') {
                        window.location.href = response.success_url;
                    }
                },
                error: function(xhr, status, error) {
                    alert("Something went wrong. Please try again.");
                    $('#save_butt').show();
                    $('#loader_butt').hide();
                }
            });
        }
    });
});

// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


$('.custom_slick_slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    dots: true,
    fade: true,
    adaptiveHeight: true,
    asNavFor: '.slick_slider_nav',
    responsive: [{
        breakpoint: 768,
        settings: {
            dots: false
        }
    }]
})

$('.slick_slider_nav').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.custom_slick_slider',
    centerMode: false,
    focusOnSelect: true,
    variableWidth: true
});


/** google_map js **/

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}