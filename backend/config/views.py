from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def frontend(request):
    """
    Renvoie la page d'accueil de l'application Vue.js.

    Pose aussi le cookie CSRF, que le frontend renvoie dans l'en-tête
    X-CSRFToken de chaque requête qui modifie des données.
    """
    index = settings.FRONTEND_DIST / "index.html"
    if not index.exists():
        raise Http404("Build Vue.js introuvable : lancez `npm run build` dans frontend/")
    return FileResponse(open(index, "rb"), content_type="text/html")
