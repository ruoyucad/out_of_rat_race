
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product
# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'products/list.html', context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context


def product_detail_view(request, pk=None, *args, **kwargs):
    # instance = Product.objects.get(pk=pk)  # id
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:

    #     raise Http404("product does not exit")
    # except:
    #     print("huh ?")

    qs = Product.objects.filter(id=pk)
    if qs.exist() and qs.count() == 1:
        instance = qs.fisrt()
    else:
        raise Http404('product does not exit')

    context = {
        'object': instance
    }
    return render(request, 'products/detail.html', context)
