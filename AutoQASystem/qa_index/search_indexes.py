from .models import *
from haystack import indexes


class QAItemIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return QAItem

    def index_queryset(self, using=None):
        return self.get_model().objects.all()