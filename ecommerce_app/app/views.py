from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
def home(req):
  return render(req, "app/home.html");
