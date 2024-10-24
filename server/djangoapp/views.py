# Uncomment the required imports before adding the code

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
    
# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
