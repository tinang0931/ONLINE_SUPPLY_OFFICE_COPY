from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db.models import F

class SearchItemIndex(models.Model):
    search_item = models.OneToOneField('search.SearchItem', on_delete=models.CASCADE)
    search_vector = SearchVectorField(null=True)

    def save(self, *args, **kwargs):
        self.search_vector = SearchVector('search_item__title', 'search_item__description', weight='A') + \
                              SearchVector(F('search_item__title'), F('search_item__description'), weight='B')
        super().save(*args, **kwargs)