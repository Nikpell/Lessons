class HandlerGET:
    def __init__(self, func):
        self.__fn = func

    def __call__(self, request, *args, **kwargs):
        res = self.get(self.__fn, request)
        return res

    def get(self, func, request, *args, **kwargs):
        if request.get('method') in ["GET", None]:
            return f'GET: {func(request)}'

@HandlerGET
def contact(request):
    return "Сергей Балакирев"

res = contact({"method": "POST", "url": "contact.html"})
print(res)