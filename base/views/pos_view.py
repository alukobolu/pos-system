from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from base.models import Category, Inventory
from base.addcart import Cart


class POSView(View):

    def get(self, request):
        if request.GET.get('q') ==None or request.GET.get('q') =='':
            last = Inventory.objects.all().order_by('-id')
            cart = Cart(request)
            
            for item in cart:
                item['update_quantity_form'] = {'quantity': item['quantity'],'price': item['price'] ,'method': item['method'] ,'update': True}
            
            paginator = Paginator(last, 1) 
            page_number = request.GET.get('main_page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'cosmetic': page_obj,
                'cart': cart,
            }
            cate = Category.objects.all()
            lists=[]
            for i,cat in enumerate(cate):
                if Inventory.objects.filter(category_name=cat).exists() == True:
                    product = Inventory.objects.filter(category_name=cat)
                    paginator = Paginator(product, 1) 
                    li = 'page'+str(i)
                    page_number = request.GET.get(li)
                    page_obj = paginator.get_page(page_number)
                    product = page_obj
                else:
                    product = None
                lists.append(product)
            context['group'] = lists
            context['categories'] = cate
            template_name = 'pos/pos.html'
            return render(request, template_name, context)
        else:
            query = request.GET['q']
            print(query)
            last = Inventory.objects.filter(name__icontains=query).order_by('-id')
            cart = Cart(request)
            for item in cart:
                item['update_quantity_form'] = {'quantity': item['quantity'],'price': item['price'] ,'method': item['method'] ,'update': True}

            context = {
                'cosmetic': last,
                'cart': cart,
            }
            template_name = 'pos/pos.html'
            return render(request, template_name, context)


# Add to cart views
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Inventory, id=id)
    cart.add(product=product, quantity=1, update_quantity=1)
    return redirect('pos_view')


# Remove Shopping Cart views
def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Inventory, id=id)
    cart.remove(product)
    return redirect('pos_view')


# update Shopping Cart views
@require_POST
def cart_updated(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST['number'])
        price = request.POST['price']
        method = request.POST['method']
    product = get_object_or_404(Inventory, id=id)
    cart.add(product=product, quantity=number,price=price,method=method, update_quantity=True)
    return redirect('pos_view')
