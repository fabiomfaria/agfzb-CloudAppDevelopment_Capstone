from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, add_review_to_cf, post_review
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# var
urldealerships = "https://5dbcd2a2.us-south.apigw.appdomain.cloud/dealership/get_dealerships/"
urlreviews = "https://5dbcd2a2.us-south.apigw.appdomain.cloud/dealership/get_reviews/"
urlreview = "https://5dbcd2a2.us-south.apigw.appdomain.cloud/dealership/post_review/"

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_dealers_from_cf(urldealerships)
        context = {}
        context["dealerships"] = dealerships

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(urlreviews, dealer_id)
        dealership = get_dealers_from_cf(urldealerships, dealerId=dealer_id)
        if len(dealership) == 0:
            return redirect('djangoapp:index')
        context = {}
        context["reviews"] = reviews
        context["dealership"] = dealership[0]
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'GET':
            dealership = get_dealers_from_cf(urldealerships, dealerId=dealer_id)
            if len(dealership) == 0:
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            carModel = CarModel.objects.all().filter(dealer_id=int(dealer_id))
            context["dealership"] = dealership[0]
            context["cars"] = carModel
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == 'POST':
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = True if "purchasecheck" in request.POST and request.POST["purchasecheck"] == 'on' else False
            review["purchase_date"] = request.POST["purchasedate"]
            cars = request.POST["car"].split("#")
            try:
                review["car_model"] = CarModel.objects.get(id=int(cars[0])).name
                review["car_year"] = CarModel.objects.get(id=int(cars[0])).year.year
                review["car_make"] = CarMake.objects.get(id=int(cars[0])).name
            except:
                review["car_model"] = ""
                review["car_make"] = ""
                review["car_year"] = ""
            
            json_payload = {}
            json_payload["review"] = review
            result = post_review(urlreview, json_payload)
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
