import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

""" from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key = None, **kwargs):
    print(kwargs)
    try:
        if api_key is not None and len(api_key) > 0:
            print("GET from {} with AUTH".format(url))
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('api_key', api_key))
        else:
            print("GET from {} ".format(url))    
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs 
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    try:
        print("POST from {} ".format(url))    
        response = requests.post(url, headers={'Content-Type': 'application/json'}, params=kwargs, json=json_payload)
    except:
        # If any error occurs 
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def _get_dealers_from_cf_by_url(url):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            # print(f"dealer={dealer}")
            results.append(CarDealer.create(dealer))
    return results


def get_dealers_from_cf():
    return _get_dealers_from_cf_by_url("https://fffinal.us-south.apigw.appdomain.cloud/api/dealership")

def get_dealer_by_id_from_cf(dealer_id):
    return _get_dealers_from_cf_by_url(f"https://fffinal.us-south.apigw.appdomain.cloud/api/dealership?dealer_id={dealer_id}")

def get_dealers_by_state_from_cf(state):
    return _get_dealers_from_cf_by_url(f"https://fffinal.us-south.apigw.appdomain.cloud/api/dealership?state={state}")
  
  
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(dealerId):
    results = []
    json_result = get_request(f"https://fffinal.us-south.apigw.appdomain.cloud/api/review/?dealerId={dealerId}")
    if json_result and "body" in json_result:
        reviews = json_result["body"]
        # print(reviews)
        for review in reviews:
            review['sentiment'] = analyze_review_sentiments(review['review'])
            # print(f"review={review}")
            results.append(DealerReview.create(review))
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative """



