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
            
            paginator = Paginator(last, 8) 
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
                    paginator = Paginator(product, 8) 
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

class Items:
    def __init__(self,request,id):
        self.cart = Cart(request)
        self.product = get_object_or_404(Inventory, id=id)
        self.request = request

    def act(self):
        raise NotImplementedError("There is no act for this !!!")

class CartAdd(Items):
    def act(self):
        self.cart.add(product=self.product, quantity=1, update_quantity=1)

class CartRemove(Items):
    def act(self):
        self.cart.remove(self.product)

class CartUpdate(Items):
    def act(self):
        number = int(self.request.POST['number'])
        price = self.request.POST['price']
        method = self.request.POST['method']
        self.cart.add(product=self.product, quantity=number,price=price,method=method, update_quantity=True)

class CartDiscount(Items):
    def act(self):
        discount = self.request.POST['discount']
        self.cart.set_final_price(discount)

def cart_actions(action):
    action.act()
    
# Add to cart views
class Cart_add(View):
    def get(self,request, id):
        action = CartAdd(request, id)
        cart_actions(action)
        return redirect('pos_view')

# Remove Shopping Cart views
class Cart_remove(View):
    def get(self,request, id):
        action = CartRemove(request,id)
        cart_actions(action)
        return redirect('pos_view')


# update Shopping Cart views
class Cart_update(View):
    def post(self,request, id):
        action = CartUpdate(request,id)
        cart_actions(action)
        return redirect('pos_view')

# Set discount to cart views
class Cart_discount(View):
    def get(self,request, id):
        action = CartDiscount(request, id)
        cart_actions(action)
        return redirect('pos_view')