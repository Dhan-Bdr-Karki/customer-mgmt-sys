from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.models import Group

from .models import *
from .forms import CreateUserForm, OrderForm, CustomerForm


from .filters import OrderFilter
from accounts import forms
from .decorators import allowed_users, unauthenticated_user, admin_only

# login, register
# # authentication models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # for restricting page

# # using flash messages to pass messages
from django.contrib import messages

# if user is authenticated redirecting them to login otherwise register page
@unauthenticated_user
def registerUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # adding customer to group
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # # c
            # Customer.objects.create(user = user, name = user.username)
            

             # or
             # can be done using signal i.e. signals.py
             
            messages.success(request, 'Account was created for ' + username)

            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user # -> using decorators
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def accountSettings(request):
	# customer = request.user.customer
	# form = CustomerForm(instance=customer)

	# if request.method == 'POST':
	# 	form = CustomerForm(request.POST, request.FILES,instance=customer)
	# 	if form.is_valid():
	# 		form.save()


	# context = {'form':form}

    customer = request.user.customer
    # Create a form instance with customer data.
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()
    

    context = {'orders':orders, 'customers':customers,
    'total_customers':total_customers, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending, 'out_for_delivery':out_for_delivery}
    return render(request,'accounts/dashboard.html', context)


# product page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html', {'products':products})

    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProduct(request):
    products = Product.objects.all()
    tags = Tag.objects.all()
    categories = Category.objects.all()
    # print('Category -> ', category)
    

    if request.method == 'POST':
        product = request.POST
        print('Product ->', product)
        category = Category.objects.get(id=product['category'])
        print('CAtegory -> ', category)

        
        if product['tags'] != 'none':
            tagObj = Tag.objects.get(id=product['tags'])

        elif product['new_tag'] != '':
            tagObj, created = Tag.objects.get_or_create(name = product['new_tag'])
        else:
            tagObj = None

            

        new_product = Product.objects.create(
            name = product['name'],
            price = product['price'],
            category = category,
            description = product['description'],
        )
        new_product.tags.add(tagObj)
        new_product.save()
        return redirect('products')

    context = {'products':products, 'tags' : tags, 'categories':categories}
 
    return render(request,'accounts/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)

    print("{} image {}".format(customer, customer.profile_pic))
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {'customer':customer, 'orders':orders, 'orders_count':orders_count, 'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addCustomer(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('profile_pic')

        print('data : ', data)
        print('image' , image)

        new_customer = Customer.objects.create(
            name = data['name'],
            phone = data['phone'],
            email = data['email'],
            profile_pic = image,
        )
        return redirect('home')


    context = {}
    return render(request, 'accounts/add_customer.html', context)

# place order
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    # inlineformset_factory args must be parent model and then child model and which fields
    # you want to allow for the child objects
    # extra adds more field
    # can_delete -> gives delete checkbox
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=5, can_delete=False)
    customer = Customer.objects.get(id=pk)

    # form = OrderForm(initial={'customer':customer})
    # if request.method == 'POST':
        # form = OrderForm(request.POST)
        # if form.is_valid():
        #     form.save()
        # return redirect ('/')
    # context = {'form':form}

    # queryset = Order.objects.none() -> hiding the displayed filled fields or removing instances
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect ('/')
    context = {'formset':formset}
    return render(request, 'accounts/multiorder_form.html', context)


# update
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    # Creating a form to change an existing room.
    order = Order.objects.get(id=pk)
    # for pre-filled form
    form = OrderForm(instance=order)

    # restricing pages
    # if request.user != room.host:
    #     return HttpResponse('You are not allowed here')


    if request.method == 'POST':
    # print(request.POST)
    # Create a form to edit an existing Roomform, but use
    # POST data to populate the form.
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


# delete
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    # restricing user
    # if request.user != order.name:
    #     return HttpResponse('You are not allowed here')

    if request.method == "POST":
        order.delete()
        return redirect('/')

    return render(request, 'accounts/delete.html', {'order':order})


@login_required(login_url='login') 
@allowed_users(allowed_roles=['customer'])
def userPage(request):

    # following relationships "backwards". For that _set is used.
    # The _set is a reverse lookup class variable django puts in for you.
    orders = request.user.customer.order_set.all()
    print('Orders ->', orders)

    # or
    # request.user refers to the actual user model instance.
    # here, related_name = "entries" passed as args in orders. So, we don't have to use 'order_set'.
    # orders = request.user.customer.order.all()


    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()


    context = {'orders':orders, 'total_orders':total_orders,
    'delivered':delivered, 'pending':pending, 'out_for_delivery':out_for_delivery}

    return render(request, 'accounts/user.html', context)