from django.urls import path
from . import views

urlpatterns = [
    path('', views.BaseView.as_view(), name='index'),
    path('<str:ct_model>/<slug:slug>', views.ProductDetailView.as_view(),name='product_detail'),
    path('cart/', views.CartView.as_view(),name='cart'),
    path('add-to-cart/<str:ct_model>/<str:product_slug>', views.AddToCart.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:ct_model>/<str:product_slug>', views.DeleteFromCart.as_view(), name='delete_from_cart'),
    path('change-qty/<str:ct_model>/<str:product_slug>', views.ChangeQTY.as_view(), name='change_qty'),
    path('cart/order/',views.OrderView.as_view(), name='order'),
    path('search/', views.Search.as_view(), name='search'),



]