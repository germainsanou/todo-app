from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Pagination par défaut de l'API : ?page=2 et, au besoin, ?page_size=50.

    Réponse : {"count": 42, "next": "<url>", "previous": "<url>", "results": [...]}
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
