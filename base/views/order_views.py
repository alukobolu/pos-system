from base.models import OrderItem,Inventory
from base.models import Cart as ModelCart
from django.shortcuts import render, redirect
from base.forms.order_form import OrderForm
from base.addcart import Cart
from django.views.generic import ListView


def bulling_information_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            instance =  ModelCart()
            instance.total = cart.get_total_price
            instance.save()

            for item in cart:
                
                instance.products.add(item['product'])
                instance.save()
                
                OrderItem.objects.create(
                    orderItem=order,
                    products=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    method=item['method']
                )
                inv =Inventory.objects.get(id=item['product'].id)
                inv.current_stock = inv.current_stock - int(item['quantity'])
                inv.save()
                
            cart.clear()
        return redirect('pos_view')
    else:
        form = OrderForm()
    return render(request, 'pos/bulling_information.html', {'form': form, 'cart': cart})


class OrderItemView(ListView):
    template_name = 'pos/order_list.html'
    model = OrderItem
    context_object_name = 'order'
    paginate_by = 10
