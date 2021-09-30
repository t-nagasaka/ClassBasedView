from django.shortcuts import render
from django.views.generic.base import (View, TemplateView, RedirectView)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from . import forms
from datetime import datetime
from .models import Books
from django.contrib.messages.views import SuccessMessageMixin
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


class BookListView(ListView):
    model = Books
    template_name = 'book_list.html'

    def get_queryset(self):
        qs = super(BookListView, self).get_queryset()
        if 'name' in self.kwargs:
            qs = qs.filter(name__startswith=self.kwargs['name'])
        qs = qs.order_by('description')
        return qs


class BookCreateView(CreateView):
    model = Books
    fields = ['name', 'description', 'price']
    template_name = 'add_book.html'
    # success_url = reverse_lazy('store:list_books')

    def form_valid(self, form):
        form.instance.create_at = datetime.now()
        form.instance.update_at = datetime.now()
        return super(BookCreateView, self).form_valid(form)

    def get_initial(self, **kwargs):
        initial = super(BookCreateView, self).get_initial(**kwargs)
        initial['name'] = 'sample'
        return initial


class BookUpdateView(SuccessMessageMixin, UpdateView):

    template_name = 'update_book.html'
    model = Books
    form_class = forms.BookUpdateForm
    success_message = '更新に成功しました'

    def get_success_url(self):
        print(self.object)
        return reverse_lazy('store:detail_book', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        picture_form = forms.PictureUploadForm()
        context['picture_form'] = picture_form
        return context

    def post(self, request, *args, **kwargs):
        picture_form = forms.PictureUploadForm()
        if picture_form.is_valid() and request.FILES:
            book = self.get_object()
            picture_form.save(book=book)
        return super(BookUpdateView, self).post(request, *args, **kwargs)


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'delete_book.html'
    success_url = reverse_lazy('store:list_books')


class BookFormView(FormView):

    template_name = 'form_book.html'
    form_class = forms.BookForm
    success_url = reverse_lazy('store:list_books')

    def get_initial(self):
        initial = super(BookFormView, self).get_initial()
        initial['name'] = 'form sample'
        return initial

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(BookFormView, self).form_valid(form)


class BookRedirectView(RedirectView):
    url = 'https://google.com'

    def get_redirect_url(self, *args, **kwargs):
        book = Books.objects.first()
        print(book)
        if 'pk' in kwargs:
            return reverse_lazy('store:detail_book', kwargs={'pk': kwargs['pk']})
        return reverse_lazy('store:edit_book', kwargs={'pk': book.pk})
