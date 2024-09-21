from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from . models import Product, Customer, Cart, OrderPlaced, Wishlist, Payment
from django.db.models import Count
from . forms import CustomerRegistationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import random
# Create your views here.

@login_required
def home(request):
  totalitem = 0
  wishitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))
  return render(request, "app/home.html",locals())

@login_required
def about(request):
  totalitem = 0
  wishitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))
  return render(request, "app/about.html",locals())

@login_required  
def contact(request):
  totalitem = 0
  wishitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))
  return render(request, "app/contact.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
  def get(self,request,val):
    
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/category.html",locals())

@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
  def get(self,request,val):
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values('title')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/category.html",locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
  def get(self, request,pk):
    product = Product.objects.get(pk=pk)
    wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
    totalitem = 0
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/productdetail.html",locals())


class CustomerRegistationView(View):
  def get(self, request):
    form = CustomerRegistationForm()
    return render(request,"app/customerregistration.html",locals())
  def post(self, request):
    form = CustomerRegistationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Congratulations! User Register Successfully")
    else:
      messages.warning(request, "Invalid Input Data")
    return render(request,"app/customerregistration.html", locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html',locals())
  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():

      user = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      mobile = form.cleaned_data['mobile']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=user, name = name, locality = locality, city = city, mobile = mobile, state = state, zipcode= zipcode)
      reg.save()
      messages.success(request, "Profile ban da luu")
    else:
      messages.warning(request, "Moi ban nhap du lieu")
    return render(request, 'app/profile.html',locals())

@login_required  
def address(request):
  totalitem = 0
  wishitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))
 
  add = Customer.objects.filter(user = request.user)   
  return render(request, 'app/address.html',locals()) 

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
  def get(self, request,pk):
    add = Customer.objects.get(pk=pk)
    form = CustomerProfileForm(instance= add)
    return render(request, 'app/updateAddress.html',locals())
  def post(self, request,pk):
    form = CustomerProfileForm(request.POST)
    
    if form.is_valid():
      add = Customer.objects.get(pk=pk)
      add.name = form.cleaned_data['name']
      add.locality = form.cleaned_data['locality']
      add.city = form.cleaned_data['city']
      add.mobile = form.cleaned_data['mobile']
      add.state = form.cleaned_data['state']
      add.zipcode = form.cleaned_data['zipcode']
      add.save()
      messages.success(request, "Ho so ban da cap nhat")
    else:
        messages.warning(request, "Nhap data vao")
    return redirect('address')

@login_required  
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)

    # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng chưa
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        # Nếu sản phẩm đã tồn tại, tăng số lượng
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Nếu sản phẩm chưa tồn tại, tạo mới
        cart_item.save()

    return redirect("/cart")

@login_required  
def show_cart(request):
  totalitem = 0
  wishitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))
 
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'app/addtocart.html', locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Wishlist.objects.filter(user=user)

    return render(request, "app/wishlist.html", locals())


@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = famount + 40  # Assuming a fixed shipping fee of 40
        return render(request, 'app/checkout.html', locals())

    def post(self, request):
        user = request.user
        cust_id = request.POST.get('custid')  # Get the selected address ID from the form

        if not cust_id:
            messages.warning(request, "Please select a shipping address.")
            return redirect('checkout')

        try:
            customer = Customer.objects.get(id=cust_id, user=user)
        except Customer.DoesNotExist:
            messages.warning(request, "Invalid shipping address selected.")
            return redirect('checkout')

        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('checkout')

        famount = sum(item.quantity * item.product.discounted_price for item in cart_items)
        totalamount = famount + 40  # Shipping fee

        # Generate a unique order_id
        order_id = f"ORDER{random.randint(100000, 999999)}"

        # Create a Payment record
        payment = Payment.objects.create(
            user=user,
            amount=totalamount,
            order_id=order_id,
            payment_status='Success',  # In a real scenario, integrate with a payment gateway to get actual status
            paid=True
        )

        # Create OrderPlaced records for each cart item
        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                payment=payment
            )

        # Clear the cart
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully.")
        return redirect('orders')





@login_required  
def calculate_total(user):
    # """
    # Hàm tính tổng tiền trong giỏ hàng.
    # """
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount += value
    totalamount = amount + 40  # Phí vận chuyển cố định là 40
    return amount, totalamount

@login_required  
def orders(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 
  order_placed = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        
    return JsonResponse(data)




def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        
    return JsonResponse(data)





def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        
    return JsonResponse(data)



def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            "message": "Wishlist Added Successfully",
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            "message": "Wishlist Remove Successfully",
        }
        return JsonResponse(data)


def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    product = Product.objects.filter(Q(title__icontains=query))
    
    return render(request, "app/search.html", locals())
