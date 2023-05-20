from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as loginUser
from django.contrib.auth.decorators import login_required
from .models import *
import json
from .forms import CutomerSingup, CustomerLogin, CutomerProfileForm, ProductForm, MerchantsProfileForm, RiderProfileForm, UpdatePriceForm
from django.contrib import messages
from django.views import View
from django.db.models import Q
# Create your views here.

def home(request):
    return render(request, 'base.html')


def login(request):
    if request.method == 'GET':
        form1 = CustomerLogin()
        context = {
            "form": form1
        }
        return render(request, 'login.html', context=context)
    else:
        form = CustomerLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                # Chuyển hướng tương ứng với từng vai trò
                if user.account.role == 'Customer':
                    return redirect('profile')
                elif user.account.role == 'Merchants':
                    return redirect('profilemerchants')
                elif user.account.role == 'Rider':
                    return redirect('profilerider')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    form = CutomerSingup()
    context = {
            "form": form
    }
    if request.method == 'GET':
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = CutomerSingup(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user = form.save()
            account = Account(user = user, role = role)
            account.save()
            messages.success(request, 'Đăng ký Thành Công !')
            # if user is not None:
            #     return redirect('login')
        else:
            messages.warning(request,'Đăng ký không thành công !')
        return render(request, 'signup.html', context=context)


def customer(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product.html',context)

class ProfileViews(View):
    def get(self, request):
        form  = CutomerProfileForm()
        return render(request, 'profile.html', locals())
    def post(self, request):
        form  = CutomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            phone = form.cleaned_data['phone']
            reg = Customer(user = user, name=name ,email=email,city=city,phone=phone,state=state, address=address)
            reg.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return render(request, 'profile.html', locals())

def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add =  Customer.objects.filter(user=request.user)
    return render(request,'address.html', locals())

class ProfileViewsMerchants(View):
    def get(self, request):
        form  = MerchantsProfileForm()
        return render(request, 'profilemerchants.html', locals())
    def post(self, request):
        form  = MerchantsProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            if not Merchants.objects.filter(user=user).exists():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                address_rd = form.cleaned_data['address_rd']
                phone = form.cleaned_data['phone']
                reg = Merchants(user = user, name=name ,email=email, address_rd=address_rd,phone=phone)
                reg.save()
                messages.success(request,'Lưu Thành Công')
            else:
                messages.warning(request, 'Bạn đã có địa chỉ vui lòng cập nhật trong Adderss')
        else:
            messages.warning(request,"Lỗi !!!!")
        return render(request, 'profilemerchants.html', locals())
    
def merchantsaddress(request):
    merchants =  Merchants.objects.filter(user=request.user)
    return render(request,'merchantsaddress.html', locals())

class updateAddressMerchants(View):
    def get(self, request, pk):
        merchants = Merchants.objects.get(pk=pk)
        form = MerchantsProfileForm(instance=merchants)
        return render(request,'updateaddrider.html', locals())
    def post(selff,request, pk):
        form = MerchantsProfileForm(request.POST)
        if form.is_valid():
            merchants = Merchants.objects.get(pk=pk)
            merchants.name = form.cleaned_data['name']
            merchants.email = form.cleaned_data['email']
            merchants.address_rd = form.cleaned_data['address_rd']
            merchants.phone = form.cleaned_data['phone']
            merchants.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return redirect('merchantsaddress')
    
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CutomerProfileForm(instance=add)
        return render(request,'updateaddress.html', locals())
    def post(selff,request,pk):
        form = CutomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.email = form.cleaned_data['email']
            add.address = form.cleaned_data['address']
            add.state = form.cleaned_data['state']
            add.city = form.cleaned_data['city']
            add.phone = form.cleaned_data['phone']
            add.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return redirect('address')


def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value= p.quantity * p.product.price
        amount = amount+value
    totalamount = amount + 30
    return render(request,  'addtocart.html', locals())


class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.price
            famount = famount + value
        totalamount = famount+30
        return render(request, 'checkout.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity+=1
        c.save()
        user =request.user
        cart = Cart.objects.filter(user=user)
        #print(prod_id)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        user =request.user
        cart = Cart.objects.filter(user=user)
        #print(prod_id)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.delete()
        user =request.user
        cart = Cart.objects.filter(user=user)
        #print(prod_id)
        amount = 0
        for p in cart:
            value= p.quantity * p.product.price
            amount = amount + value
        totalamount = amount + 30
        data = {
            'amount': amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def done(request):
    user = request.user
    customer = Customer.objects.filter(user=user).latest('id')
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('/orders')


def add_to_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def orders(request):
    order_placed = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'order.html', locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'about.html', locals())
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'contact.html', locals())
    

def search(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        searched = request.POST['searched']
        keys = Product.objects.filter(name = searched)
    return render(request, 'search.html', {'searched':search,'keys':keys})

def searchmerchants(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        user = request.user
        merchants = Merchants.objects.get(user = user)
        keys = Product.objects.filter(name = searched, merchants = merchants)
    return render(request, 'searchmer.html', {'searched':search,'keys':keys})


def rider(request):
    return render(request, 'rider.html')

def addproduct(request):
    submitted = False
    merchants = Merchants.objects.all()
    for merchant in merchants:
        if not isinstance(merchant.name, str):
            merchant.delete()
    if request.method == "POST":
        form= ProductForm (request.POST)
        if form.is_valid():
            user = request.user
            merchants = Merchants.objects.get(user=user)
            form.instance.merchants = merchants
            form.save()
            return HttpResponseRedirect ('/merchants?submitted= True')
    else: 
            form = ProductForm
            if 'submitted' in request.GET:
                submitted =True  
    form = ProductForm()
    return render(request, 'addproduct.html',{'form':form, 'submitted': submitted})

def merchants(request):
    user = request.user
    merchant = Merchants.objects.filter(user=user)
    name = 'temp'
    if not merchant:
        merchant = Merchants(user=user, name = name)
        merchant.save()
    merchants = Merchants.objects.get(user=user)
    products = Product.objects.filter(merchants=merchants)
    context = {'products': products}
    return render(request, 'productmerchants.html', context)



def rider(request):
    riders = Rider.objects.all()
    context = {'riders': riders}
    return render(request, 'rider.html',context)

def ordersmc(request):
    order_placed = OrderPlaced.objects.all()
    user = request.user
    merchants = Merchants.objects.get(user=user)
    products_added_by_merchant = Product.objects.filter(merchants=merchants)
    orders_with_products_added_by_merchant = []
    for order in order_placed:
        for productsadd in products_added_by_merchant:
            if order.product.name == productsadd.name:
                orders_with_products_added_by_merchant.append(order)
    return render(request, 'ordermc.html', {'orders': orders_with_products_added_by_merchant})


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = OrderPlaced.objects.get(id=order_id)
        order.status = new_status
        order.save()
        return redirect('ordersmc')
    else:
        order = OrderPlaced.objects.get(id=order_id)
        return render(request, 'update_order.html', {'order': order})




def ordersRider(request):
    orders = OrderPlaced.objects.all()
    return render(request, 'orderider.html', {'orders': orders})


def addrider(request):
    submitted = False
    if request.method == "POST":
        form= RiderProfileForm (request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect ('/merchants?submitted= True')
    else: 
            form = ProductForm
            if 'submitted' in request.GET:
                submitted =True  
    form = ProductForm
    return render(request, 'addproduct.html',{'form':form, 'submitted': submitted})
    


class ProfileViewsRider(View):
    def get(self, request):
        form  = RiderProfileForm()
        return render(request, 'profilerider.html', locals())
    def post(self, request):
        form  = RiderProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address_rd = form.cleaned_data['address_rd']
            phone = form.cleaned_data['phone']
            reg = Rider(user = user, name=name ,email=email, address_rd=address_rd,phone=phone)
            reg.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return render(request, 'profilerider.html', locals())
    
def rideraddress(request):
    riders =  Rider.objects.filter(user=request.user)
    return render(request,'rideraddress.html', locals())

class updateAddressRider(View):
    def get(self, request, pk):
        riders = Rider.objects.get(pk=pk)
        form = RiderProfileForm(instance=riders)
        return render(request,'updatemerchants.html', locals())
    def post(selff,request, pk):
        form = RiderProfileForm(request.POST)
        if form.is_valid():
            rider = Merchants.objects.get(pk=pk)
            rider.name = form.cleaned_data['name']
            rider.email = form.cleaned_data['email']
            rider.address_rd = form.cleaned_data['address_rd']
            rider.phone = form.cleaned_data['phone']
            rider.save()
            messages.success(request,'Lưu Thành Công')
        else:
            messages.warning(request,"Lỗi !!!!")
        return redirect('rideraddress')
    

def dashboardcus(request):
    user = request.user
    customer = Customer.objects.filter(user=user)
    orders = OrderPlaced.objects.filter(user = user)
    total_order = orders.count()
    dilivery = OrderPlaced.objects.filter(status = 'Delivered').count()
    pending = OrderPlaced.objects.filter(status = 'Pending').count()
    context = {
        'orders': orders,
        'customer': customer,
        'total_order':total_order,
        'dilivery': dilivery,
        'pending': pending,

    }
    return render(request, 'dashboardcustomer.html', context)


def cancel_order(request, order_id):
    order = OrderPlaced.objects.get(id=order_id)
    if order.status == 'Pending':
        order.status = 'Cancel'
        order.save()
        messages.success(request, "Bạn đã hủy đơn hàng thành công.")
    else:
        messages.error(request, "Bạn không thể hủy đơn hàng.")
    return redirect('dashboardcus')


def dashboardmer(request):
    user = request.user
    order_placed = OrderPlaced.objects.all()
    user = request.user
    merchants = Merchants.objects.get(user=user)
    products_added_by_merchant = Product.objects.filter(merchants=merchants)
    merchant = Merchants.objects.filter(user=user)
    count = 0
    total_cost = 0
    count1 = 0
    orders = []
    for order in order_placed:
        for productsadd in products_added_by_merchant:
            if order.product.name == productsadd.name:
                total_cost = total_cost + productsadd.price
                orders.append(order)
                if order.status == "Delivered":
                    count = count + 1
                else:
                    count1 = count1 + 1
    context = {
        'count': count,
        'total_cost': total_cost,
        'count1': count1,
        'orders': orders,
        'merchant': merchant
    }
    return render(request, 'dashboardmer.html', context)

from django.shortcuts import get_object_or_404
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('merchants')


def ridersave(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    rider = get_object_or_404(Rider, user=request.user)  # Assuming the rider is authenticated
    saved_order = RiderSavedOrders.objects.create(user=rider.user, rider=rider, name=rider.name, email=rider.email, xe=rider.xe, phone=rider.phone, address_rd=rider.address_rd)
    saved_order.order = order
    saved_order.save()
    return redirect('savedorders')

def savedorders(request):
    rider = get_object_or_404(Rider, user=request.user)  # Assuming the rider is authenticated
    saved_orders = RiderSavedOrders.objects.filter(rider=rider)
    return render(request, 'saveorder.html', {'saved_orders': saved_orders})

def update_price(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = UpdatePriceForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('merchants')
    else:
        form = UpdatePriceForm(instance=product)
    
    return render(request, 'updatepirce.html', {'form': form})