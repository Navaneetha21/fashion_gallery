from django.shortcuts import render, redirect,loader,HttpResponse
from .models import *
# Create your views here.
def seller_login(request):
    print(request.method)
    print("lll")
    if request.method == "POST":
        usernames = request.POST.get("seller_name")
        passwords = request.POST.get("password")

        user_data = Seller.objects.filter(seller_name=usernames, password=passwords)
        if user_data:
            for x in user_data:
                id=x.seller_id

            request.session['seller_id'] = id
            return redirect('/seller/seller_page')
        else:
            print("invalid")
            return render(request, 'seller_login.html', {'status':"invalid"})
    return render(request, 'seller_login.html')

def seller_register(request):
    print(request.method)
    print("hrllo")
    if request.method == "POST":
        usernames = request.POST.get("seller_name")
        emails = request.POST.get("email")
        passwords = request.POST.get("password")
        addresss = request.POST.get("address")
        phones = request.POST.get("phone_number")
        licenses =request.POST.get("license_number")
        print("ppppp")
        data = Seller()
        data.seller_name = usernames
        data.email = emails
        data.password = passwords
        data.address = addresss
        data.phone_number = phones
        data.license_number = licenses
        data.save()
        print(usernames,emails,passwords,addresss,phones,licenses)
        return redirect('/seller/seller_login')
    return render(request, 'seller_register.html')

def add_product(request):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        print(seller_id)
        subcategories=SubCategory.objects.all()
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            print(seller_id)
            products = request.POST.get("product_name")
            descriptions = request.POST.get("description")
            quantities = request.POST.get("quantity")
            material = request.POST.get("materials")
            patterns = request.POST.get("pattern")
            prices = request.POST.get("price")
            subcategory_id = request.POST.get("subcategory")
            data = Product()
            data.product_name = products
            data.description = descriptions
            data.quantity = quantities
            data.materials = material
            data.pattern = patterns
            data.price = prices
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.subcategory_id = SubCategory.objects.get(subcategory_id=subcategory_id)
            data.save()
            return redirect('/')
        return render(request, 'add_product.html',{'subcategory':subcategories})
    else:
        return redirect('/seller/seller_login')

def viewpdct(request):
    product_data = Product.objects.all()
    return render(request, 'view_producttable.html', {'product': product_data})
def remove(request,product_id):
    print("remove fun called")
    product_data = Product.objects.get(product_id=product_id)
    product_data.delete()
    return redirect('/seller/view_producttable')


def edit(request, product_id):
    if 'seller_id' in request.session:
        seller_id = request.session.get("seller_id")
        print(seller_id)
        subcategories = SubCategory.objects.all()
        if request.method == "POST":
            seller_id = request.session.get("seller_id")
            print(seller_id)
            products = request.POST.get("product_name")
            descriptions = request.POST.get("description")
            quantities = request.POST.get("quantity")
            material = request.POST.get("materials")
            patterns = request.POST.get("pattern")
            prices = request.POST.get("price")
            subcategory_id = request.POST.get("subcategory")
            data = Product.objects.get(product_id=product_id)
            data.product_name = products
            data.description = descriptions
            data.quantity = quantities
            data.materials = material
            data.pattern = patterns
            data.price = prices
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.subcategory_id = SubCategory.objects.get(subcategory_id=subcategory_id)
            data.save()
            return redirect('/view_producttable')
        product_data = Product.objects.filter(product_id=product_id)
        return render(request, 'edit_product.html', {'product': product_data,'subcategory': subcategories})
    else:
        return redirect('/seller/seller_login')

def image(request, product_id):
    if 'seller_id' in request.session:
        product = Product.objects.filter(product_id=product_id)
        print("hello image")
        if request.method == "POST":
            print("hello post")
            print(f'{product_id}')
            seller_id = request.session.get("seller_id")
            product_image = request.FILES.get("product_image")
            data = Image()
            data.image_file = product_image
            data.seller_id = Seller.objects.get(seller_id=seller_id)
            data.product_id = Product.objects.get(product_id=product_id)
            data.save()
            return redirect('/')
        return render(request, 'image.html', {'product': product})
    else:
        return render(request, 'seller_login.html')

def seller_home(request):
    if 'seller_id' in request.session:
        seller = request.session['seller_id']
        print(seller)
        data = Seller.objects.filter(seller_id=seller)
        return render(request, 'seller_page.html', {'sellers': data})
    else:
        print("bye")
        return redirect('/seller/seller_login')

def seller_logout(request):
    del request.session['seller_id']
    return redirect('/seller/seller_login')

def product(request):
    if 'seller_id' in request.session:
        seller = request.session['seller_id']
        print(seller)
        data = Seller.objects.filter(seller_id=seller)
        return render(request, 'product.html', {'sellers': data})
    else:
        print("bye")
        return redirect('/seller/seller_login')