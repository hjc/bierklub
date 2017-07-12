from django.shortcuts import render


def standard_404(request):
    """Return a standard Page Not Found."""
    return render(request, "error_handlers/404.html", {'title': 'Page Not Found'})


def standard_500(request):
    """Return a standard 500 page."""
    return render(
        request,
        'error_handlers/500.html',
        {'title': 'Uh Oh!'}
    )
