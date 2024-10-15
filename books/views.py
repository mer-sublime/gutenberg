# Create your views here.

from django.db.models import Sum, Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person
from .serializers import AuthorSerializer


class AuthorsView(APIView):
    """Retrieve authors ranked by total download count of their books."""

    def get(self, request):
        authors = (
            Person.objects
            .annotate(
                total_download_count=Sum('book__download_count', distinct=True),
                number_of_books=Count('book', distinct=True),
                number_of_bookshelves=Count('book__bookshelves', distinct=True)
            )
            .filter(total_download_count__gt=0)  # Only include authors with books
            .order_by('-total_download_count')
        )

        serializer = AuthorSerializer(authors, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
