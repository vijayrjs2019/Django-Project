jQuery(document).ready(function($) {
    let loaderIcon = "<b>Please Wait.. </b><em class='fa fa-spinner fa-spin'></em>";
    $(".msg").delay(5200).fadeOut(500);

     //Contact US Form validation
    $("#contact-us-form").validate({ 
        rules: {
            user_name: {
                required: true
            },
            user_email: {
                required: true,
                email: true
            },
            user_phone_no: {
                required: true,
                digits: true
            },
            user_subject: {
                required: true
            },
            user_message: {
                required: true
            } 
        },
        messages: {
            user_name: {
                required: "Please enter name", 
            },
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },
            user_phone_no: {
                required: "Please enter phone no", 
                digits: "Please enter a number" 
            },
            user_subject: {
                required: "Please enter subject", 
            },
            user_message: {
                required: "Please enter message", 
            }
        },
        submitHandler: function(form) {
            $('.cum-button').prop('disabled', true).html(loaderIcon); 
            form.submit();
        }
    });

    // Blog Comments Form validation
    $("#blog_comments_form").validate({ 
        rules: {
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            user_email: {
                required: true,
                email: true
            }, 
            user_message: {
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
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },  
            user_message: {
                required: "Please enter commets", 
            }
        },
        submitHandler: function(form) {
            $('.cum-button').prop('disabled', true).html(loaderIcon); 
            form.submit();
        }
    });

    // Book Now Form validation
    $("#book-now-form").validate({ 
        rules: {
            booking_date: {
                required: true
            },
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            user_email: {
                required: true,
                email: true
            }, 
            user_phone_no: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
            terms: {   
                required: true
            }
        },
        messages: {
            booking_date: {
                required: "Please select booking date", 
            },
            first_name: {
                required: "Please enter first name", 
            },
            last_name: {
                required: "Please enter last name", 
            },
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },  
            user_phone_no: {
                required: "Please enter phone no", 
                digits: "Please enter only digits", 
                minlength: "Must be 10 digits",
                maxlength: "Must be 10 digits"
            },
            terms: {
                required: "You must agree to terms and conditions"
            }
        },
        submitHandler: function(form) {
            $('.cum-button').prop('disabled', true).html(loaderIcon); 
            form.submit();
        }
    });

    // Find Receipt Form validation
    $("#find-receipt").validate({ 
        rules: {
            find_id: {
                required: true
            } 
        },
        messages: {
            first_name: {
                find_id: "Please enter Payment ID or Order ID", 
            } 
        },
        submitHandler: function(form) {
            $('.cum-button').prop('disabled', true).html(loaderIcon); 
            form.submit();
        }
    });
    // Home page Book Now Form validation
    $("#home-booking-form").validate({ 
        rules: {
            booking_date: {
                required: true
            },
            first_name: {
                required: true
            },
            last_name: {
                required: true
            },
            user_email: {
                required: true,
                email: true
            }, 
            user_phone_no: {
                required: true,
                digits: true,
                minlength: 10,
                maxlength: 10
            },
            package_id: {   
                required: true
            }
        },
        messages: {
            booking_date: {
                required: "Please select booking date", 
            },
            first_name: {
                required: "Please enter first name", 
            },
            last_name: {
                required: "Please enter last name", 
            },
            user_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },  
            user_phone_no: {
                required: "Please enter phone no", 
                digits: "Please enter only digits", 
                minlength: "Must be 10 digits",
                maxlength: "Must be 10 digits"
            },
            package_id: {
                required: "Plsease select package"
            }
        },
        submitHandler: function(form) {
            $('.cum-button').prop('disabled', true).html(loaderIcon); 
            form.submit();
        }
    });

});


// Razorpay Payment Integration
function payNow() {
    let userData = { 
        first_name: $('#first_name').val(),
        last_name: $('#last_name').val(),
        phone_no: $('#phone_no').val(),
        user_email: $('#user_email').val(),
        booking_date: $('#booking_date').val(),
    };
    let loaderIcon = "<b>Please Wait.. </b><em class='fa fa-spinner fa-spin'></em>";
    $('#pay_butt').html(loaderIcon);
    $.ajax({
        url: '/pay-now/', 
        type: 'POST',
        data: {
            package_id: $('#package_id').val(), 
            submitte_totalPrice: $('#submitte_totalPrice').val(),  
            totalPrice: $('#totalPrice').val(),  
            tax_details: $('#tax_details').val(),
            userData: JSON.stringify(userData),
        },
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
            console.log(response);

            if (!response.amount || !response.payment_id) {
                alert("Invalid payment details received.");
                $('#pay_butt').html('Pay Now');
                return;
            }

            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
            var options = {
                "key": response.razorpay_key_id,
                "amount": parseInt(response.amount * 100),
                "currency": "INR",
                "name": "Travela",
                "description": "Booking Payment",
                "order_id": response.payment_id,
                "handler": function (res) {
                    fetch('/razorpay-success', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            booking_id: response.booking_id,
                            razorpay_payment_id: res.razorpay_payment_id,
                            razorpay_order_id: res.razorpay_order_id,
                            razorpay_signature: res.razorpay_signature
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        window.location.href = data.redirect_url;
                    })
                    .catch(err => {
                        alert("Payment succeeded, but final confirmation failed. Please contact support.");
                        console.error(err);
                    });
                },
                "modal": {
                    "ondismiss": function () {
                        $('#pay_butt').html('Pay Now');
                    }
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
        },
        error: function(xhr, status, error) {
            alert("Something went wrong. Please try again.");
            $('#pay_butt').html('Pay Now'); 
        }
    });
}
