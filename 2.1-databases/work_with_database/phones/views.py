from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_by = request.GET.get('sort')
    if sort_by == 'name':
        phones_obj = Phone.objects.order_by('name').all()
    elif sort_by == 'min_price':
        phones_obj = Phone.objects.order_by('price').all()
    elif sort_by == 'max_price':
        phones_obj = Phone.objects.order_by('-price').all()
    else: phones_obj = Phone.objects.all()
    context = {'phones' : phones_obj, 'par': request.GET.get('sort')}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_obj = Phone.objects.filter(slug=slug).first()
    print(request.GET.get('sort'))
    context = {'phone' : phone_obj}
    return render(request, template, context)
