from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomSignupForm # 🌟 Import your custom form
from django.db.utils import OperationalError

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # 1. Create the user object from the form data but don't commit yet
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)  # 🔑 IMPORTANT: Hash the password
            user.save()
            print("User created!")

            # 2. Authenticate the user so Django sets the correct backend when logging in
            from django.contrib.auth import authenticate
            from django.conf import settings

            # Try authenticating by email first, then by username
            auth_user = authenticate(request, username=user.email, password=password)
            if auth_user is None:
                auth_user = authenticate(request, username=user.username, password=password)

            if auth_user is None:
                # Fallback: set backend explicitly from settings (last resort)
                backend = settings.AUTHENTICATION_BACKENDS[0] if settings.AUTHENTICATION_BACKENDS else 'django.contrib.auth.backends.ModelBackend'
                user.backend = backend
                login(request, user)
            else:
                login(request, auth_user)

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
                    'description': product.description,
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
    cart = request.session.get('cart', {})
    pid = str(item_id)
    if quantity > 0:
        cart[pid] = quantity
    else:
        cart.pop(pid, None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart
    request.session.modified = True
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
    
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import Garment, ArtPiece, CustomizedPreview

def generate_preview(request):
    """Handle POST from custom preview form, validate inputs and render custom page
    with the same context (`products`, `selected_garment`, `selected_art`)."""
    products = Product.objects.all()

    # Read selections from session to preserve what user previously chose
    session_garment_id = request.session.get('selected_garment')
    session_art_id = request.session.get('selected_art')

    selected_garment = None
    selected_art = None
    try:
        if session_garment_id is not None and str(session_garment_id).strip() != '':
            selected_garment = Garment.objects.filter(id=int(session_garment_id)).first()
    except (ValueError, TypeError):
        selected_garment = None

    try:
        if session_art_id is not None and str(session_art_id).strip() != '':
            selected_art = ArtPiece.objects.filter(id=int(session_art_id)).first()
    except (ValueError, TypeError):
        selected_art = None

    if request.method == "POST":
        garment_id = request.POST.get('garment_id')
        art_id = request.POST.get('art_id')
        desc = request.POST.get('description')

        # Validate and convert IDs
        try:
            garment_id = int(garment_id)
            art_id = int(art_id)
        except (ValueError, TypeError):
            return render(request, 'product/custom.html', {
                'error': 'Invalid garment or art selection.',
                'products': products,
                'selected_garment': selected_garment,
                'selected_art': selected_art,
            })

        garment = Garment.objects.filter(id=garment_id).first()
        art = ArtPiece.objects.filter(id=art_id).first()

        if not garment or not art:
            return render(request, 'product/custom.html', {
                'error': 'Selected garment or art not found.',
                'products': products,
                'selected_garment': selected_garment,
                'selected_art': selected_art,
            })

        # persist selection to session so the custom page reflects them
        request.session['selected_garment'] = garment.id
        request.session['selected_art'] = art.id

        # Look up API key from settings or env; provide useful error if missing
        from django.conf import settings
        API_KEY = getattr(settings, 'STABILITY_API_KEY', None)
        if not API_KEY:
            import os
            API_KEY = os.environ.get('STABILITY_API_KEY')

        if not API_KEY:
            return render(request, 'product/custom.html', {
                'error': 'Image generation API key is not configured. Set STABILITY_API_KEY in settings or environment.',
                'products': products,
                'selected_garment': garment,
                'selected_art': art,
            })

        try:
            response = requests.post(
                "https://api.stability.ai/v2beta/stable-image/generate/core",
                headers={
                    "authorization": f"Bearer {API_KEY}",
                    "accept": "image/*"
                },
                files={"image": garment.image.open("rb")},
                data={"prompt": f"Style of {art.title}: {desc}", "output_format": "webp"},
                timeout=60,
            )
        except requests.RequestException:
            return render(request, 'product/custom.html', {
                'error': 'Failed to reach image generation API.',
                'products': products,
                'selected_garment': garment,
                'selected_art': art,
            })

        if response.status_code == 200:
            new_preview = CustomizedPreview(user_description=desc)
            file_name = f"preview_{garment.id}_{art.id}.webp"

            try:
                # Attempt to save the image; if the DB table doesn't exist this will raise
                # OperationalError (e.g. before migrations have been applied).
                new_preview.result_image.save(file_name, ContentFile(response.content), save=True)
            except OperationalError:
                # Friendly error message for missing migration / table
                return render(request, 'product/custom.html', {
                    'error': 'Unable to save preview to the database: migrations may be pending. Run `python manage.py makemigrations` and `python manage.py migrate`.',
                    'products': products,
                    'selected_garment': garment,
                    'selected_art': art,
                })

            return render(request, 'product/custom.html', {
                'preview': new_preview,
                'products': products,
                'selected_garment': garment,
                'selected_art': art,
            })

        # Non-200 response: include status for debugging
        return render(request, 'product/custom.html', {
            'error': f'Image generation failed (status {response.status_code}).',
            'products': products,
            'selected_garment': garment,
            'selected_art': art,
        })

    # GET: render the page with products and any existing selected values
    return render(request, 'product/custom.html', {
        'products': products,
        'selected_garment': selected_garment,
        'selected_art': selected_art,
    })
