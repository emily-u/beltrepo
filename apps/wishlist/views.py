from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,'wishlist/index.html')

def regis(request):
    result = User.objects.regis_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/main')
    
    request.session['user_id'] = result.id
    return redirect('/dashboard')

def login(request):
    result = User.objects.login_validator(request.POST)
    if not result:
        messages.error(request, "login info invalid")
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/main')

def dashboard(request):
    try:
        context = {
            'user': User.objects.get(id=request.session['user_id']),      
            'all_lists': Wish.objects.all()
  
        }
        return render(request,'wishlist/result.html',context)

    except KeyError:
        return redirect('/main')

def createitems(request):
    if request.method == 'GET':        
        return render(request,'wishlist/add.html')
    if request.method == 'POST':
        errors = User.objects.item_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/wish_items/create')

    else:
        Wish.objects.create(item=request.POST["item"],creator=User.objects.get(id=request.session['user_id']))

        return redirect('/dashboard')

def addtolist(request,itemid):
    Wish.objects.get(id=itemid).follower.add(User.objects.get(id=request.session['user_id']))
        
    return redirect('/dashboard')
    
def remove(request,itemid):
    Wish.objects.get(id=itemid).follower.remove(User.objects.get(id=request.session['user_id']))
        
    return redirect('/dashboard')

def delete(request,itemid):
    User.objects.get(id=request.session['user_id']).createwish.filter(id = itemid).delete()
    return redirect('/dashboard')

def showitem(request,itemid):
    useritems = Wish.objects.get(id=itemid)
    liker = list(useritems.follower.all())

    context = {
        'useritems': useritems,
        'liker': liker,
    }
    return render(request,'wishlist/user.html',context)