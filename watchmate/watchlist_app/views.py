# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse
#
# def movie_list(request):
#     movies = Movie.objects.all()
#     #print(movies) # It provide complex queryset as output
#     #print(movies.values()) #  It provide dictionary as output
#     data = {
#             "movies" : list(movies.values())
#         }
#     return JsonResponse(data) # to send a json response we need data in dictionary format only
#
#
# def movie_detail(request ,pk):
#     movies = Movie.objects.get(pk=pk)
#     data = {
#         "name": movies.name,
#         "description" : movies.description,
#         "active" : movies.active
#     }
#     #print(movies.name ,movies.description ,movies.active )
#     return JsonResponse(data)
