from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request, 'anemoneApp/home.html')

def index(request):
    return render(request, 'anemoneApp/index.html')

def about(request):
    return render(request, 'anemoneApp/Pages/about.html')

def dashboard(request):
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
    return render(request, 'anemoneApp/Pages/product.html', {'arts': arts, 'garments': garments})

def profile(request):
    return render(request, 'anemoneApp/Pages/profile.html')

def settings(request):
    return render(request, 'anemoneApp/Pages/settings.html')

def signup(request):
    return render(request, 'anemoneApp/Pages/signup.html')

def terms(request):
    return render(request, 'anemoneApp/Pages/terms.html')

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
    return render(request, 'anemoneApp/Pages/custom.html', {
        'products': products,
        'selected_garment': selected_garment,
        'selected_art': selected_art, 
    })

def product_detail(request, product_id):
    # Placeholder: You would fetch product details from DB in a real app
    return render(request, 'anemoneApp/Pages/product_detail.html', {'product_id': product_id})

def add_to_cart(request, product_id):
    # Placeholder: Implement cart logic here
    if request.method == 'POST':
        # Add product to cart logic goes here
        return HttpResponseRedirect(reverse('custom'))
    return HttpResponseRedirect(reverse('custom'))
