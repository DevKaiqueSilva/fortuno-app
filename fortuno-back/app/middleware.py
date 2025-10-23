class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Override Railway's CORS headers
        response['Access-Control-Allow-Origin'] = 'https://fortuno-app.vercel.app'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Origin, Content-Type, Accept, Authorization, X-Requested-With'
        response['Access-Control-Allow-Credentials'] = 'true'
        
        return response