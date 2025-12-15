from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomSignupForm # 🌟 Import your custom form

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # 1. Create the user object from the form data
            user = form.save()
            user.set_password(form.cleaned_data['password']) # 🔑 IMPORTANT: Hash the password
            user.save()
            print("User created!")

            # 2. Log the user in
            login(request, user)
            return redirect('dashboard')  # Redirect to a success page.
        else:
            # Pass the form back to the template to show errors
            pass 
            
    else:
        form = CustomSignupForm() # A blank form for GET request

    # For a custom HTML form, we only need to pass the form errors back, not the form object itself
    context = {
        # Pass the form object to access errors in the template
        'form': form, 
    }
    return render(request, 'registration/signup.html', context)

# Create your views here.

def index(request):
    return render(request, 'anemoneApp/index.html')

def about(request):
    return render(request, 'anemoneApp/Pages/about.html')

from django.contrib.auth.decorators import login_required

@login_required 
def dashboard(request):
    # This view will only run if the user is logged in.
    return render(request, 'anemoneApp/Pages/dashboard.html')

def login_view(request):
    return render(request, 'anemoneApp/Pages/login.html')

def product(request):
    # Example arts and garments data
    arts = [
        {'name': 'Eagle Painting', 'image': 'Images/Eagle.jpg'},
        {'name': 'Sun Art', 'image': 'Images/Sun_P.jpg'},
        {'name': 'Butterfly', 'image': 'Images/Butterfly_P.jpg'},
    ]
    garments = [
        {'name': "Men's Jeans", 'image': 'Images/Topjean.jpg'},
        {'name': 'Hoodie', 'image': 'Images/Sun_P.jpg'},
        {'name': 'Cap', 'image': 'Images/Sun_P_cap.jpg'},
        {'name': 'Bag', 'image': 'Images/Cat_P.jpg'},
        {'name': 'T-Shirt', 'image': 'Images/Apple_P.jpg'},
        {'name': 'Short Jeans', 'image': 'Images/Butterfly_P.jpg'},
    ]
    return render(request, 'product/product.html', {'arts': arts, 'garments': garments})

@login_required
def profile(request):
    return render(request, 'anemoneApp/Pages/profile.html')

@login_required
def settings(request):
    return render(request, 'anemoneApp/Pages/settings.html')

def terms(request):
    return render(request, 'anemoneApp/Pages/terms.html')

def cart(request):
    products_db = {
        1: {'name': "Skull Face Denim Men's Jeans", 'price': 499.99, 'image': 'Images/skull_P.jpg'},
        2: {'name': "Sun Hoodie", 'price': 359.99, 'image': 'Images/Sun_P.jpg'},
        3: {'name': "Sun Jeans Cap", 'price': 120.00, 'image': 'Images/Sun_P_cap.jpg'},
        4: {'name': "Cat Bag", 'price': 100.00, 'image': 'Images/Cat_P.jpg'},
        5: {'name': "Jelly Fish Hoodie", 'price': 359.99, 'image': 'Images/Fish_P.jpg'},
        6: {'name': "Red Apple T-Shirt", 'price': 150.00, 'image': 'Images/Apple_P.jpg'},
        7: {'name': "Butter Fly Short Jeans", 'price': 250.00, 'image': 'Images/Butterfly_P.jpg'},
        # Add any other products you want to support here
    }
    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    for pid, qty in cart.items():
        pid_int = int(pid)
        product = products_db.get(pid_int)
        if product:
            total_price = product['price'] * qty
            cart_items.append({
                'id': pid_int,
                'product': {
                    'name': product['name'],
                    'price': product['price'],
                    'image': product['image'],
                    'total_price': total_price,
                },
                'quantity': qty,
            })
            cart_total += total_price
    tax = cart_total * 0.1
    grand_total = cart_total + tax
    return render(request, 'product/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'tax': tax,
        'grand_total': grand_total,
    })
    
from django.shortcuts import redirect

def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
    return redirect('cart')
    
from django.views.decorators.http import require_POST

@require_POST
def update_cart(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    # Update the cart item with item_id to the new quantity
    # (session, database, etc.)
    return redirect('cart')

def custom(request):
    products = [
        {
            'id': 1,
            'name': "Skull Face Denim Men's Jeans",
            'price': 499.99,
            'image': 'Images/skull_P.jpg'
        },
        {
            'id': 2,
            'name': "Sun Hoodie",
            'price': 359.99,
            'image': 'Images/Sun_P.jpg'
        },
        {
            'id': 3,
            'name': "Sun Jeans Cap",
            'price': 120.00,
            'image': 'Images/Sun_P_cap.jpg'
        },
        {
            'id': 4,
            'name': "Cat Bag",
            'price': 100.00,
            'image': 'Images/Cat_P.jpg'
        },
        {
            'id': 5,
            'name': "Jelly Fish Hoodie",
            'price': 359.99,
            'image': 'Images/Fish_P.jpg'
        },
        {
            'id': 6,
            'name': "Red Apple T-Shirt",
            'price': 150.00,
            'image': 'Images/Apple_P.jpg'
        },
        {
            'id': 7,
            'name': "Butter Fly Short Jeans",
            'price': 250.00,
            'image': 'Images/Butterfly_P.jpg'
        },
    ]
    
    selected_garment = {'name': "Men's Jeans", 'image': 'Images/Topjean.jpg'}
    selected_art = {'name': "Eagle Painting", 'image': 'Images/Eagle.jpg'}
    return render(request, 'product/custom.html', {
        'products': products,
        'selected_garment': selected_garment,
        'selected_art': selected_art, 
    })

def product_detail(request, product_id):
    # Placeholder: You would fetch product details from DB in a real app
    return render(request, 'anemoneApp/Pages/product_detail.html', {'product_id': product_id})

from django.db.models import Q
from .models import Product
from decimal import Decimal

def search(request):
    """
    Handles the search for products, querying the database across 
    product name, description, and SKU.
    """
    query = request.GET.get('q')
    results = Product.objects.all() # Default empty queryset

    if query:
        # Check if the query is a valid number for price filtering (optional enhancement)
        is_price_query = False
        try:
            Decimal(query.replace('M', '').strip())
            is_price_query = True
        except:
            pass
            
        # Construct the complex lookup using Q objects (OR logic)
        search_criteria = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) 
        )
        
        # If the query looks like a price, you could optionally add price filtering
        # if is_price_query:
        #     search_criteria |= Q(price=Decimal(query.replace('M', '').strip()))
            
        # Filter the Products and order by name
        results = Product.objects.filter(search_criteria).order_by('name')

    # Render the results template
    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'product/search.html', context)
