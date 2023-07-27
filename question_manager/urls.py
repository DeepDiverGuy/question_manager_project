from django.urls import path
from .views import (
    add_favorite_question,
    add_read_question,
    count_favorite_questions_per_user,
    count_read_questions_per_user,
    filter_questions,
    get_favorite_questions,
    get_read_questions,
)

urlpatterns = [
    # URL patterns for inserting data for FavoriteQuestion and ReadQuestion
    path('add_favorite_question/', add_favorite_question, name='add_favorite_question'),
    path('add_read_question/', add_read_question, name='add_read_question'),

    # URL patterns for retrieving data for FavoriteQuestion and ReadQuestion
    path('get_favorite_questions/', get_favorite_questions, name='get_favorite_questions'),
    path('get_read_questions/', get_read_questions, name='get_read_questions'),

    # URL patterns for counting favorite and read questions per user
    path('count_favorite_questions_per_user/', count_favorite_questions_per_user, name='count_favorite_questions_per_user'),
    path('count_read_questions_per_user/', count_read_questions_per_user, name='count_read_questions_per_user'),

    # URL pattern for filtering questions by status (read, unread, favorite, unfavorite)
    path('filter_questions/', filter_questions, name='filter_questions'),
]
