from django.urls import path
from . import views

app_name = 'performance_management' 

urlpatterns = [
    path('add_review/', views.add_review, name='add_review'),
    path('review_list/', views.review_list, name='review_list'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
