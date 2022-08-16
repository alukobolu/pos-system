from django.urls import path
from base.views.dashboard_view import Dashboard
from base.views.auth_view import UserLoginView, LogoutView
from base.views.category_view import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView
from base.views.inventory_view import CreateInventoryView, InventoryListView, InventoryDetailView, \
    InventoryUpdateView, InventoryDeleteView
from base.views.tag_view import CreateListTagView, TagDeleteView
from base.views.product_view import CreateProductView, ProductListView

from base.views.pos_view import POSView, Cart_add, Cart_discount ,  Cart_update, Cart_remove
from base.views.order_views import bulling_information_view, OrderItemView, CartView

urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('create-category/', CategoryCreateView.as_view(), name='create_category'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category-delete/<pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    path('create-inventory/', CreateInventoryView.as_view(), name='inventory_create'),
    path('inventory/', InventoryListView.as_view(), name='inventory_list'),
    path('inventory/<pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory-update/<pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory-delete/<pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('tag/', CreateListTagView.as_view(), name='create_list_tag'),
    path('tag/<pk>/', TagDeleteView.as_view(), name='tag_delete'),
    path('create-product/', CreateProductView.as_view(), name='product_create'),
    path('product-list/', ProductListView.as_view(), name='product_list'),
    path('cart/<int:id>/', Cart_add.as_view(), name='cart_add'),
    path('cart-update/<int:id>/', Cart_update.as_view(), name='cart_update'),
    path('cart-discount/<int:id>/', Cart_discount.as_view(), name='cart_discount'),
    path('cart-remove/<int:id>/', Cart_remove.as_view(), name='cart_remove'),
    path('pos/', POSView.as_view(), name='pos_view'),
    path('bulling-infromation/', bulling_information_view, name='bulling_information'),
    path('order-infromation/', OrderItemView.as_view(), name='order_information'),
    path('cart-infromation/', CartView.as_view(), name='cart_information'),
]
