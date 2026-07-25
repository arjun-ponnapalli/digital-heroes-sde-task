import unittest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import requests

class PagePulseAPITests(APITestCase):
    
    def setUp(self):
        self.url = reverse('api-analyze')
        self.valid_payload = {'url': 'https://example.com'}
        self.invalid_payload = {'url': 'not_a_valid_url'}

    @patch('pagepulse.services.analyzer.requests.get')
    def test_happy_path(self, mock_get):
        """Test a successful URL analysis."""
        # Mock a successful HTML response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'Content-Type': 'text/html; charset=utf-8'}
        mock_response.text = '''
            <html>
                <head>
                    <title>Test Page</title>
                    <meta name="description" content="This is a test description.">
                </head>
                <body>
                    <h1>Main Heading</h1>
                    <img src="test.jpg" alt="An image">
                    <img src="missing_alt.jpg">
                    <p>Some word count text here.</p>
                </body>
            </html>
        '''
        mock_get.return_value = mock_response
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        data = response.data['data']
        self.assertEqual(data['http_status_code'], 200)
        self.assertEqual(data['page_title'], 'Test Page')
        self.assertEqual(data['meta_description'], 'This is a test description.')
        self.assertEqual(data['h1_count'], 1)
        self.assertEqual(data['missing_alt_count'], 1)
        self.assertGreater(data['word_count'], 0)

    def test_invalid_url(self):
        """Test API behavior when an invalid URL is provided."""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error_code'], 'VALIDATION_ERROR')

    @patch('pagepulse.services.analyzer.requests.get')
    def test_timeout_handling(self, mock_get):
        """Test handling of request timeouts."""
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response.data['success'])
        self.assertIn("timed out", response.data['message'].lower())

    @patch('pagepulse.services.analyzer.requests.get')
    def test_non_html_response(self, mock_get):
        """Test when the target URL returns a non-HTML content type (e.g., PDF or Image)."""
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'application/pdf'}
        mock_get.return_value = mock_response
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error_code'], 'NON_HTML_CONTENT')

    @patch('pagepulse.services.analyzer.requests.get')
    def test_connection_error(self, mock_get):
        """Test handling of DNS failures or connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to resolve")
        
        response = self.client.post(self.url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertFalse(response.data['success'])
        self.assertIn("failed to connect", response.data['message'].lower())
