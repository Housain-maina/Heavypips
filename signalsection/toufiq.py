def add_variable_to_context(request):
    isAjax=False
    if request.is_ajax():
        isAjax=True

    return {'isAjax': isAjax}

class MyMiddleware:
    def process_response(self, request, response):
        if request.is_ajax():
            response['Location'] = request.get_full_path()
            response['Cache-Control'] = 'no-cache'

        return response;