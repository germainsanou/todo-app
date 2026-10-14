from django.conf import settings
from django.http import FileResponse, Http404


def frontend(request):
    """Renvoie la page d'accueil de l'application React."""
    index = settings.FRONTEND_DIST / "index.html"
    if not index.exists():
        raise Http404("Build React introuvable : lancez `npm run build` dans frontend/")
    return FileResponse(open(index, "rb"), content_type="text/html")