from django.shortcuts import render, redirect, loader, HttpResponse
from .models import *
from sellerapp.models import Product, Image, Size
from django.db.models import Q
from django.db.models import Sum, F, DecimalField
from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
# import requests


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
            print(request.session['user_id'])
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
    recent_visits = request.session.get('recent_visits', [])
    recent_product = Product.objects.filter(product_id__in=recent_visits)[:4]
    product_map = {product.product_id: product for product in recent_product}
    ordered_products = [product_map[product_id] for product_id in recent_visits if product_id in product_map]
    recent_product = ordered_products[:4]

    print(recent_visits)

    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images', 'review','sizes', 'cart','shirts', 'offer','kurtas', 'jeans','sarees','tshirts','westerns','boysdrss').all()
    product = Product.objects.all().order_by('-created_date')[:4]
    maincategory = MainCategory.objects.all()
    men_product_details = Product.objects.prefetch_related('images').filter(
        subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="FGMC-001"))[:4];
    womens_details = Product.objects.prefetch_related('images').filter(
        subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="FGMC-002"))[:4];
    kids_details = Product.objects.prefetch_related('images').filter(
        subcategory_id__maincategory_id=MainCategory.objects.get(maincategory_id="FGMC-003"))[:4];

    if request.method == "POST":

        product = Product.objects.all()
        print(product)
        search = request.POST.get('product_name')
        response = render(request, 'home.html', {'product': product, 'recent_view': recent_product})
        if search:
            product_details = Product.objects.filter(Q(product_name__icontains=search) | Q(price__icontains=search))
            return render(request, 'search.html', {'search': product_details})

    elif 'price' in request.GET:
        price = request.GET['price']
        product_details = Product.objects.filter(price__lte=int(price))
        return render(request, 'search.html', {'search': product_details})
    return render(request, 'home.html', {'product_details': product_details, 'main': maincategory, 'arrival': product,'mens': men_product_details, 'womens': womens_details, 'kids': kids_details,'recent_view': recent_product})


def view_product(request, product_id):
    maincategory = MainCategory.objects.all()
    product_details = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images', 'review', 'sizes', 'cart', 'shirts', 'kurtas','jeans', 'sarees','tshirts','westerns','boysdrss').filter(product_id=product_id)
    recent_visits = request.session.get('recent_visits', [])
    print(recent_visits)

    recent_visits.insert(0, product_id)
    print(recent_visits)
    recent_visits = list(set(recent_visits))
    request.session['recent_visits'] = recent_visits

    if request.method == "POST":
        if 'user_id' in request.session:
            user_id = request.session.get("user_id")
            print(user_id)
            print("user session exists")

            if 'add_to_cart' in request.POST:
                quantity = request.POST.get('quantity')
                data = Cart()
                data.user_id = User.objects.get(user_id=user_id)
                data.product_id = Product.objects.get(product_id=product_id)
                data.quantity = quantity
                data.save()
                return redirect('/view_cart')
            elif 'buy_now' in request.POST or "order_btn" in request.POST:
                print("buy this")
                quantity = request.POST.get('quantity')
                address = Address.objects.filter(user_id=User.objects.get(user_id=user_id))
                if request.method == "POST" and request.POST.get('not_go') != "Nooo":
                    quantity = request.POST.get('quantity')
                    address_id = request.POST.get('address')
                    data = Order()
                    data.user_id = User.objects.get(user_id=user_id)
                    data.quantity = quantity
                    data.product_id = Product.objects.get(product_id=product_id)
                    data.address_id = Address.objects.get(address_id=address_id)
                    data.save()
                    return redirect('/')
                return render(request, 'order.html',{'order':product_details,'address':address,"quantity":quantity})
        else:
            return redirect('/user_login')

    return render(request, 'view_product.html', {'product': product_details, 'main': maincategory})


def more(request):
    more = Product.objects.all()
    return render(request, 'moreproduct.html', {'mores': more})


def view_cart(request):
    if 'user_id' in request.session:
        product_details = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product_details.values()
        print(data)

        total_price = Cart.objects.filter(user_id=User.objects.get(user_id=request.session['user_id'])).aggregate(
            total_price=Sum(F('product_id__price') * F('quantity'), output_field=models.DecimalField())
        )['total_price'] or Decimal('0.00')
        print(f"Total price for user : ₹{total_price}")

        return render(request, 'view_cart.html', {'cart': product_details, 'total_price': total_price})
    else:
        return redirect('/user_login')


def order(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        product = Order.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product.values()
        print(data)
        total_price = Order.objects.filter(user_id=User.objects.get(user_id=request.session['user_id'])).aggregate(
            total_price=Sum(F('product_id__price') * F('quantity'), output_field=models.DecimalField())
        )['total_price'] or Decimal('0.00')
        print(f"Total price for user : ₹{total_price}")
        return render(request, 'order.html', {'products': product, 'address': address, 'total_price': total_price})
    else:
        return redirect('/user_login')


def view_order(request):
    if 'user_id' in request.session:
        product_details = Order.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        data = product_details.values()
        print(data)
        new_order = Order.objects.filter(status='pending').order_by('-ordered_date')
        delivered_order = Order.objects.filter(status='active').order_by('-ordered_date')
        cancelled_order = Order.objects.filter(status='cancel').order_by('-ordered_date')
        return render(request, 'view_order.html',
                      {'orders': product_details, 'new': new_order, 'deliver': delivered_order,
                       'cancel': cancelled_order})
    else:
        return redirect('/user_login')


def cancel(request, order_id):
    if 'user_id' in request.session:
        order = Order.objects.get(order_id=order_id)
        order.status = 'cancel'
        order.save()
        return redirect('/view_order')
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
            data = Review()
            data.review = review
            data.user_id = User.objects.get(user_id=user_id)
            data.product_id = Product.objects.get(product_id=product_id)
            data.save()
            return redirect(f'/view_product/{product_id}')
        return render(request, 'review.html', {'products': product})
    else:
        return redirect('/user_login')


def review(request):
    if 'user_id' in request.session:
        review = Review.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'review.html', {'reviews': review})
    else:
        return redirect('/user_login')

# def removereview(request, user_id):
#     if 'user_id' in request.session:
#         data = Review.objects.get(user_id=user_id)
#         data.delete()
#         return redirect('/view_product')


def removes(request, cart_id):
    product_data = Cart.objects.get(cart_id=cart_id)
    product_data.delete()
    return redirect('/view_cart')


def wishlist(request):
    if 'user_id' in request.session:
        product_details = Wishlist.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        maincategory = MainCategory.objects.all()
        data = product_details.values()
        print(data)
        return render(request, 'wishlist.html', {'wishlist': product_details, 'main': maincategory})
    else:
        return redirect('/user_login')


def search(request):
    print('search funtn working')
    maincategory = MainCategory.objects.all()
    data = Product.objects.select_related('seller_id', 'subcategory_id').prefetch_related('images', 'review', 'sizes','cart', 'shirts', 'kurtas','jeans', 'sarees', 'tshirts','westerns', 'boysdrss').all()
    # maincategory = MainCategory.objects.prefetch_related('main').all()
    if request.method == "POST":
        search = request.POST.get('product_name')
        sort_option = request.POST.get('sort_option')
        sort_discount = request.POST.get('sort_discount')
        sort_arrival = request.POST.get('sort_arrival')
        print(sort_arrival)
        if sort_option and search:
            data = Product.objects.filter(Q(product_name__icontains=search) | Q(price__icontains=search) |Q(description__icontains=search)  |Q(materials__icontains=search) |Q(subcategory_id__subcategory_name__icontains=search)| Q(subcategory_id__maincategory_id__maincategory_name__icontains=search))
            data = data.filter(price__lte=int(sort_option))
            print(search)
        elif sort_arrival and search:
            print('create with')
            data = Product.objects.filter(
                Q(product_name__icontains=search) | Q(price__icontains=search) | Q(description__icontains=search) | Q(
                    materials__icontains=search) | Q(subcategory_id__subcategory_name__icontains=search) | Q(
                    subcategory_id__maincategory_id__maincategory_name__icontains=search))

            data = data.order_by('-created_date')
        elif sort_discount and search:
            data = Offer.objects.filter(discount__lte=int(sort_discount))
            data = data.filter(product_id__product_name__icontains=search)
            return render(request, 'search.html', {'searchs': data})
        elif search:
            data = Product.objects.filter(
                Q(product_name__icontains=search) | Q(price__icontains=search) | Q(description__icontains=search) | Q(
                    materials__icontains=search) | Q(subcategory_id__subcategory_name__icontains=search) | Q(
                    subcategory_id__maincategory_id__maincategory_name__icontains=search))
        return render(request, 'search.html', {'search': data,'main': maincategory})
    return render(request, 'search.html', {'search': data, 'main': maincategory})


def about(request):
    about = loader.get_template('about.html')
    return HttpResponse(about.render())


def category(request, maincategory_id):
    maincategory = MainCategory.objects.all()
    maincategory_instance = MainCategory.objects.get(maincategory_id=maincategory_id)
    product_details = Product.objects.prefetch_related('images').filter(
        subcategory_id__maincategory_id=maincategory_instance)
    if request.method == "POST":
        sort_option = request.POST.get('sort_option')
        sort_discount = request.POST.get('sort_discount')
        sort_arrival = request.POST.get('sort_arrival')
        if sort_option == 'low_to_high':
            product_details = product_details.order_by('price')
        elif sort_option == 'high_to_low':
            product_details = product_details.order_by('-price')
        elif sort_arrival:
            product_details = Product.objects.prefetch_related('images').filter(
                subcategory_id__maincategory_id=maincategory_instance)
            product_details = product_details.order_by('-created_date')
        elif sort_discount:
            product_details = Offer.objects.filter(discount__lte=int(sort_discount))
            product_details = product_details.filter(product_id__subcategory_id__maincategory_id=maincategory_instance)
            return render(request, 'page.html', {'products': product_details})
    return render(request, 'page.html', {'product_detail': product_details, 'main': maincategory})


def discount(request):
    discount = Offer.objects.all()
    return render(request, 'discount_sale.html', {'discount': discount})

# def checkout(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         currency = request.POST.get('currency')
#
#         payment_data = {
#             'amount': amount,
#             'currency': currency,
#         }
#         headers = {
#             'Authorization': 'Bearer ' + settings.PAYMENT_API_KEY,
#             'Content-Type': 'application/json'
#         }
#         payment_response = requests.post(settings.PAYMENT_API_URL, json=payment_data, headers=headers)
#
#         if payment_response.status_code == 200:
#             return JsonResponse({'message': 'Payment successful'})
#         else:
#             return JsonResponse({'message': 'Payment failed'}, status=400)
#
#     return render(request, 'checkout.html')