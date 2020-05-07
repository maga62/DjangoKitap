
from unicodedata import category


from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage
from kitap.models import Kitap, Category, Images, Comment


def index(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    sliderdata = Kitap.objects.all()[:4]
    dayproduct = Kitap.objects.all()[:3]
    lastproduct = Kitap.objects.all().order_by('-id')[:4]
    randomproduct = Kitap.objects.all().order_by('?')[:4]
    context={'setting':setting,
             'page':'home',
             'sliderdata':sliderdata,
             'category': category,
             'dayproduct':dayproduct,
             'lastproduct': lastproduct,
             'randomproduct': randomproduct,
             }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,
             'page':'hakkimizda',
             'category': category,}
    return render(request, 'hakkimizda.html', context)
def referanslar(request):
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    context={'setting':setting,
             'page':'referanslar',
             'category':category}
    return render(request, 'referanslar.html', context)
def iletisim(request):
    if request.method=='POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=form.cleaned_data['name']
            data.email=form.cleaned_data['email']
            data.subject=form.cleaned_data['subject']
            data.message=form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajiniz gonderildi: succes")
            return  HttpResponseRedirect('/iletisim')
    setting=Setting.objects.get(pk=1)
    category = Category.objects.all()
    form=ContactFormu()
    context={'setting':setting,'form':form,
             'category':category}
    return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products=Kitap.objects.filter(category_id=id)

    context={'products':products,
             'category':category,
             'categorydata': categorydata


             }
    return render(request, 'products.html', context)

def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    product = Kitap.objects.get(pk=id)
    category = Category.objects.all()
    images = Images.objects.filter(kitap_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context={'product':product,
             'category':category,
             'setting': setting,
             'images': images,
             'comments': comments


             }

    return render(request, 'product_detail.html',context)

def product_search(request):
    if request.method=='POST':
        form=SearchForm(request.POST)
        if form.is_valid():
            category=Category.objects.all()
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid == 0:
                products=Kitap.objects.filter(title__icontains=query)
            else:
                products = Kitap.objects.filter(title__icontains=query,category_id=catid)
            context = {'products': products,
                       'category': category,
                       }
            return render(request, 'products_search.html', context)
    return HttpResponseRedirect('/')
def product_search_auto(request):
    if request.is_ajax():
        q=request.GET.get('term','')
        product=Kitap.objects.filter(title__icontains=q)
        results=[]
        for rs in product:
            product_json={}
            product_json=rs.title
            results.append(product_json)
        data=json.dumps(results)
    else:
        data='fail'
    mimetype='application/json'
    return HttpResponse(data,mimetype)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası !  Kullanıcı adı veya şifre yanlış. ")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'category': category,'setting':setting,}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate( username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               }
    return render(request, 'signup.html', context)