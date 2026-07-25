from rest_framework import serializers
from ..validators.url_validator import is_valid_url

class AnalyzeRequestSerializer(serializers.Serializer):
    url = serializers.CharField(required=True, allow_blank=False)
    
    def validate_url(self, value):
        if not is_valid_url(value):
            raise serializers.ValidationError("Please provide a valid HTTP or HTTPS URL.")
        return value
