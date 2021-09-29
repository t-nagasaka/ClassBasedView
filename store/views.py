from django.shortcuts import render
from django.views.generic.base import (View, TemplateView)
from django.views.generic.detail import DetailView
from . import forms
from datetime import datetime
from .models import Books
import pprint


class IndexView(View):
    def get(self, request, *args, **kwags):
        book_form = forms.BookForm()
        return render(request, 'index.html', context={
            'book_form': book_form
        })

    def post(self, request, *args, **kwargs):
        book_form = forms.BookForm(request.POST or None)
        if book_form.is_valid():
            book_form.save()
        return render(request, 'index.html', context={
            'book_form': book_form
        })


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(kwargs)
        context["name"] = kwargs.get('name')
        context["time"] = datetime.now()
        return context


class BookDetailView(DetailView):
    model = Books
    template_name = 'book.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint.pprint(vars(context['books']))
        return context
    
