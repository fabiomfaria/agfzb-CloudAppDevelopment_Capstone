from django.db import models
from django.utils.timezone import now


# Create your models here.
SEDAN = "SEDAN"
SUV = "SUV"
WAGON = "WAGON"

CAR_MODELS_CHOICES = (
    (SEDAN, "Sedan"),
    (SUV, "SUV"),
    (WAGON, "WAGON"),
)

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    def __str__(self):
        return ("Car name: {0}, description: {1}".format(self.name, self.description))

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_makes = models.ManyToManyField(CarMake, related_name='carModels')
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=30)
    car_type = models.CharField(max_length=30, choices=CAR_MODELS_CHOICES)
    year = models.DateField()

    def __str__(self):
        return ("Car name: {0}, type: {1}".format(self.name, self.car_type))

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name + " " + str(self.id)

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview :
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Dealer review: " + self.review
    