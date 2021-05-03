from rest_framework.pagination import PageNumberPagination


class CustomPaginationUser(PageNumberPagination):
    page_size_ = 50
    page_size_query_param = 'page_Size'
    max_page_size = 100


class CustomPaginationInvestment(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
