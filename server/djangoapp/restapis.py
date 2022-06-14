import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

"""# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_review(url, json_payload, **kwargs):
    results = []
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, dealerId=-1):
    results = []
    if dealerId >= 0:
        json_result = get_request(url,  dealerId=dealerId)
    else:
        json_result = get_request(url)
    if json_result:
        if "rows" in json_result["body"] and len(json_result["body"]["rows"]) > 0:
            dealers = json_result["body"]["rows"]
            for dealer in dealers:
                dealer_doc = dealer["doc"]
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
                results.append(dealer_obj)
        elif "docs" in json_result["body"] and len(json_result["body"]["docs"]) > 0:
            dealer_doc = json_result["body"]["docs"][0]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"],
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results
  
  
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for review in reviews:
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"], sentiment="positive", id=review["id"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    # Note: I'm going to follow IBM NLU API instead because Course Lab example doesn't work.
    NLU_API_KEY = 'HWREf8jdoh868vaURWTDaEoY_N0pti6BH_rv6kbtuVBj' 
    NLU_API_URL = 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/21494ebd-affd-4dcb-8282-b543ddf213b5'
    sentiment = "neutral"

    authenticator = IAMAuthenticator(NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
        )

    natural_language_understanding.set_service_url(NLU_API_URL)

    print(f"Analyzing sentiment for: {text}")
    try:
        word_count = math.ceil(len(text.split()) / 2)
        if word_count <= 0:
            word_count = 1
        response = natural_language_understanding.analyze(
            text=text,
            features=Features(
                keywords=KeywordsOptions(emotion=False, sentiment=True, limit=word_count)
                )
            ).get_result()
        if "keywords" in response:
            keywords = response['keywords']
            sentiment_tally = {
                "positive" : 0,
                "negative" : 0,
                "neutral" : 0
                }
            highest = "neutral"
            for keyword in keywords:
                key = keyword['sentiment']['label']
                sentiment_tally[key] += 1
                if sentiment_tally[key] > sentiment_tally[highest]:
                    highest = key
            sentiment = highest
        print(json.dumps(response, indent=2))
    except ApiException as ae:
        print("NLU ApiException: {}".format(ae))
    print(f"Final sentiment: {sentiment}")
    return sentiment


def add_review_to_cf(json_payload):
    results = []
    url = "https://5dbcd2a2.us-south.apigw.appdomain.cloud/dealership/post_review"
    json_result = post_request(url, json_payload=json_payload)
    print(f"json_result={json_result}")
    if json_result and "body" in json_result:
        reviewId = json_result["body"]
        print(f"reviewId={reviewId}")
        results.append({
            "reviewId" : reviewId
            })
    return results """
