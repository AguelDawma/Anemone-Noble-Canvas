from django.shortcuts import render, redirect
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

from .models import Product, Garment, ArtPiece

def product(request):
    
    if request.method == 'POST':
        selected_garment_id = request.POST.get('selected_garment')
        selected_art_id = request.POST.get('selected_art')
        
        request.session['selected_garment'] = selected_garment_id
        request.session['selected_art'] = selected_art_id
        
        return redirect('custom')
    
    else:
        garments = Garment.objects.all()
        arts = ArtPiece.objects.all()
        
        context = {
            'garments': garments,
            'arts': arts,
        }
        
        return render(request, 'product/product.html', context)
    
@login_required
def profile(request):
    return render(request, 'anemoneApp/Pages/profile.html')

@login_required
def settings(request):
    return render(request, 'anemoneApp/Pages/settings.html')

def terms(request):
    return render(request, 'anemoneApp/Pages/terms.html')

from .models import Product, Garment, ArtPiece

def cart(request):

    cart = request.session.get('cart', {})
    cart_items = []
    cart_total = 0
    for pid, qty in cart.items():
        pid_int = int(pid)
        product = Product.objects.filter(id=pid_int).first()
        if product:
            total_price = product.price * qty
            cart_items.append({
                'id': pid_int,
                'product': {
                    'name': product.name,
                    'price': product.price,
                    'image': product.image,
                    'total_price': total_price,
                },
                'quantity': qty,
            })
            cart_total += total_price
            
    tax = cart_total * Decimal('0.10')
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
        pid = str(product_id)
        
        if pid in cart:
            cart[pid] += 1
        else:
            cart[pid] = 1

        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')
    
from django.views.decorators.http import require_POST

@require_POST
def update_cart(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    # Update the cart item with item_id to the new quantity
    # (session, database, etc.)
    return redirect('cart')

def custom(request):
    products = Product.objects.all()
    
    garment_id = request.session.get('selected_garment')
    art_id = request.session.get('selected_art')
    
    garment = Garment.objects.filter(id = garment_id).first()
    art = ArtPiece.objects.filter(id = art_id).first()
    
    return render(request, 'product/custom.html', {
        'products': products,
        'selected_garment': garment,
        'selected_art': art, 
    })

def product_detail(request, product_id):
    # Placeholder: You would fetch product details from DB in a real app
    return render(request, 'anemoneApp/Pages/product_detail.html', {'product_id': product_id})

from django.db.models import Q
from .models import Product, Garment, ArtPiece
from decimal import Decimal
from itertools import chain

def search(request):
    """
    Handles the search for products, querying the database across 
    product name, description, and SKU.
    """
    query = request.GET.get('q')
    product_results = Product.objects.all() # Default empty queryset
    garment_results = Garment.objects.all()
    art_results = ArtPiece.objects.all()
    
    results = list(chain(product_results, garment_results, art_results))

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

def select_items(request):
    if request.method == 'POST':
        selected_garment_id = request.POST.get('selected_garment')
        selected_art_id = request.POST.get('selected_art')
        
        request.session['selected_garment'] = selected_garment_id
        request.session['selected_art'] = selected_art_id
        
        return redirect('custom')
    
    else:
        garments = Garment.objects.all()
        arts = ArtPiece.objects.all()
        
        context = {
            'garments': garments,
            'arts': arts,
        }
        
        return render(request, 'product/product.html', context)
