"""
Views for the receipt_api app.
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .scraper import scrape_receipt_data
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def scrape_receipt(request):
    """
    API endpoint for scraping receipt data.
    
    Accepts both GET and POST requests:
    - GET: URL provided as a query parameter 'url'
    - POST: URL provided in the request body as JSON {'url': 'receipt_url'}
    
    Returns:
        JsonResponse: The structured receipt data
    """
    try:
        if request.method == 'GET':
            url = request.GET.get('url')
            if not url:
                return JsonResponse(
                    {'error': 'URL parameter is required'}, 
                    status=400
                )
        else:  # POST
            try:
                data = json.loads(request.body)
                url = data.get('url')
                if not url:
                    return JsonResponse(
                        {'error': 'URL field is required in request body'}, 
                        status=400
                    )
            except json.JSONDecodeError:
                return JsonResponse(
                    {'error': 'Invalid JSON in request body'}, 
                    status=400
                )
        
        # Check if it's a valid TRA receipt URL
        if 'verify.tra.go.tz' not in url:
            return JsonResponse(
                {'error': 'Only TRA receipt URLs are supported'}, 
                status=400
            )
            
        # Scrape the receipt data
        receipt_data = scrape_receipt_data(url)
        
        # Return the data as JSON
        return JsonResponse(receipt_data, safe=False)
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return JsonResponse(
            {'error': str(e)}, 
            status=500
        )