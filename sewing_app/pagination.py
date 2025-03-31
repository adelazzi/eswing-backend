from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = "page_size"  # Allow client to specify page size
    max_page_size = 200  # Limit max page size
