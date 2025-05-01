from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAuthenticatedOrReadOnly
from rest_framework.throttling import UserRateThrottle , AnonRateThrottle , ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly

from watchlist_app.models import WatchList , StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializers ,StreamPlatformSerializers ,ReviewSerializers
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPagination



"""
class based view
for use need to import 
from rest_framework.views import APIView
"""


# class ReviewDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     """
#         GenericAPIView along with mixins
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     """
#     GenericAPIView along with mixins
#     """
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)

    # def get_queryset(self):
    #     username = self.request.query_params.get('username', None)
    #     # Here usename is foriegn key thats why we need to pass __username
    #     return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist,review_user=review_user)



class ReviewList(generics.ListAPIView):
    """
            GenericAPIView concreet view
    """
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    #permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewListThrottle ,AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']




    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        GenericAPIView concreet view
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle, AnonRateThrottle]
    throttle_scope = 'review-detail'




class StreamPlatformVS(viewsets.ModelViewSet):
    """
    ModelViewSet
    """
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializers
    permission_classes = [IsAdminOrReadOnly]

# class StreamPlatformVS(viewsets.ViewSet):
#     """
#     By this we dont need to create separate class for accessing list and detail
#     """
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializers(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializers(watchlist)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self ,request):
        platform = StreamPlatform.objects.all()
        serializer_data = StreamPlatformSerializers(platform, many=True)
        return Response(serializer_data.data)

    def post(self, request):
        serializer_data = StreamPlatformSerializers(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except:
            return Response({"Error : Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer_data = StreamPlatformSerializers(platform)
        return Response(serializer_data.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer_data = StreamPlatformSerializers(platform, data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self ,request):
        movies = WatchList.objects.all()
        serializer_data = WatchListSerializers(movies, many=True)
        return Response(serializer_data.data)

    def post(self, request):
        serializer_data = WatchListSerializers(data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self,request,pk):
        try:
            movies = WatchList.objects.get(pk=pk)
        except:
            return Response({"Error : Movie not found"} , status=status.HTTP_404_NOT_FOUND)
        serializer_data = WatchListSerializers(movies)
        return Response(serializer_data.data)

    def put(self,request,pk):
        movies = WatchList.objects.get(pk=pk)
        serializer_data = WatchListSerializers(movies,data=request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response(serializer_data.data)
        else:
            return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movies = WatchList.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    """
    Create this generic view to test filter_backends
    """
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializers
    pagination_class = WatchListCPagination

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'platform__name']

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__name']
    #
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields  = ['avg_rating']





"""
Function based view
"""
# @api_view(["GET","POST"])
# def movie_list(request):
#     if request.method == "GET":
#         movies = Movie.objects.all()
#         # when we have multiple object we need to set many = True
#         serializer_data = MovieSerializers(movies,many=True)
#         return Response(serializer_data.data)
#     elif request.method == "POST":
#         serializer_data = MovieSerializers(data=request.data)
#         if serializer_data.is_valid():
#             serializer_data.save()
#             return Response(serializer_data.data)
#         else:
#             return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(["GET","PUT","DELETE"])
# def movie_detail(request,pk):
#     if request.method == "GET":
#         try:
#             movies = Movie.objects.get(pk=pk)
#         except:
#             return Response({"Error : Movie not found"} , status=status.HTTP_404_NOT_FOUND)
#         serializer_data = MovieSerializers(movies)
#         return Response(serializer_data.data)
#     elif request.method == "PUT":
#         movies = Movie.objects.get(pk=pk)
#         serializer_data = MovieSerializers(movies,data=request.data)
#         if serializer_data.is_valid():
#             serializer_data.save()
#             return Response(serializer_data.data)
#         else:
#             return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         movies = Movie.objects.get(pk=pk)
#         movies.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


