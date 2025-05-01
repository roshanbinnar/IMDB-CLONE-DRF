from django.urls import path , include
from watchlist_app.api.views import WatchListGV, UserReview,StreamPlatformVS,ReviewCreate,ReviewDetail,WatchListAV , WatchDetailAV ,StreamPlatformAV , StreamPlatformDetailAV ,ReviewList
from rest_framework.routers import DefaultRouter

"""
Url depends on function based view
"""
#from watchlist_app.api.views import movie_list , movie_detail
# urlpatterns = [
#     path('list/', movie_list ,name="movie-list"),
#     path('<int:pk>/', movie_detail ,name="movie-detail")
# ]


"""
Url depends on class based view
"""

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view() ,name="movie-list"),
    path('<int:pk>/', WatchDetailAV.as_view() ,name="movie-detail"),
    # For filtering test purpose
    path('list2/', WatchListGV.as_view(), name='watch-list'),

    # For stream with viewset
    path('', include(router.urls)),

    # For stream without viewset
    # path('stream/', StreamPlatformAV.as_view(), name="stream"),
    # path('stream/<int:pk>', StreamPlatformDetailAV.as_view(), name="stream-details"),

    # path('review/', ReviewList.as_view(), name="review-list"),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name="review-create"),
    path('<int:pk>/reviews/', ReviewList.as_view(), name="review-list"),
    path('review/<int:pk>/', ReviewDetail.as_view(), name="review-detail"),
    path('reviews/<str:username>/', UserReview.as_view(), name='user-review-detail')


]