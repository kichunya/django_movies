from django.urls import path

from . import views

urlpatterns = [
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMovieView.as_view(), name="filter"),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name="json_filter"),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name='movie_detail'),
    path("comment/<int:pk>/", views.AddComment.as_view(), name="add_comment"),
    path("person/<str:slug>/", views.PersonView.as_view(), name="person_detail"),

]
