from survey.models import Survey
from .serializers import SurveySerializer
from rest_framework.generics import ListAPIView

class SurveyList(ListAPIView):
    serializer_class = SurveySerializer

    def get_queryset(self):
        """
        Filter by url query params.
        """
        queryset = Survey.objects.live()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset