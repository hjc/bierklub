from django.shortcuts import render


def standard_404(request):
    """Return a standard Page Not Found."""
    resp = render(request, "error_handlers/404.html", {'title': 'Page Not Found'})
    resp.status_code = 404
    return resp


def standard_500(request):
    """Return a standard 500 page."""
    resp = render(
        request,
        'error_handlers/500.html',
        {'title': 'Uh Oh!'}
    )
    resp.status_code = 500
    return resp
