from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from . models import *
from . form import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
#from django.views.generic import TemplateView

# class HomePageView(TemplateView):
#     template_name='shop/index.html'
#     def get(self, request, *args, **kwargs):
#         return self.get(request, *args, **kwargs)
def home(request):
    product=Product.objects.filter(trending=1)
    return render(request, 'shop/index.html', {"product":product})


def login_page(request):
   if request.user.is_authendicate:
      return redirect('/')
   else:
      if request.method=='POST':
         name=request.POST.get('username')
         pwd=request.POST.get('password')
         user=authenticate(request,username=name, password=pwd)
         if user is not None:
            login(request,user)
            messages.success(request, "Logged in successfully")
         else:
            messages.error(request, "Invalid User Name or Password")
      return render(request,"shop/login.html")
   

def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
    
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")
   

def cart_page(request):
   if request.user.is_authendicate:
      cart=Cart.objects.filter(user=request.user)
      return render(request, "shop/cart.html", {"cart":cart})
      pass
   else:
      return redirect("/")
   

def remove_cart(request, cid):
   cartitem = Cart.objects.get(id=cid)
   cartitem.delete()
   return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


def logout_page(request):
   if request.user.is_authendicate:
      logout(request)
      messages.success(request, 'Logout successfully')
   return redirect('/')

def register(request):
    form=CustomUserForm
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration success you can login nom")
          return redirect('/login')
    return render(request, 'shop/register.html', {'form':form})

def collections(request):
  catagory=Catagory.objects.filter(status=0)
  return render(request,"shop/collections.html",{"catagory":Catagory})

def collectionsview(request, name):
   if(Catagory.objects.filter(name=name, status=0)):
      prodect=Product.objects.filter(catagory__name=name)
      return render(request,"shop/prodect/index.html",{"product":Product, "catagory":name})
   else:
      messages.warning(request, "No collection is found")
      return redirect('collections')
   

def product_details(request, cname, pname):
   if(Catagory.objects.filter(name=cname, status=0)):
      if(Product.objects.filter(name=pname, status=0)):
         product=Product.objects.filter(name=pname, status=0,).filter()
      else:
         messages.error(request, "No such product found")
         return redirect('collections')
   else:
      messages.error(request, "No such catagory found")
      return redirect('collections')

def add_to_cart(request):
   if request.header.get('x-request-with')=='XMLHttpResquest':
      if request.user.is_authendicated:
         data=json.load(request)
         product_qty=data['product_qty']
         product_id=data=['pid']
         product_status=Product.objects.get(id=product_id)
         if product_status:
            if Cart.objects.filter(user=request.user.id,product_id=product_id):
                return JsonResponse({'status':'product already in cart'}, status=200)
            else:
               if product_status.quantity>=product_qty:
                  Cart.objects.create(user=request.user,product_id=product_id, product_qty=product_qty)
                  return JsonResponse({'status':'product added to cart'}, status=200)
               else:
                  return JsonResponse({'status':'product stock no available'}, status=200)
      else:
        return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
      return JsonResponse({'status':'Inavlid Access'}, status=200)