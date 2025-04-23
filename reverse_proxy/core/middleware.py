# core/middleware.py

class ProxyLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(f"[Proxy] {request.method} {request.path} => {response.status_code}")
        return response