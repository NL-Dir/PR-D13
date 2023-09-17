from django_filters import FilterSet
from .models import Comment


class CommentsFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {'commentPost': ['exact'],
                  'dateCreation': ['gt'],
                  'commentUser': ['exact'],
                  }
