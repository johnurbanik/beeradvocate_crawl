from haystack import indexes
from beers.models import Beer

class BeerIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    brewery = indexes.CharField(model_attr='brewery')
    style = indexes.CharField(model_attr='style')
    ABV = indexes.DecimalField(model_attr='ABV')
    BA_score = indexes.CharField(model_attr='BA_score')
    
    def get_model(self):
        return Beer
    
    def prepare(self, obj):
        data = super(BeerIndex, self).prepare(obj)
        base_boost = 1
        try:
            base_boost = max(1,float(int(obj.BA_score) - 50)*1.2)
        except ValueError:
            base_boost = 1
        data['boost'] = base_boost
        return data
    