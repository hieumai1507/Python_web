from django.shortcuts import render
from django.views import View
from . models import Product
from django.db.models import Count
# Create your views here.
def home(request):
  return render(request, "app/home.html");


class CategoryView(View):
  def get(self,request,val):
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request, "app/category.html",locals())