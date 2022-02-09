# Rest framework imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ItemIndexPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        # Setting page_size. Without this code, page_size in the response will
        # remain 10 even if it is present in the url
        if self.page_size_query_param in self.request.query_params:
            self.page_size = self.request.query_params.get(
                self.page_size_query_param
            )
        
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page_size,
            'results': data
        })
