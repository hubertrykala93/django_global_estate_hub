from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomLimitOffsetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            data={
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "data": data,
            }
        )
