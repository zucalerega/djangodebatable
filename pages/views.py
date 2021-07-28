from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Resource
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

class ResourceListView(ListView):
    model=Resource
    template_name='resources/resources.html'
    context_object_name='resources'
    ordering=['-published']
    #posts per page
    paginate_by=4
