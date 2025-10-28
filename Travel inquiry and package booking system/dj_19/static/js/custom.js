jQuery(document).ready(function($) {
    let loaderIcon = "<b>Please Wait.. </b><em class='fa fa-spinner fa-spin'></em>";
    $(".msg").delay(5200).fadeOut(500);

    //Contact US Form validation
    $("#subscribeFrom").validate({ 
        rules: {
            subscribe_email: {
                required: true,
                email: true
            } 
        },
        messages: {
            subscribe_email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            }
        },
        submitHandler: function(form) {
            $('#save_butt').html(loaderIcon);
            $('#save_butt').attr('disabled','disabled');
            $.ajax({
                url: $(form).attr('action'),
                method: "POST",
                data: $(form).serialize(),
                success: function(response, textStatus, xhr) {
                    $('#save_butt').html("Subscribe");
                    $('#save_butt').removeAttr('disabled');
                    $('#subscribed_msg').show();
                    if(xhr.status === 200){
                        $('#subscribe_email').val("");
                        $("#subscribed_msg").html('<span class="text-success" style="color:#00f181 !important;">You have successfully subscribed to our newsletter.</span>');
                    }else{
                        $("#subscribed_msg").html(response.error);
                    }
                    
                },
                error: function(xhr) {
                    $('#save_butt').html("Subscribe");
                    $('#save_butt').removeAttr('disabled');
                    if (xhr.status === 409 && xhr.responseJSON?.error) {
                        errorMsg = xhr.responseJSON.error;
                    } else if (xhr.responseJSON?.error) {
                        errorMsg = xhr.responseJSON.error;
                    }
                     $("#subscribed_msg").html('<span class="text-danger" style="color:#ff707e !important;">' + errorMsg + '</span>');
                }
            });

            return false;
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
            user_subject: {
                required: "Please enter subject", 
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

    //Write a comment Form validation
    $("#write_comment_form").validate({ 
        rules: {
            name: {
                required: true,
            },
            email: {
                required: true,
                email: true
            } 
        },
        messages: {
            name: {
                required: "Please enter  name", 
            },
            email: {
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
    

    $.validator.addMethod("filetype", function (value, element, param) {
        if (element.files.length === 0) return true; // no file selected
        const ext = value.split('.').pop().toLowerCase();
        return param.includes(ext);
    }, "Only .doc, .docx, or .pdf files are allowed.");
    //Apply For Job Form validation
    $("#apply_job_form").validate({ 
        rules: {
            name: {
                required: true,
            },
            phone_no: {
                required: true,
                digits: true,  
                minlength: 10, 
                maxlength: 15 
            },
            email: {
                required: true,
                email: true
            },
            resume: {
                required: true,
                filetype: ["doc", "docx", "pdf"]
            },
        },
        messages: {
            name: {
                required: "Please enter  name", 
            },
            phone_no: {
                required: "Please enter phone number",
                digits: "Please enter only digits",
                minlength: "Phone number must be at least 10 digits",
                maxlength: "Phone number can't be more than 15 digits"
            },
            email: {
                required: "Please enter email", 
                email: "Please enter a valid email address" 
            },
            resume: {
                required: "Please upload resume", 
                filetype: "Only .doc, .docx, or .pdf files are allowed"
            }
        },
        submitHandler: function(form) {
            $('#save_butt').hide();
            $('#loader_butt').show();
            form.submit();
        }
    });

    // registrations Popup Form
     $("#registrationsForm").validate({
        rules: {
            first_name: { required: true },
            last_name: { required: true },
            username: { required: true },
            email: {
            required: true,
            email: true
            },
            password1: {
            required: true,
            minlength: 6
            },
            password2: {
            required: true,
            equalTo: "#id_password1"
            }
        },
        messages: {
            first_name: { required: "Please enter first name" },
            last_name: { required: "Please enter last name" },
            username: { required: "Please enter username" },
            email: {
            required: "Please enter email",
            email: "Enter a valid email"
            },
            password1: {
            required: "Please enter a password",
            minlength: "Password must be at least 6 characters"
            },
            password2: {
            required: "Please confirm your password",
            equalTo: "Passwords do not match"
            }
        },
        submitHandler: function(form) {
            $('#save_butt_frm').html(loaderIcon);
            $('#save_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });
    
    // registrations Page Form
    $("#registrationsPageForm").validate({
        rules: {
            first_name: { required: true },
            last_name: { required: true },
            username: { required: true },
            email: {
            required: true,
            email: true
            },
            password1: {
            required: true,
            minlength: 6
            },
            password2: {
            required: true,
            equalTo: "#p_password1"
            }
        },
        messages: {
            first_name: { required: "Please enter first name" },
            last_name: { required: "Please enter last name" },
            username: { required: "Please enter username" },
            email: {
            required: "Please enter email",
            email: "Enter a valid email"
            },
            password1: {
            required: "Please enter a password",
            minlength: "Password must be at least 6 characters"
            },
            password2: {
            required: "Please confirm your password",
            equalTo: "Passwords do not match"
            }
        },
        submitHandler: function(form) {
            $('#reg_page_butt_frm').html(loaderIcon);
            $('#reg_page_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });

    // Login page validations
    $("#loginPageForm").validate({
        rules: {
            username: { required: true },
            password: {
            required: true,
            minlength: 6
            },
        },
        messages: { 
            username: { required: "Please enter username" },
            password: {
            required: "Please enter a password",
            minlength: "Password must be at least 6 characters"
            },
        },
        submitHandler: function(form) {
            $('#login_page_butt_frm').html(loaderIcon);
            $('#login_page_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });

    // Login Popup validations
    $("#loginPopupForm").validate({
        rules: {
            username: { required: true },
            password: {
            required: true,
            minlength: 6
            },
        },
        messages: { 
            username: { required: "Please enter username" },
            password: {
            required: "Please enter a password",
            minlength: "Password must be at least 6 characters"
            },
        },
        submitHandler: function(form) {
            $('#login_popup_butt_frm').html(loaderIcon);
            $('#login_popup_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });

    // registrations Page Form
    $("#changePasswordForm").validate({
        rules: {
            old_password: { required: true },
            new_password1: {
            required: true,
            minlength: 6
            },
            new_password2: {
            required: true,
            equalTo: "#new_password1"
            }
        },
        messages: {
            old_password: { required: "Please enter old password" },
            new_password1: {
            required: "Please enter a new password",
            minlength: "Password must be at least 6 characters"
            },
            new_password2: {
            required: "Please confirm password",
            equalTo: "Passwords do not match"
            }
        },
        submitHandler: function(form) {
            $('#chng_butt_frm').html(loaderIcon);
            $('#chng_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });

    // User Profile  Page Form
    $("#userProfileForm").validate({
        rules: {
            first_name: { required: true },
            last_name: { required: true }, 
            email: {
            required: true,
            email: true
            },
            phone: { required: true }, 
            country: { required: true }, 
            address: { required: true }, 
        },
        messages: {
            first_name: { required: "Please enter first name" },
            last_name: { required: "Please enter last name" },
            email: {
            required: "Please enter email",
            email: "Enter a valid email"
            },
            phone: { required: "Please enter phone" },
            country: { required: "Please select country" },
            address: { required: "Please enter address" },
        },
        submitHandler: function(form) {
            $('#up_page_butt_frm').html(loaderIcon);
            $('#up_page_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });


    // User Profile  Page Form
    $("#userAddImageOnGalleryForm").validate({
        rules: {
            img_title: { required: true },
            img_category: { required: true },  
            img_country: { required: true }, 
            thumbnail_image: { required: true }, 
        },
        messages: {
            img_title: { required: "Please enter image title" },
            img_category: { required: "Please select category" },
            img_country: { required: "Please select country" },
            thumbnail_image: { required: "Please select image" }, 
        },
        submitHandler: function(form) {
            $('#uaig_butt_frm').html(loaderIcon);
            $('#uaig_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });

    // Online Booking Enquiry Form
    $("#online_booking_enquiry").validate({
        rules: {
            bon_name: { required: true },
            bon_email: {
            required: true,
            email: true
            },
            bon_phone: { 
                required: true ,
                digits: true
            }, 
            bon_departure_date: { required: true }, 
            bon_no_person: { 
                required: true ,
                digits: true
            }, 
            bon_hotel_type: { required: true },
            bon_category: { required: true }, 
            bon_destination: { required: true },
            bon_country: { required: true },
            bon_duration: { 
                required: true , 
                digits: true
            },
            bon_tour_details: { required: true }, 
        },
        messages: {
            bon_name: { required: "Please enter image title" },
            bon_email: {
            required: "Please enter email",
            email: "Enter a valid email"
            },
            bon_phone: {
                 required: "Please enter phone" ,
                 digits: "Please enter only digits"
            },
            bon_departure_date: { required: "Please select departure date" }, 
            bon_no_person: { 
                required: "Please enter no person" ,
                digits: "Please enter only digits"
            }, 
            bon_hotel_type: { required: "Please select hotel type" }, 
            bon_destination: { required: "Please enter destination" }, 
            bon_country: { required: "Please select country" }, 
            bon_duration: { 
                required: "Please enter no duration" ,
                digits: "Please enter only digits"
            }, 
            bon_tour_details: { required: "Please enter tour details" }, 
        },
        submitHandler: function(form) {
            $('#bon_butt_frm').html(loaderIcon);
            $('#bon_butt_frm').attr('disabled','disabled');
            form.submit();
        }
    });
 
});

let loaderIcon = "<b>Please Wait.. </b><em class='fa fa-spinner fa-spin'></em>";
   
// Form for add Image On Gallery
function addImageOnGallery(){
     $('#myAddImageOnGalleryModal').modal('show');
}

// Display Image on popup
function displayImageOnGallery(imageUrl){ 
    $('#user_image_display').attr('src', imageUrl);
     $('#myDisplayImageOnGalleryModal').modal('show');
}

// Delete Item
function confirmDeleteItem(imageId,reqType) {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    title: 'Deleted!',
                    text: 'Your item has been deleted.',
                    icon: 'success',
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    // Redirect to Django delete view
                    if(reqType == 'image'){
                        window.location.href = `/delete-user-image/${imageId}/`;
                    }else{
                        window.location.href = `/delete-travel-enquiry/${imageId}/`;
                    }
                });
            }
        });
    }


function displayTravelEnquiry(enquiry_id){
     $.ajax({
        url: '/get-travel-enquiry/',   
        type: 'GET',
        data: {
            id: enquiry_id
        },
        success: function(response) {
            // Populate modal fields with response data
            $('#dte_name').html(response.name);
            $('#dte_email').html(response.email);
            $('#dte_phone').html(response.phone_no);
            $('#dte_created_date').html(response.created_date);
            $('#dte_departure_date').html(response.departure_date);
            $('#dte_destination').html(response.duration);
            $('#dte_country').html(response.country);
            $('#dte_hotel_type').html(response.hotel_type);
            $('#dte_no_days').html(response.duration);
            $('#dte_no_person').html(response.no_person);
            $('#dte_category').text(response.category);
            $('#dte_additional_info').text(response.tourdetails);

            // Show the modal
            $('#myDisplayTravelEnquiryModal').modal('show');
        },
        error: function(xhr) {
            alert('Something went wrong!');
        }
    });
}

function displayQuotation(enquiry_id){
     $.ajax({
        url: '/get-quotation/',   
        type: 'GET',
        data: {
            id: enquiry_id
        },
        success: function(response) {
            // Populate modal fields with response data
            $('#dq_btn_booked').attr('href', '/booking-confirmation/'+enquiry_id);
            $('#dq_price').html(response.price);
            $('#dq_quotation_deacription').html(response.deacription); 
            $('#myDisplayQuotationModal').modal('show');
        },
        error: function(xhr) {
            alert('Something went wrong!');
        }
    });
}

function payNow(srt) {
    let userData = {};
    if (srt === 'Package') {
        userData['bon_name'] = $('#bon_name').html(); 
        userData['bon_email'] = $('#bon_email').html();
        userData['bon_phone'] = $('#bon_phone').html();
        userData['bon_departure_date'] = $('#bon_departure_date').html();
        userData['bon_tour_details'] = $('#bon_tour_details').html(); 
        userData['bon_package_id'] = $('#enquiry_id').val();
        userData['bon_want_register'] = $('#bon_want_register').val(); 
    }
    $('#pay_butt').html(loaderIcon);
    $.ajax({
        url: '/pay-now/', 
        type: 'POST',
        data: {
            booking_type: srt,
            enquiry_id: $('#enquiry_id').val(),
            sub_total_amount: $('#sub_total_amount').val(),
            total_tax_amount: $('#total_tax_amount').val(),
            total_amount: $('#total_amount').val(),
            tax_details: JSON.parse($('#tax_details').val()),
            userData: userData 
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

function loginWithOption(srt){
    if(srt == 'normal'){
          $(".cum-normal").removeClass("btn-light").addClass("btn-primary");
          $(".cum-face").removeClass("btn-primary").addClass("btn-light");
    }else{
         $(".cum-face").removeClass("btn-light").addClass("btn-primary");
         $(".cum-normal").removeClass("btn-primary").addClass("btn-light");
    }
}