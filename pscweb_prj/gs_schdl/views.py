from django.shortcuts import render
from django.views import generic
from .models import Production

class ProductionIndexView(generic.ListView):
    model = Production
    paginate_by = 10
