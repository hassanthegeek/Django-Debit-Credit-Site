from accounts.models import AccountDetail
from django.urls import path
from .views import CreateAccountDetail, ShopAccounts, UpdateAccountDetail, home, ShopListView, ShopCreateView, ShopUpdateView, delete_accoun_detail, UpdateAccountDetail

app_name = 'account'
urlpatterns = [
    path('', ShopListView.as_view(), name='home'),
    path('shops/', ShopListView.as_view(), name='shops'),
    path('shops/create/', ShopCreateView.as_view(), name='create-shop'),
    path('shops/<int:pk>/update/', ShopUpdateView.as_view(), name='update-shop'),
    path('shops/<int:pk>/details/', ShopAccounts.as_view(),
         name='shop-account-details'),
    path('shops/details/delete/<int:pk>',
         delete_accoun_detail, name='delete-ad'),
    path('shops/<int:pk>/details/add',
         CreateAccountDetail.as_view(), name='add-entry'),
    path('shops/details/update/<int:pk>',
         UpdateAccountDetail.as_view(), name='update-ad')
]
