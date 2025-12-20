from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import CustomSignupForm # 🌟 Import your custom form
from django.db.utils import OperationalError
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__) 

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

        # Save as integers in session when possible, otherwise remove keys
        try:
            if selected_garment_id and str(selected_garment_id).strip() != '':
                request.session['selected_garment'] = int(selected_garment_id)
            else:
                request.session.pop('selected_garment', None)
        except (ValueError, TypeError):
            request.session.pop('selected_garment', None)

        try:
            if selected_art_id and str(selected_art_id).strip() != '':
                request.session['selected_art'] = int(selected_art_id)
            else:
                request.session.pop('selected_art', None)
        except (ValueError, TypeError):
            request.session.pop('selected_art', None)

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

from django.contrib import messages

def product_detail(request, product_id):
    
    product = Product.objects.filter(id=product_id).first()
    back_url = request.META.get('HTTP_REFERER', '/')
    
    if not product:
        messages.error(request, "Oops! This item is not available right now.")
        return redirect('store')
    
    return render(request, 'product/product_detail.html', {'product': product,
                                                           'back_url': back_url,
                                                           })

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

        # Save as integers in session when possible, otherwise remove keys
        try:
            if selected_garment_id and str(selected_garment_id).strip() != '':
                request.session['selected_garment'] = int(selected_garment_id)
            else:
                request.session.pop('selected_garment', None)
        except (ValueError, TypeError):
            request.session.pop('selected_garment', None)

        try:
            if selected_art_id and str(selected_art_id).strip() != '':
                request.session['selected_art'] = int(selected_art_id)
            else:
                request.session.pop('selected_art', None)
        except (ValueError, TypeError):
            request.session.pop('selected_art', None)

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
from .models import Garment, ArtPiece, customItem

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
        pos = request.POST.get('position')
        size = request.POST.get('size')

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

        # Helper: compress to webp
        def compress_to_webp(image_field, max_size=1024, quality=80):
            try:
                image_field.open('rb')
                img = Image.open(image_field)
                # normalize mode
                if img.mode not in ('RGB', 'RGBA'):
                    img = img.convert('RGB')
                img.thumbnail((max_size, max_size), Image.LANCZOS)
                buf = BytesIO()
                img.save(buf, format='WEBP', quality=quality)
                buf.seek(0)
                return buf
            except Exception as e:
                logger.exception('Image compression failed')
                return None

        # Try a few sizes progressively smaller to avoid 413 Payload Too Large
        sizes = [1024, 800, 600, 400]
        response = None
        last_err = ''
        for s in sizes:
            g_buf = compress_to_webp(garment.image, max_size=s, quality=80)
            a_buf = compress_to_webp(art.image, max_size=s, quality=80)
            if not g_buf or not a_buf:
                last_err = 'Failed to process images for preview.'
                continue

            files = {
                'gament_image': ('garment.webp', g_buf, 'image/webp'),
                'art_image': ('art.webp', a_buf, 'image/webp'),
            }

            try:
                response = requests.post(
                    "https://api.stability.ai/v2beta/stable-image/generate/core",
                    headers={
                        "authorization": f"Bearer {API_KEY}",
                        "accept": "image/*"
                    },
                    files=files,
                    data={"prompt": f"using image-to-image, inpaint a {size} given art on the given outfit at the {pos}.", "output_format": "webp"},
                    timeout=60,
                )
                response.raise_for_status()
                # success
                break
            except requests.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                logger.exception('Image generation HTTP error')
                if status == 413:
                    # Payload too large — try next smaller size
                    logger.warning(f'Payload too large at size {s}; trying smaller size')
                    last_err = f'Payload too large at size {s}.'
                    continue
                last_err = str(e)
                break
            except requests.RequestException as e:
                logger.exception('Image generation request failed')
                last_err = str(e)
                break

        # If we never got a successful response, report the last error
        if response is None:
            return render(request, 'product/custom.html', {
                'error': f'Image generation failed: {last_err}',
                'products': products,
                'selected_garment': garment,
                'selected_art': art,
            })

        # Successful response; save preview
        file_name = f"preview_{garment.id}_{art.id}.webp"
        item_name = f"preview_{garment.id}_{art.id}"
        item_price = garment.price + art.price
        new_custom = customItem(name = item_name, size = garment.size , price = item_price, category = garment.category)

        try:
            new_custom.image.save(file_name, ContentFile(response.content), save=True)
        except OperationalError:
            return render(request, 'product/custom.html', {
                'error': 'Unable to save preview to the database: migrations may be pending.',
                'products': products,
                'selected_garment': garment,
                'selected_art': art,
            })

        return render(request, 'product/custom.html', {
            'preview': new_custom,
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
    
def store(request):
    
    products = Product.objects.all()
    
    return render(request, 'product/store.html', {
        'products': products,
    })
