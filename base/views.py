from base.views.dashboard_view import Dashboard
from base.views.auth_view import UserLoginView, LogoutView
from base.views.category_view import CategoryCreateView, CategoryListView, CategoryUpdateView, CategoryDeleteView
from base.views.inventory_view import CreateInventoryView, InventoryListView, InventoryDetailView, \
    InventoryUpdateView, InventoryDeleteView
from base.views.tag_view import CreateListTagView, TagDeleteView
from base.views.product_view import CreateProductView, ProductListView

from base.views.pos_view import POSView, cart_add, cart_updated, cart_remove
from base.views.order_views import bulling_information_view, OrderItemView