from django.shortcuts import render
from django.views.generic.base import (View,)


class IndexView(View):
    def get(self, request, *args, **kwags):
        return render(request, 'index.html')
