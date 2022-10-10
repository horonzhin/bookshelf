import datetime


class LoggerMiddleware:
    """Логирование информации о посетителе"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        method = request.method
        time = datetime.datetime.now()
        url = request.path

        with open('log.txt', 'a') as file:
            file.write(f'{time} | {ip} | {method} | {url}\n')

        return self.get_response(request)

