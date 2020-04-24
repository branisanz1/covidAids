from django.contrib.auth import get_user, decorators, authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Ad, User, Conversation, Message
from .forms import ConversationForm
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from .forms import SignupForm, ProfilForm, AnnouncesForm, LoginForm, MessageForm
from django.db.models import Count

def home(request):
    template = loader.get_template('home.html')
    context = {
        "topFive" : User.objects.annotate(num_ads=Count('ad')).order_by('-num_ads')[:5],
        "lastDemand" : Ad.objects.filter(type = 'demand',status= 'online' ).order_by('id')[:5],
        "lastSupply" : Ad.objects.filter(type = 'supply',status= 'online' ).order_by('id')[:5]

    }
    return HttpResponse(template.render(context,request))



def supply(request):
    template = loader.get_template('ad/supply.html')
    result =  Ad.objects.filter(type = 'supply')
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        result = Ad.objects.all().filter(title__contains=search_term, type='supply') 

    context = {
        "ads": result
    }
    return HttpResponse(template.render(context,request))


def demand(request):
    template = loader.get_template('ad/demand.html')
    result =  Ad.objects.filter(type = 'demand')

    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        result = Ad.objects.all().filter(title__contains=search_term, type='demand') 

    context = {
        "ads": result
    }
    return HttpResponse(template.render(context,request))


def detail(request, id):

    template = loader.get_template('ad/detail.html')
    idAd = int(id)
    form = ConversationForm()
    if request.method == 'POST':
        form = ConversationForm(request.POST)
        ad = Ad.objects.get(id=idAd)
        conversation = Conversation.objects.create(ad=ad)
        if form.is_valid():
            conversation.save()
            return redirect('worker:conversation', id=conversation.id)

    try:
        context = {
            "ad":  Ad.objects.get(id = idAd)
        }
    except:
        context = {
            "ad":  None
        }

    if request.method == 'POST':
        form = ConversationForm(request.POST)
        if form.is_valid():
            return HttpResponse(template.render(context,request))

    


    return HttpResponse(template.render(context,request))


@csrf_protect
@requires_csrf_token
def signup(request):
    template = loader.get_template('accounts/signup.html')

    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            context = {
                'form': form
            }
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password1']
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('worker:home')
        else:
            form = SignupForm()
            context = {
                'form': form
            }

        return HttpResponse(template.render(context, request))

    return redirect('worker:home')


@decorators.login_required(login_url='/account/login/')
def profil(request):

    template = loader.get_template('accounts/profil.html')
    user = get_user(request)
    context = {
        "user":  user
    }
    if request.method == 'POST':
            form = ProfilForm(request.POST)
            context = {
                'form': form
            }
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()

           
    else:
        form = ProfilForm(initial={'email': user.email, 'first_name' : user.first_name, 'last_name': user.last_name})
        context = {
            'form': form
        }
    return HttpResponse(template.render(context,request))

@decorators.login_required(login_url='/account/login/')
def announces(request):

    template = loader.get_template('accounts/announces.html')
    user = get_user(request)
    context = {
        "announces":  Ad.objects.filter(user_id = user.id)
    }
 
    return HttpResponse(template.render(context,request))

@decorators.login_required(login_url='/account/login/')
def add_announce(request):

    template = loader.get_template('accounts/add.html')
    user = get_user(request)
    announces = Ad()
    context = {
        "announces":  Ad.objects.filter(user_id = user.id)
    }
    if request.method == 'POST':
            form = AnnouncesForm(request.POST)
            
            if form.is_valid():
                announces.title = form.cleaned_data['title']
                announces.description = form.cleaned_data['description']
                announces.category = form.cleaned_data['category']
                announces.type = form.cleaned_data['type']
                announces.status = "online"
                announces.user = user
                announces.save()
                context = {
                    'form': form,
                    'success': True
                }
           
    else:
        form = AnnouncesForm()
        context = {
            'form': form,
            'success': False
        }
    return HttpResponse(template.render(context,request))



def logout_view(request):
    logout(request)
    return redirect('worker:home')

def login_view(request):
    template = loader.get_template('accounts/login.html')
    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            context= {
                'form': form
            }
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(email=email, password=password)
                if user:
                    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('worker:home')
                else:
                    form = LoginForm()
                    context = {
                        'form' : form,
                        "error" : "Vos identifiants sont incorrects !"
                    }
                
        else:
            form = LoginForm()
            context= {
                'form': form
            }
        return HttpResponse(template.render(context,request))

    return redirect('worker:home')

    
@csrf_protect
@requires_csrf_token
def conversation(request, id):
    template = loader.get_template('ad/conversation.html')
    id = int(id)
    print(id)
    conversation = Conversation.objects.get(id=id)
    print(conversation)

    get_messages = Message.objects.filter(conversation_id=id).order_by('-created')
    form = MessageForm()
    message = Message()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        user = get_user(request)
        message.sender = user
        message.conversation = conversation
        message.content = form.data["content"]
        if form.is_valid():
            message.save()
            context = {
                'conversation': conversation,
                'messages': get_messages,
                'form': form,
            }
            return HttpResponse(template.render(context, request))
    context = {
        'conversation': conversation,
        'messages': get_messages,
        'form': form,
    }
   
    return HttpResponse(template.render(context, request))
