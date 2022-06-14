from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake
from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, add_review_to_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

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
    context = {}
    if request.method == "GET":
        dealerships = get_dealers_from_cf()
        context["dealers"] = dealerships
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealers = get_dealer_by_id_from_cf(dealer_id)
        context["dealer"] = None
        if len(dealers) > 0:
            context["dealer"] = dealers[0]
        context["reviews"] = get_dealer_reviews_from_cf(dealer_id)
    return render(request, "djangoapp/dealer_details.html", context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "POST":
        if request.user is not None and request.user.is_authenticated:
            print("POST something.")
            POST = request.POST
            review = {
                "dealership" : dealer_id,
                "name" : f"{request.user.first_name} {request.user.last_name}",
                "purchase" : ("purchase" in POST and POST["purchase"] == "on"),
                "purchase_date" : POST["purchase_date"],
                "review" : POST["review"],
                }

            review["car_make"] = "undefined"
            review["car_model"] = "undefined"
            review["car_year"] = 1800
            post_carId = POST["car"]
            car_models = get_all_cars_by_dealer(dealer_id)
            if car_models and post_carId in car_models:
                car = car_models[post_carId]
                review["car_make"] = car.makeId.name
                review["car_model"] = car.name
                review["car_year"] = car.year.year
                
            json_payload = { "review" : review }
            print(f"json_payload={json_payload}")
            result = add_review_to_cf(json_payload)
            if result and len(result) > 0:
                print(f"POST add_review_to_cf SUCCESS! reviewId={result[0]['reviewId']}")
                return redirect('djangoapp:dealer', dealer_id=dealer_id)
    # GET part
    context = {}
    dealers = get_dealer_by_id_from_cf(dealer_id)
    context["dealer"] = None
    context["cars"] = get_all_cars_options_by_dealer(dealer_id)
    if len(dealers) > 0:
        context["dealer"] = dealers[0]
    return render(request, "djangoapp/add_review.html", context)
