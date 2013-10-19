from django.core.urlresolvers import resolve, Resolver404


def navigation(request):
    try:
        match = resolve(request.path)
        return {
            'url_name': match.url_name
        }
    except Resolver404 as e:
        return {
            'url_name' : ''
        }