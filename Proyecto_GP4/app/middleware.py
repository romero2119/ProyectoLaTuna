class HistorialNavegacionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.method == 'GET':

            url_actual = request.path

            # Evitar guardar estáticos o admin
            if not url_actual.startswith('/static') and not url_actual.startswith('/admin'):

                ultima = request.session.get('ultima_url')

                if ultima and ultima != url_actual:
                    request.session['penultima_url'] = ultima

                request.session['ultima_url'] = url_actual

        return self.get_response(request)