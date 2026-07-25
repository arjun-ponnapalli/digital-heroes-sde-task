from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .serializers import AnalyzeRequestSerializer
from ..services.analyzer import analyze_webpage

class AnalyzeWebpageAPIView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = []
    """
    API endpoint that accepts a URL, validates it, and returns a detailed SEO/performance report.
    """
    def post(self, request, *args, **kwargs):
        # 1. Validate incoming data
        serializer = AnalyzeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Invalid URL provided.",
                "error_code": "VALIDATION_ERROR",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        url = serializer.validated_data['url']
        
        # 2. Process URL
        try:
            report_data = analyze_webpage(url)
            return Response({
                "success": True,
                "data": report_data
            }, status=status.HTTP_200_OK)
            
        except ValueError as ve:
            # Handles non-HTML responses
            return Response({
                "success": False,
                "message": str(ve),
                "error_code": "NON_HTML_CONTENT"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Handles connection errors, timeouts, SSL, etc.
            # In a production app, we would log the exact exception stack trace here.
            return Response({
                "success": False,
                "message": str(e),
                "error_code": "FETCH_ERROR"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
