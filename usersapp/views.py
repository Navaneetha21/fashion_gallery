from django.shortcuts import render, redirect, loader, HttpResponse
from .models import *
from sellerapp.models import Product, Image, Size
from django.db.models import Q
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
# Create your views here.


from django.db.models import Sum


def user_login(request):
    print(request.method)
    if request.method == "POST":
        usernames = request.POST.get("user_name")
        passwords = request.POST.get("password")
        user_data = User.objects.filter(user_name=usernames, password=passwords)
        if user_data:
            for x in user_data:
                id = x.user_id
            request.session['user_id'] = id
            return redirect('/')
        else:
            print("invalid")
            return render(request, 'user_login.html', {'status': "invalid"})
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
        # profile=Profile.objects.create(data=data, phone_number=phones)
        data.user_name = usernames
        data.email = emails
        data.password = passwords
        data.address = addresss
        data.phone_number = phones
        data.save()
        print(usernames, emails, passwords, addresss, phones)
        return redirect('/')
    return render(request, 'user_register.html')


def welcome(request):
    if 'user_name' in request.session:
        user = request.session['user_name']
        print(user)
        user_data = User.objects.filter(user_name=user)
        return render(request, 'welcome.html', {'users': user_data})
    else:
        print("bye")
        return redirect('/user_login')


def logout(request):
    del request.session['user_id']
    return redirect('/user_login')


def home(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','review','sizes','cart','shirts','offer','kurtas','jeans','sarees','tshirts','westerns','boysdrss').all()
        if request.method == "POST":
            search = request.POST.get('product_name')
            if search:
                product_details = Product.objects.filter(Q(product_name__icontains=search)|Q(price__icontains=search))
                return render(request, 'search.html', {'search': product_details})
        elif 'price' in request.GET:
            price = request.GET.get('price')
            product_details = Product.objects.filter(price=price)
            return render(request, 'search.html', {'search': product_details})
        return render(request, 'home.html', {'product_details': product_details})
    else:
        return redirect('/user_login')


def view_product(request, id):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images','review','sizes','cart','shirts','kurtas','jeans','sarees','tshirts','westerns','boysdrss').filter(product_id=id)
        if request.method == "POST":
            quantities = request.POST.get('quantity')
            data = Cart()
            data.user_id = User.objects.get(user_id=user_id)
            data.product_id = Product.objects.get(product_id=id)
            data.quantity = quantities
            data.save()
            return redirect('/view_cart')
        return render(request, 'view_product.html', {'product': product_details})
    else:
        return redirect('/user_login')


def view_cart(request):
    if 'user_id' in request.session:
        product_details = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product_details.values()
        print(data)

        total_price = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id'])).aggregate(
            total_price=Sum(F('product_id__price') * F('quantity'), output_field=models.DecimalField())
        )['total_price'] or Decimal('0.00')
        print(f"Total price for user : ₹{total_price}")

        return render(request, 'view_cart.html',{'cart': product_details, 'total_price': total_price})
    else:
        return redirect('/user_login')


def profile(request):
    if 'user_id' in request.session:
        user = request.session['user_id']
        data = User.objects.filter(user_id=user)
        return render(request, 'profile.html', {'users': data})
    else:
        return redirect('/user_login')


def address(request):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            house = request.POST.get("house_name")
            city = request.POST.get("city_name")
            land = request.POST.get("landmark")
            states = request.POST.get("state")
            districts = request.POST.get("district")
            post = request.POST.get("post_office")
            pins = request.POST.get("pin")
            data = Address()
            data.house_name = house
            data.city_name = city
            data.landmark = land
            data.state = states
            data.district = districts
            data.post_office = post
            data.pin = pins
            data.user_id = User.objects.get(user_id=user_id)
            data.save()
            print(house, city, land, states, districts, post, pins)
            return redirect('/view_address')
        return render(request, 'address.html')
    else:
        return redirect('/user_login')


def viewaddress(request):
    if 'user_id' in request.session:
        add = Address.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'view_address.html', {'adds': add})
    else:
        return redirect('/user_login')


def editaddress(request, address_id):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            house = request.POST.get("house_name")
            city = request.POST.get("city_name")
            land = request.POST.get("landmark")
            states = request.POST.get("state")
            districts = request.POST.get("district")
            post = request.POST.get("post_office")
            pins = request.POST.get("pin")
            data = Address.objects.get(address_id=address_id)
            data.house_name = house
            data.city_name = city
            data.landmark = land
            data.state = states
            data.district = districts
            data.post_office = post
            data.pin = pins
            data.user_id = User.objects.get(user_id=user_id)
            data.save()
            print(house, city, land, states, districts, post, pins)
            return redirect('/view_address')
        data = Address.objects.filter(address_id=address_id)
        return render(request, 'edit_address.html', {'datas': data})
    else:
        return redirect('/user_login')


def remove(request, address_id):
    product_data = Address.objects.get(address_id=address_id)
    product_data.delete()
    return redirect('/view_address')


def addreview(request, product_id):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        product = Product.objects.filter(product_id=product_id)
        if request.method == "POST":
            review = request.POST.get("review")
            product_id = request.POST.get("product_id")
            data = Review()
            data.review = review
            data.user_id = User.objects.get(user_id=user_id)
            data.product_id = Product.objects.get(product_id=product_id)
            data.save()
            return redirect('/view_product')
        return render(request, 'review.html', {'products': product})
    else:
        return redirect('/user_login')


def review(request):
    if 'user_id' in request.session:
        review = Review.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'review.html', {'reviews': review})
    else:
        return redirect('/user_login')


def removes(request, cart_id):
    product_data = Cart.objects.get(cart_id=cart_id)
    product_data.delete()
    return redirect('/view_cart')


def wishlist(request):
    if 'user_id' in request.session:
        product_details = Wishlist.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product_details.values()
        print(data)
        return render(request, 'wishlist.html', {'wishlist': product_details})
    else:
        return redirect('/user_login')


def search(request):
    if 'user_id' in request.session:
        data = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images', 'review','sizes', 'cart', 'shirts','kurtas', 'jeans','sarees', 'tshirts','westerns','boysdrss').filter(product_id=id)
        subcategory = Product.objects.all()
        if request.method == 'POST':
            search = request.POST.get("product_name")
            if search:
                data = Product.objects.filter(
                    Q(product_name__icontains=search) | Q(price__icontains=search) | Q(subcategory__icontains=search))
        return render(request, 'search.html', {'search': data, 'datas': data})
    else:
        return redirect('/user_login')

def about(request):
    about=loader.get_template('about.html')
    return HttpResponse(about.render())
