from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/Edit/', views.profile_edit, name='profileedit'),
    path('Movie/add/', views.add_movie, name='addmovie'),
    path('mymovies/', views.my_movies, name='mymovies'),
    path('mymovies/<slug:slug>/edit/', views.edit_my_movie, name='edit_my_movie'),
    path('mymovies/<slug:slug>/delete', views.delete_my_movie, name='delete_my_movie'),
    path('movie/<slug:slug>/', views.movie_detail, name='movie_detail'),
    path('movie/<slug:slug>/add_review/', views.add_review, name='add_review'),
    path('movie/<slug:slug>/edit_review/', views.edit_review, name='edit_review'),
    path('movie/<slug:slug>/reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('search/', views.search_movies, name='search_movies'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    
    # path('movie/<int:movie_id>',views.details,name='details'),
    # path('add/',views.add_movie,name='add_movie'),
    # path('update/<int:id>',views.update,name='update'),
    # path('delete/<int:id>',views.delete,name='delete'),
]
