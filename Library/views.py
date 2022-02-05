from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from .forms import UserSignUpForm,UserInfo,UserFLEname
from .models import Book_category,Book,Book_package,User_info,Online_read_pack,Online_read_book_list,Order
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,UpdateView
from django.views import View

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

class Index(View):
    def get(self,request):
        all_pack = Book_package.objects.all() 
        context = {
            'book_pack':all_pack,
        }
        return render(request,'index.html',context)    


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('successfully login in')
                return redirect('home')
            else:
                return render(request,'account/login.html')
        else:
            return render(request,'account/login.html')
    else:
        return redirect('home')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

def signup_view(request):
    form = UserSignUpForm()
    form1 = UserInfo()
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        form1 = UserInfo(request.POST , request.FILES or None)        

        if form.is_valid() and form1.is_valid():
            print(form1.cleaned_data['profile_pic'])
            userform = form.save()
            userinfo = form1.save(commit=False)
            userinfo.user = userform
            userinfo.save()
            return redirect('login')    

    return render(request,'account/signup.html',context={'form':form,'form1':form1})

class Shop(View):
    def get(self,request):
        book_list = None
        categoryID = request.GET.get('category')
        if categoryID:
            book_list = Book.objects.filter(category__id=categoryID)
        else:
            book_list = Book.objects.all()
        all_category = Book_category.objects.all()

        # this query for pagination
        productview = request.GET.get('productview', 1)
        home_paginator = Paginator(book_list, 12)
        try:
            products_list = home_paginator.page(productview)
        except PageNotAnInteger:
            products_list = home_paginator.page(1)
        except EmptyPage:
            products_list = home_paginator.page(home_paginator.num_pages)
        # end pagination query

        context = {
            'books':products_list,
            'categories':all_category,
        }
        return render(request,'shop.html',context)

    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            item = cart.get(product)
            if item:
                if remove:
                    if item<=1:
                        cart.pop(product)
                    else:
                        cart[product] = item-1
                else:
                    cart[product] = item+1
            else:
                cart[product] = 1
        
        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart

        book_list = Book.objects.all()
        print('product:',request.session.get('cart'))
        return render(request,'shop.html',{'books':book_list})


class Add_to_cart(View):
    def post(self,request):
            product = request.POST.get('product')
            remove = request.POST.get('remove')
            cart = request.session.get('cart')
            if cart:
                item = cart.get(product)
                if item:
                    if remove:
                        if item<=1:
                            cart.pop(product)
                        else:
                            cart[product] = item-1
                    else:
                        cart[product] = item+1
                else:
                    cart[product] = 1
            
            else:
                cart = {}
                cart[product] = 1
            
            request.session['cart'] = cart
            url = f'/details/{product}/'

            print(url)
            return redirect(url)

@login_required(redirect_field_name='login')
def user_profile(request):
    user = request.user
    read_pack = Online_read_pack.objects.filter(user=user)
    
    # total book from pack
    total_book = int()
    for i in read_pack:
        total_book += i.book_pack.max_book
        print(type(i.book_pack.max_book))
        print(total_book)
    # get user
    user_profile = User_info.objects.get(user=user)
    # filter book taken user
    read_book_list = Online_read_book_list.objects.filter(user=user)

    max_book = total_book-read_book_list.count()
    context = {
        'user':user,
        'profile':user_profile,
        'read_pack':read_pack,
        "total_book":total_book,
        'read_book_list':read_book_list,
        "max_book":max_book,
    }
    return render(request,'dashboard.html',context)

def book_details(request,id):
    book = get_object_or_404(Book,id=id)
    return render(request,'book_details.html',{'book':book})

# take online read book pack
@login_required(redirect_field_name='login')
def my_pack(request):
    if request.method == "POST":
        pack_id = request.POST['pack_id']
        traxid = request.POST['traxid']

        pack = Book_package.objects.get(id=pack_id)
        c_user = request.user
        
        mypac =  Online_read_pack(user = c_user,book_pack = pack,payment_traxid = traxid )
        mypac.save()
        return redirect('profile')
    else:
        return redirect('home')

# take book for online
@login_required(redirect_field_name='login')
def book_take(request,id):
    book = get_object_or_404(Book,id=id)
    c_user = request.user
    getbook = Online_read_book_list.get_orders_by_Id(id)
    pack_exits = Online_read_pack.get_orders_by_user(request.user)
    print(getbook)
    if pack_exits:
        if getbook:
            return HttpResponse("Already exits")
        else:
            mybook = Online_read_book_list(user= c_user,book_list=book)
            print(mybook)
            mybook.save()
    else:
        return redirect('home')
    return redirect('profile')


class Cart(View):
    def get(self,request):
        mycart = request.session.get('cart')
        if mycart:
            ids = list(request.session.get('cart').keys())
            books = Book.get_books_by_id(ids)
            return render(request,'cart.html',{'books':books})
        else:
            request.session['cart'] = {}
            ids = list(request.session.get('cart').keys())
            books = Book.get_books_by_id(ids)
            return render(request,'cart.html',{'books':books})


class IncDec(View):
    def post(self,request):
        product = request.POST.get('productid')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
        return redirect('cart')


class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        bkashtrxid = request.POST.get('bkashtrxid')
        phone = request.POST.get('phone')
        customer = request.user
        cart = request.session.get('cart')
        products = Book.get_books_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products,bkashtrxid)

        for product in products:
            # print(cart.get(str(product.id)))
            order = Order(customer=customer,
                          product=product,
                          price=product.price,
                          bkashTrxID=bkashtrxid,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            print(customer,product,product.price,address,phone,cart.get(str(product.id)),bkashtrxid)
        request.session['cart'] = {}

        return redirect('cart')



class OrderView(View):
    # @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.user
        orders = Order.get_orders_by_customer(customer) 
        print(orders)
        return render(request,'order.html',{'orders':orders})


class ProductSearch(View):
    def get(self,request):  
        context = {}  
        mysearch = request.GET.get('search')
        context['mysearch'] = mysearch

        products = None

        categories = Book_category.objects.all()
        context['categories'] = categories

        categoryID = request.GET.get('category')
        message = None
        # here get product by search name
        if mysearch:
            myproductsearch = Book.objects.filter(book_name__icontains=mysearch)
            if myproductsearch:
                products=myproductsearch
            else:
                message = 'Search not found'
        else:
            if categoryID:
                products = Book.objects.filter(category__id=categoryID)
            else:
                products = Book.objects.all()
        # here check froduct or not th
        if message:
            context['message'] = message
        else:
            
            # this query for pagination
            productview = request.GET.get('productview', 1)
            home_paginator = Paginator(products, 12)
            try:
                products_list = home_paginator.page(productview)
                context['books'] = products_list
            except PageNotAnInteger:
                products_list = home_paginator.page(1)
                context['books'] = products_list
            except EmptyPage:
                products_list = home_paginator.page(home_paginator.num_pages)
                context['books'] = products_list
            # end pagination query

        return render(request,'shop.html',context)

@login_required(redirect_field_name='login')
def EditUserInfo(request):
    if request.method == 'POST':
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfo( request.POST, request.FILES or None, instance=mydata)
        form1 = UserFLEname( request.POST, request.FILES or None, instance=user)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
        return redirect('profile')
    else:
        mydata = User_info.objects.get(user=request.user)
        user = User.objects.get(username=request.user.username)
        form = UserInfo(instance=mydata)
        form1 = UserFLEname(instance=user)
    context={
        'form':form,
        'form1':form1,
    }
    return render(request,'editinfo.html',context)


@login_required(redirect_field_name='login')
def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # user = form.save()
            # update_session_auth_hash(request, user) 
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'changepass.html', {'form': form})

# need to work on 
# 1) Change password

