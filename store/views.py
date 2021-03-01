from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from .models import Product, Profile, ShippingAddress, Cart, OrderList
from django.views import View
from .forms import UserRegistrationForm, ShippingAddressForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
import razorpay
from django.http import HttpResponse
from . import checksum
from django.conf import settings
from .utils import VerifyPaytmResponse
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=("rzp_test_DHiSVzftjW7gxG","X3uykk8LwzVSfIuVoOTn7oVS"))



class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['products'] = Product.objects.order_by('-quantity')[:10]
        context['deals'] = Product.objects.order_by('selling_price')[:10]
        return context


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'registration.html', {'form':form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Registration Succesfull!')
            form.save()
        return render(request, 'registration.html', {'form':form})
        


class ProductDetailView(View):
    

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        deals = Product.objects.filter(category=product.category)[:10]
        product_incart = False
        if request.user.is_authenticated:
            product_incart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        product_list = Product.objects.filter(brand='Adidas')[:10]

        return render(request, 'product_detail.html', {'deals':deals, 'product':product, 'product_incart':product_incart, 'product_list':product_list})

    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile.html'


class ShippingAddressView(View):
    def get(self, request):
        form = ShippingAddressForm()
        return render(request, 'shippingaddresscreate.html', {'form':form})
    
    def post(self, request):
        user = request.user
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            ad1 = form.cleaned_data['address_line_1']
            ad2 = form.cleaned_data['address_line_2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            country = form.cleaned_data['country']
            s = ShippingAddress.objects.create(user = user, address_line_1 = ad1, address_line_2 = ad2, city = city, state=state, zipcode=zipcode, country=country)
            messages.success(request, 'Address added Successfully.')
            s.save()
        return render(request, 'shippingaddresscreate.html', {'form':form})

class ShippingAddressListView(View):

    def get(self, request):
        if request.method == "GET":
            user = request.user
            addresses = ShippingAddress.objects.filter(user=user)
            print(addresses)
            return render(request, 'shipping_address_list.html', {'addresses':addresses})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    
    cart = Cart.objects.create(user=user, product=product)
    cart.save()
    return redirect('/cart')

@login_required()
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        if product_cart:
            for p in product_cart:
                tempcost = (p.quantity * p.product.selling_price)
                cost += tempcost
                total_cost = shipping_cost + cost
            return render(request, 'cart.html', {'carts':carts, 'cost':cost, 'total_cost':total_cost})
        
        else:
            return render(request, 'empty_cart.html')
    else:
        return render(request, 'empty_cart.html')


def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        
        carts = Cart.objects.filter(user=request.user)
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost
        data = {
            'quantity' : c.quantity,
            'cost': cost,
            'total_cost':total_cost
        }
        return JsonResponse(data)
            

def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        carts = Cart.objects.filter(user=request.user)
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost
        data = {
            'quantity' : c.quantity,
            'cost': cost,
            'total_cost':total_cost
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        product_id = request.GET['product_id']
        print(product_id)
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.delete()
        carts = Cart.objects.filter(user=request.user)
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost
        data = {
            'cost': cost,
            'total_cost': total_cost
        }
        return JsonResponse(data)

class CheckoutView(View):
    
    def get(self, request):
        user = request.user
        address = ShippingAddress.objects.filter(user=user)
        products = Cart.objects.filter(user=user)
        carts = Cart.objects.filter(user=request.user)
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost

        return render(request, 'checkout.html', {'address':address, 'products':products, 'cost':cost, 'total_cost':total_cost})

def search(request):
    query = request.GET['query']
    search_result = Product.objects.filter(name__icontains=query) 
    return render(request, 'search.html', {'search_result':search_result})


class CategoryView(View):

    def get(self, request, data=None):
        category_list = [p.category for p in Product.objects.all()]
        category_filtered = []
        for c in category_list:
            if c not in category_filtered:
                category_filtered.append(c)
        if data == None:
            product = Product.objects.all().order_by('selling_price')
        elif data in category_filtered:
            product = Product.objects.filter(category=data).order_by('selling_price')
        
        paginator = Paginator(product, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        return render(request, 'category.html',{'category_filtered':category_filtered, 'page_obj':page_obj})


class BrandView(View):

    def get(self, request, data=None):
        brand_list = [p.brand for p in Product.objects.all()]
        print(brand_list)
        brand_filtered = []
        for c in brand_list:
            if c not in brand_filtered:
                brand_filtered.append(c)
        print(brand_filtered)
        if data == None:
            products = Product.objects.all()
        elif data in brand_filtered:
            products = Product.objects.filter(brand=data)
            
        return render(request, 'brands.html',{'brand_filtered':brand_filtered, 'products':products})



class TrackingView(TemplateView):
    template_name = 'tracking.html'

class ConfirmationView(View):
    
    def get(self, request):
        user = request.user
        address_id = request.GET.get('address_id')
        address = ShippingAddress.objects.get(id=address_id)
        carts = Cart.objects.filter(user=request.user)
        for c in carts:
            OrderList(user=user, address=address, product=c.product, quantity=c.quantity).save()
            c.delete()
        
        shipping_cost = 200.0
        cost = 0.0
        product_cart = list(carts)
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost

        return render(request, 'confirmation.html', {'address':address, 'products':products, 'cost':cost, 'total_cost':total_cost})

class PaymentView(View):

    def get(self, request):
        user = request.user
        address_id = request.GET.get('address_id')
        address = ShippingAddress.objects.get(id=address_id)
        cart_items = Cart.objects.filter(user=request.user)
        product_cart = list(cart_items)
        shipping_cost = 200.0
        cost = 0.0
        for p in product_cart:
            tempcost = (p.quantity * p.product.selling_price)
            cost += tempcost
            total_cost = shipping_cost + cost
        order_amount = total_cost*100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {'Shipping Address': 'Indore'}

        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes))
        order_id = response['id']
        order_status = response['status']
        context = {}
        if order_status == 'created':
            context['order_id'] = order_id
            context['price'] = order_amount
            context['address'] = address
            context['total_cost'] = total_cost
            return render(request, 'payment.html', context)
        return HttpResponse('Order create error.')

def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }


    try:
        status = client.utility.verify_payment_signature(params_dict)
        return render(request, 'confirmation.html', {'status': 'Payment Successful'})
    except:
        return render(request, 'confirmation.html', {'status': 'Payment Faliure!!!'})


def paytm_payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=request.user)
    product_cart = list(cart_items)
    shipping_cost = 200.0
    cost = 0.0
    for p in product_cart:
        tempcost = (p.quantity * p.product.selling_price)
        cost += tempcost
        total_cost = shipping_cost + cost

    order_id = checksum.__id_generator__()
    bill_amount = str(total_cost)
    data_dict = {
        'MID': settings.PAYTM_MERCHANT_ID,
        'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
        'WEBSITE': settings.PAYTM_WEBSITE,
        'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
        'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
        'MOBILE_NO': '7405505665',
        'EMAIL': 'dhaval.savalia6@gmail.com',
        'CUST_ID': '123123',
        'ORDER_ID':order_id,
        'TXN_AMOUNT': bill_amount,
    }
    
    data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, settings.PAYTM_MERCHANT_KEY)
    context = {
        'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
        'comany_name': settings.PAYTM_COMPANY_NAME,
        'data_dict': data_dict
    }
    return render(request, 'payment_paytm.html', context)


@csrf_exempt
def response(request):
    user = request.user
    carts = Cart.objects.filter(user=request.user)
    OrderList(user=user, address=address, cart=carts).save()
    c.delete()
        
    shipping_cost = 200.0
    cost = 0.0
    product_cart = list(carts)
    for p in product_cart:
        tempcost = (p.quantity * p.product.selling_price)
        cost += tempcost
        total_cost = shipping_cost + cost
    resp = VerifyPaytmResponse(request)
    order_details = OrderList.objects.filter(user=user)
    if resp['verified']:
        return render(request, 'confirmation.html', {'order_details':order_details, 'address':address, 'carts':carts, 'cost':cost, 'total_cost':total_cost})
    else:
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)


class ElementsView(TemplateView):
    template_name = 'elements.html'

class LoginView(TemplateView):
    template_name = 'login.html'

class ContactView(TemplateView):
    template_name = 'contact.html'