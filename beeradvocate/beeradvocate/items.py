# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib_exp.djangoitem import DjangoItem
from beers.models import Beer

class BeerAdvocateItem(DjangoItem):
    django_model = Beer

#class BeerAdvocateItem(Item):
#    url = Field()
#    name = Field()
#    brewery = Field()
#    brewery_number = Field()
#    beer_number = Field()
#    BA_score = Field()
#    #brew_location = Field()            Not implemented
#    style = Field()              
#    ABV = Field()
#    reviews = Field()
#    
