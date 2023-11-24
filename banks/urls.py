from django.urls import path
from . import views

app_name = "banks"
urlpatterns = [
    path("add/", views.BankCreateView.as_view(), name="add"),
    path(
        "<int:bank_id>/details/", views.BankDetailsView.as_view(), name="bank-details"
    ),
    path(
        "<int:bank_id>/branches/add/",
        views.BranchCreateView.as_view(),
        name="branch-add",
    ),
    path(
        "branch/<int:branch_id>/details/",
        views.BranchDetailsView.as_view(),
        name="branch-details",
    ),
    path(
        "<int:bank_id>/branches/all/",
        views.BranchListView.as_view(),
        name="branch-list",
    ),
    path("all/", views.BankListView.as_view(), name="banks-all"),
    path(
        "branch/<branch_id>/edit/",
        views.BranchUpdateView.as_view(),
        name="branch-update",
    ),
]
