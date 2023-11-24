from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/view/", views.profile_view, name="profile-view"),
    path("profile/edit/", views.profile_edit, name="profile-edit")
    # path('<int:pk>/', views.StoresDetail.as_view(), name='detail'),
    # path('create/', views.StoresCreate.as_view(), name='create'),
    # path('<int:pk>/update/', views.StoresUpdate.as_view(), name='update'),
    # path('<int:pk>/delete/', views.StoresDelete.as_view(), name='delete'),
    # path('<int:store_id>/add/', views.products_add, name='add-product'),
]
