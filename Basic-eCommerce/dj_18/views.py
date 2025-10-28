from django.shortcuts import render,redirect
from siteSetting.models import AboutUsInfo,SubscribeList,ContactUs,Testimonial,SliderList
from blogs.models import Blogs
from product.models import Category,Product,TaxSetting,ShippingCostSetting,ProductDelivery,RazorpaySetting
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib import messages
from decimal import Decimal
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
import random
import razorpay
from django.conf import settings
from django.views.decorators.http import require_POST
import json
# Home
def home(request):
    aboutUsInfo = AboutUsInfo.objects.first()
    product = Product.objects.all().order_by('-id')[:6]
    blogs = Blogs.objects.all().order_by('-id')[:3]
    testimonial = Testimonial.objects.all().order_by('-id')[:3]
    sliderList = SliderList.objects.all().order_by('-id')[:4]
    return render(request,'pages/home.html',{'title':'Home','products':product,'aboutUsInfo':aboutUsInfo,'blogs':blogs,'testimonial':testimonial,'sliderList':sliderList})

# About
def about(request):
    data = AboutUsInfo.objects.first()
    return render(request,'pages/about.html',{'title':'About Us','aboutUsInfo':data})

# furnitures
def furnitures(request, category_id=None):
    category = Category.objects.all()
    product = Product.objects.all().order_by('-id')
    
    if category_id:
        product = product.filter(category=category_id).order_by('-id')

    if request.method == 'POST':
        srt = request.POST.get('product_name')
        if srt:  # this checks for None and empty string
            product = Product.objects.filter(product_name__icontains=srt).order_by('-id')
        
    return render(request,'pages/furnitures.html',{'title':'Furnitures','category':category,'products':product,'category_id':category_id})

def furnituresDetail(request,slug):
    data = Product.objects.get(slug=slug)
    return render(request,'pages/furnituresDetail.html',{'title':data.product_name,'furnituresDetail':data})

#blog
def blog(request):
    data = Blogs.objects.all()
    return render(request,'pages/blog.html',{'title':'Blog','blogList':data})

#blog Detail
def blogDetail(request,slug):
    data = Blogs.objects.get(slug=slug)
    return render(request,'pages/blogDetail.html',{'title':data.title,'blogDetail':data})

# contact Us
def contactUs(request):
    errormessage = None
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        user_phone = request.POST.get("user_phone")
        user_email = request.POST.get("user_email")
        user_message = request.POST.get("user_message")
        if user_email and user_message and user_name and user_phone:
            if ContactUs.objects.filter(user_email=user_email).exists():
                messages.error(request, "This email is already subscribed!")
                # errormessage = "This email is already subscribed."  # Set error message
            else:
                ContactUs.objects.create(user_name=user_name,user_phone=user_phone,user_email=user_email,user_message=user_message)
                messages.success(request, "Email has benn sent successfully!")
                # succesmessage = "Email has benn sent successfully."  # Set success message
                return redirect('contactUs')

    return render(request,'pages/contactUs.html',{'title':'Contact Us',"errormessage": errormessage})

#subscribe
def subscribe(request):
    message = None
    if request.method == 'POST':
        email = request.POST.get("email")
        if email:
            if SubscribeList.objects.filter(email=email).exists():
                message = "This email is already subscribed."  # Set error message
            else:
                SubscribeList.objects.create(email=email)
                return redirect('contactUs')

    return render(request, "pages/contactUs.html", {"message": message})  # Pass message to template


def checkOut(request):
    # Initialize variables to default values
    product_info = None
    sub_total = 0
    apply_tax = 0
    total_price = 0
    quantity = 1  # You can set this dynamically if needed
    taxSetting = None
    shippingCost = None

    # Handle POST request
    if request.method == 'POST':
        # Ensure taxSetting is found or raise an error
        taxSetting = TaxSetting.objects.first()
        if not taxSetting:
            raise Http404("Tax settings not found")

        # Safely handle product info
        product_id = request.POST.get("product_id")
        try:
            product_info = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise Http404("Product not found")

        # Safely handle tax value and calculate subtotal
        total_tax_in_per = Decimal(taxSetting.tax_value) if taxSetting.tax_value else Decimal(0)
        sub_total = quantity * product_info.product_price 

        # Handle tax calculation based on type
        if taxSetting.text_apply_type == "Flat":
            apply_tax = Decimal(taxSetting.tax_value)
        else:
            apply_tax = (total_tax_in_per / 100) * sub_total

        # Handle shipping cost
        shippingCost = ShippingCostSetting.objects.first()
        if not shippingCost:
            raise Http404("Shipping cost settings not found")
        
        if shippingCost.cost_apply_type == "Free":
            apply_shipping_cost = 0
        else:
            apply_shipping_cost = Decimal(shippingCost.cost_value) if shippingCost.cost_value else Decimal(0)

        # Total price calculation
        total_price = sub_total + apply_tax + apply_shipping_cost

    # Render the checkout page with context
    return render(request, 'pages/checkout.html', {
        'title': 'Check Out',
        'product_info': product_info,
        'quantity': quantity,
        'sub_total': sub_total,
        'apply_tax': apply_tax,
        'total_price': total_price,
        'taxSetting': taxSetting,
        'shippingCost': shippingCost
    })
   
# process To Payment
# def processToPayment(request):
#     return HttpResponse("Processing to payment...")

# process To Payment
@csrf_exempt
def processToPayment(request):
    if request.method == 'POST':
        order_id = random.randint(1000000000, 9999999999)
        data = request.POST
        product_id = data.get('product_id')
        product_price = data.get('product_price')
        shipping_type = data.get('shipping_type')
        shipping_cost = data.get('shipping_cost')
        tax_apply_type = data.get('tax_apply_type')
        tax_value = data.get('tax_value')
        tax_apply = data.get('total_apply_tax')
        total_pay_amount = data.get('total_pay_amount')
        print("Total Pay Amount:", total_pay_amount) 
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_no = data.get('phone_no')
        country = data.get('country')
        state = data.get('state')
        city = data.get('city')
        zip_code = data.get('zip_code')
        delivery_address = data.get('delivery_address')
        payment_method = data.get('payment_method') 
        deliveryData  = ProductDelivery.objects.create(
            product = Product.objects.get(id=product_id),
            product_price = product_price,
            shipping_type = shipping_type,
            shipping_cost = shipping_cost,
            tax_apply_type = tax_apply_type,
            tax_value = tax_value,
            tax_apply = tax_apply,
            total_price = total_pay_amount,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_no=phone_no,
            country=country,
            state=state,
            city=city,
            zip_code=zip_code,
            delivery_address=delivery_address,
            payment_method=payment_method
        )
        inserted_id = deliveryData.id 
        if payment_method == 'Cash On Delivery':
            order = ProductDelivery.objects.get(id=inserted_id)
            order.payment_status = 'Paid'
            order.order_id = str(order_id)+str(inserted_id)
            order.save()
            return JsonResponse({'success': True,'payment_method': payment_method,'order_id': order.order_id,'success_url': '/cod-success'}, status=200)
        elif payment_method == 'Razorpay':
            razorpaySetting = RazorpaySetting.objects.first()
            new_order_id = str(order_id)+str(inserted_id)
            amount_paise = int(float(total_pay_amount) * 100)
            client = razorpay.Client(auth=(razorpaySetting.razorpay_key_id, razorpaySetting.razorpay_secret_key))
            # Create Razorpay order
            razorpay_order = client.order.create({
                "amount": amount_paise,
                "currency": "INR",
                "receipt": f"order_rcptid_{new_order_id}",
                "payment_capture": 1
            })

            deliveryData.order_id = razorpay_order['id']
            deliveryData.save()
            return JsonResponse({
                'success': True,
                'payment_method': payment_method,
                'order_id': razorpay_order['id'],
                'razorpay_key_id': razorpaySetting.razorpay_key_id,
                'amount': total_pay_amount,
                'success_url': '/razorpay-success',
                'delivery_id': deliveryData.id,
                'gateway_mode': razorpaySetting.gateway_mode
            }, status=200)

    return JsonResponse({'status': 'error'}, status=400)

# Payment Success COD
def paymentSuccessCOD(request):
     return render(request,'pages/paymentSuccessCOD.html',{'title':'Payment Success'})

# Payment Success Razorpay
def paymentSuccessGateway(request):
     return render(request,'pages/paymentSuccess.html',{'title':'Payment Success'})

@csrf_exempt
@require_POST
def razorpay_success(request):
    data = json.loads(request.body)
    delivery_id = data.get('delivery_id')
    try:
        delivery = ProductDelivery.objects.get(id=delivery_id)
        delivery.payment_status = 'Paid'
        delivery.save()

        return JsonResponse({
            "redirect_url": "/payment-success"
        })
    except ProductDelivery.DoesNotExist:
        return JsonResponse({"error": "Invalid delivery ID"}, status=400)
     
        
