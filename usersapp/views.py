from django.shortcuts import render, redirect,loader,HttpResponse
from .models import *
from sellerapp.models import Product,Image,Size
# Create your views here.
def user_login(request):
    print(request.method)
    if request.method == "POST":
        usernames = request.POST.get("user_name")
        passwords = request.POST.get("password")
        user_data = User.objects.filter(user_name=usernames, password=passwords)
        if user_data:
            request.session['user_name'] = usernames
            return redirect('/')
        else:
            print("invalid")
            return render(request, 'user_login.html', {'status':"invalid"})
    return render(request, 'user_login.html')

def user_register(request):
    print(request.method)
    print("hrllo")
    if request.method == "POST":
        usernames = request.POST.get("user_name")
        print(usernames)
        emails = request.POST.get("email")
        passwords = request.POST.get("password")
        addresss = request.POST.get("address")
        phones = request.POST.get("phone_number")
        print("ppppp")
        data = User()
        data.user_name = usernames
        data.email = emails
        data.password = passwords
        data.address = addresss
        data.phone_number = phones
        data.save()
        print(usernames,emails,passwords,addresss,phones)
        return redirect('/')
    return render(request, 'user_register.html')

def welcome(request):
    if 'user_name' in request.session:
        user = request.session['user_name']
        print(user)
        user_data = User.objects.filter(user_name=user)
        return render(request, 'welcome.html',{'users':user_data})
    else:
        print("bye")
        return redirect('/user_login')

def logout(request):
    del request.session['user_name']
    return redirect('/user_login')

def home(request):
    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images').all()

    # Accessing the data
    for product in product_details:
        print(f"Product Name: {product.product_name}")
        print(f"Seller ID: {product.seller_id}")
        print(f"Subcategory ID: {product.subcategory_id}")

        # Accessing associated images
        for image in product.images.all():
            print(f"Image ID: {image.image_id}")
            print(f"Image URL: {image.image_file.url}")
    return render(request, 'home.html', {'product_details':product_details})

def view_product(request, id):
    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','sizes','shirts','kurtas','jeans','sarees','tshirts','westerns','boysdrss').filter(product_id=id)
    return render(request, 'view_product.html', {'product': product_details})

def view_cart(request, id):
    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','sizes').filter(product_id=id)
    return render(request, 'view_cart.html', {'product_details': product_details})




