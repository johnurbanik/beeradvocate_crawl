from django.db import models

# Create your models here.

class Beer(models.Model):
    url = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    brewery = models.CharField(max_length = 255)
    brewery_number = models.IntegerField()
    beer_number = models.IntegerField()
    BA_score = models.CharField(max_length = 255, blank = True)
    #brew_location = Field()            Not implemented
    style = models.CharField(max_length = 255, blank = True)              
    ABV = models.DecimalField(decimal_places = 2, max_digits= 5, blank = True)
    reviews = models.TextField(blank = True)
    
    def __unicode__(self):
        return self.name + '-' + self.brewery