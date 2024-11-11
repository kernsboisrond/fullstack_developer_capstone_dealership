# Uncomment the required imports before adding the code

from .restapis import get_request, analyze_review_sentiments, post_review
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'username': user.username})
        else:
            return JsonResponse({'status': 'failed', 'message': 'Invalid credentials'})
    
    return JsonResponse({'status': 'failed', 'message': 'Only POST requests are allowed'})

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)  # Logs out the user
            return JsonResponse({"status": "success", "message": "User logged out", "username": ""})
        else:
            return JsonResponse({"status": "failed", "message": "No user is logged in"})
    else:
        return JsonResponse({"error": "Only GET method is allowed"}, status=400)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"email": email, "error": "Email already in use"}, status=409)

        # Create new user
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)

        # Log in the user after registration
        login(request, user)

        # Return success response
        return JsonResponse({"userName": username, "status": "Authenticated"}, status=201)
    
    return JsonResponse({"error": "Invalid request method"}, status=400)
    
def get_cars(request):
    # Check if there are any CarMake records in the database
    count = CarMake.objects.count()
    print(count)
    
    # If no car makes exist, populate the database
    if count == 0:
        initiate()

    # Fetch all CarModel records, including related CarMake data
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    
    # Build a list of cars with their make and model information
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
        
    # Return the list of cars as a JSON response
    return JsonResponse({"CarModels": cars})




# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                if response and isinstance(response, dict) and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = "unknown"
            return JsonResponse({"status": 200, "reviews": reviews})
        else:
            return JsonResponse({"status": 500, "message": "Failed to fetch reviews"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
def add_review(request):
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

