from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="index"),
    path("fresh", views.fresh, name="fresh"),
    path('paper/<int:paper_id>/', views.paper_detail, name='paper_detail'),  # Paper detail page
    path("subject", views.subject, name="subject"),
    path("search", views.search, name="search"),
    path('increase_score/<int:paper_id>/', views.increase_score, name='increase_score'),
    path('fetch_papers/', views.fetch_papers, name='fetch_papers'),
    path('fetch_categories/', views.fetch_categories, name='fetch_categories'),
    path('search_papers/', views.search_papers, name='search_papers'),
]