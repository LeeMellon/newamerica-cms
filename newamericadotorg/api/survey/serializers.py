from rest_framework import serializers
from survey.models import Survey

# Serializers define the API representation.
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'