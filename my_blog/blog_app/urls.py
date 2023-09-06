from django.urls import path
from . import views
app_name = 'blog_app'# allows me to organize URLs by app and use the name when referring to them 
urlpatterns = [
    # posting my views 
    #path('',views.post_list, name='post_list'),
    path("",views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),# angle brackets are used to capture values from the URL
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
