from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.contrib import messages
from .forms import Userregisterform,UserUpdateForm,ProfileUpdateForm
from django.http import Http404,HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,ListView
from django.contrib.auth.models import User
from blog.models import Post
from poll.models import Questions,Comments,Tags,likes1,likes2,Collab,dlikes1,dlikes2,Watch
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.urls import reverse
import os
# Create your views here.

def signup(request):
    if request.method=='POST':
        name = request.POST['name']
        email =request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(username=name).first()
        user1 = User.objects.filter(email=email).first()
        if user is None and user1 is None:
            user= User(username=name,email=email,password=make_password(password),first_name=str(0))
            user.is_active = True
            user.save()
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            '''
            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            link =reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            url = domain+link
            send_mail(
		    f'wallpair account activation link',
		    f'Hii {user.username} \n welcome to wallpair \njust click the link given below to Verify and activate your  account \n{url}\n\n if this is not you then sorry we will not send email again\n\n\nthank you team wallpair.com ',
		    'wallpair',
		    [email],
		    fail_silently=False,
		    )'''
            
            #messages.info(request,f'hii {name} your account is created\n')

            #messages.info(request,f'click the link given to your email address to activate your account')
            #return render(request,'users/mailmsg.html')
            messages.info(request,f'Hey {user.username} your account is created and you are logged in')
            return redirect("/")



        else:
            messages.info(request,f'Username or Email is already Registered!')
            return redirect('/register/')
    return render(request,'users/register.html')

@login_required
def profile(request):
	if request.method =='POST':
		user_form = UserUpdateForm(request.POST,instance=request.user)
		profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
		if  user_form.is_valid() and  profile_form.is_valid():
			#messages.success(request,f'hey\t{request.user.username} your acccount is updated!')
			user_form.save()
			profile_form.save()
			return redirect('profile')

	user_form = UserUpdateForm(instance=request.user)
	profile_form = ProfileUpdateForm(instance=request.user.profile)
	context = {'u_form':user_form,'p_form':profile_form}

	return render(request,'users/profile.html',context)


def info(request,pk):

    user = User.objects.get(id=pk)
    ques = Questions.objects.filter(poller=user).order_by('-pk')
    que = Questions.objects.all()
    empty =[]
    for i in que:
    	try:
    		t = i.tags_set.first().users.all()
    		if t is not None:
    			for j in t:
    				if j==user:
    					empty.append(i)
    	except Exception as e:
    		print(e)
    posts = len(ques)
    likes = 0
    coms =0
    for i  in ques:
        likes+=i.vote1
        likes+=i.vote2
        coms+=len(i.comments_set.all())
    return render(request,'users/blogers.html',{'user':user,'data':ques,'likes':likes,'posts':posts,'comments':coms})

def search(request):
    views = 0
    name = request.GET['user']
    user = User.objects.filter(username=name).first()
    que = Questions.objects.all()
    empty =[]
    for i in que:
    	try:
    		t = i.tags_set.first().users.all()
    		if t is not None:
    			for j in t:
    				if j==user:
    					empty.append(i)
    	except Exception as e:
    		print(e)
    if user:
        ques = Questions.objects.filter(poller=user).order_by('-pk')
        ques = [i for i in ques ]
        posts = len(ques)
        likes = 0
        coms =0
        tags = Tags.objects.all()
        youtube= len(Questions.objects.filter(typee="y",poller=user))
        reddit= len(Questions.objects.filter(typee="reddit",poller=user))
        general=len(ques) - (youtube+reddit)
        ques = Questions.objects.filter(poller=user).order_by('-pk')
        que = [i for i in ques ]
        que = [i for i in que ]

        que = [i for i in que if i.iscontest==0]
        return render(request,'users/blogers.html',{'user':user,'data':que,'likes':likes,'posts':posts,'tags':tags,'comments':coms,'views':views,'len':len(empty),'general':general,'youtube':youtube,'reddit':reddit})
    else:
        #messages.info(request,f'Hey {request.user}, no user named {name} found')
        return render(request,'users/nouser.html')


def userlinks(request):
    name = request.GET['search']
    users = User.objects.filter(username__contains=name)
    if users:
        return render(request,'users/userlinks.html',{'users':users})
    return HttpResponse('<h1>no user</h1>')


def check(request):
    if request.method=="POST":
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid details')
            return redirect('/login/')
    return render(request,'users/logins.html')
'''
def check(request):
	if request.method=="POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			messages.success(request,'logged in')
			if request.POST.get('check',None):
				request.session.set_expiry(60*60*24*30)
				questions = Questions.objects.filter(typee='g').order_by('-date_posted')
				context = {'questions':questions}
				new = render(request,'poll/poll-base.html',context=context)
				new.set_cookie('username',username)
				return new
			return redirect('/')
		else:
			messages.info(request,f'password is incorrect')
			return redirect('/login/')
	l = 0
	if 'username' in request.COOKIES:
		l = 1
	if l==1:
			return render(request,'users/logins.html',{'data':request.COOKIES['username']})
	else:
		return render(request,'users/logins.html',{'data':''})
'''
def usertags(request,pk):
	user =  User.objects.filter(pk=pk).first()
	ques = Questions.objects.all()
	print(ques)
	em = []
	for i in ques:
	    	try:
	    		t = i.tags_set.first().users.all()
	    		if t is not None:
	    			for j in t:
	    				if j==user:
	    					em.append(i)
	    	except Exception as e:
	    		print(e)
	tags = Tags.objects.all()
	questions = em
	context = {'questions':questions,'tags':tags}

	return render(request,'users/usertags.html',context)
def userlinks1(request):
	users = User.objects.filter(username__contains=request.GET['search'].lower())
	#users = [i for i in users if i in request.user.profile.follwers.all()]
	if users:
		return render(request,'users/tags.html',{'users':users})
	return None
class Verify(View):
	def get(self,request,uidb64,token):

		uni = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(id=uni)
		if not token_generator.check_token(user,token):
			#messages.success(request,'your acccount has been created click\n the link given to your mail to activate account ')
			return HttpResponse('click on the link given to your mail address to activate your account')
		if user.is_active:
			messages.success(request,'your acccount has been activated')
			return redirect('/login/')
		user.is_active = True
		user.save()
		messages.success(request,'your account has been activated \n')

		messages.success(request,'you are logged in\n')
		login(request,user)
		return redirect('/')

def catuser(request,typee,username):
    user = User.objects.filter(username=username).first()
    t = []
    if typee=="general":
        q = [i for i in Questions.objects.filter(poller=user).order_by('-date_posted') if i.typee!="reddit"]
        q = [i for i in q if i.typee!="y"]
        q = [i for i in q if i.typee!="mpost"]
        for i in q:
            t.append(i)
    else:

        if typee=="y":
            q = Questions.objects.filter(typee="mpost",poller=user).order_by('-date_posted')
            for i in q:
                t.append(i)
        if typee=="memes":
            q = Questions.objects.filter(typee="reddit",poller=user).order_by('-date_posted')
            for i in q:
                t.append(i)
        q = Questions.objects.filter(typee=typee,poller=user).order_by('-date_posted')
        for i in q:
            t.append(i)

    tag = Tags.objects.all()
    return render(request,'users/catuser.html',{'data':t,'tags':tag})
@login_required
def follow(request,pk):
	user = User.objects.get(id=pk)
	current_user = request.user
	if current_user in user.profile.follwers.all():

		user.profile.follwers.remove(current_user)
		user.save()
		user.profile.save()
		current_user.profile.following.remove(user)
		current_user.save()
		current_user.profile.save()
		return redirect(f'/search/?user={user}')
	else:
		if user.profile.typee==1:
			if request.user in user.profile.pending.all():

				user.profile.pending.remove(current_user)
				user.save()
				user.profile.save()
				messages.info(request,f'you removed request')
				return redirect(f'/search/?user={user}')
			else:
				user.profile.pending.add(current_user)
				user.save()
				user.profile.save()
				messages.info(request,f'requested')
				return redirect(f'/search/?user={user}')


		else:
			user.profile.follwers.add(current_user)
			user.save()
			user.profile.save()
			current_user.profile.following.add(user)
			current_user.save()
			current_user.profile.save()
			messages.info(request,f'followed')

			return redirect(f'/search/?user={user}')


@login_required
def updateuser(request):
    if request.method=="POST":
        user = User.objects.filter(email=request.POST['email']).first()
        user1 = User.objects.filter(username=request.POST['username']).first()
        request.user.username = request.POST['username']
        request.user.email = request.POST['email']
        if request.FILES.get('pic',None):
            request.user.profile.image = request.FILES['pic']
        if request.POST['link']!="":
            request.user.profile.link= request.POST['link']
        request.user.profile.bio = request.POST['bio']
        request.user.profile.save()
        request.user.save()
        messages.success(request,'updated')
        return redirect('updateuser')
    return render(request,'users/new_profile.html',{'user':request.user})

@login_required
def updateaccount(request):
    if request.method=="POST":
        request.user.profile.typee = int(request.POST['typee'])
        request.user.profile.clone = int(request.POST['repost'])
        request.user.profile.save()
        messages.success(request,'updated')
        return redirect('updateaccount')
    return render(request,'users/new_account.html',{'user':request.user})

def requestusers(request):
    return render(request,'users/requestuser.html',{'user':request.user})






@login_required
def addme(request,username):
	user = User.objects.filter(username=username).first()
	if user is not None:
		request.user.profile.follwers.add(user)
		user.profile.pending.remove(user)
		user.profile.following.add(request.user)
		user.profile.save()

		request.user.save()
		request.user.profile.save()
		
		messages.success(request,'added')
		return  redirect(f'/follwer/{request.user.username}')
	return  HttpResponse('user not found')

#to remove user from following and request list
@login_required
def removeme(request,username):
	user = User.objects.filter(username=username).first()
	if user is not None:
		request.user.profile.pending.remove(user)
		request.user.profile.following.remove(user)
		user.profile.follwers.remove(request.user)
		user.profile.save()


		request.user.save()
		request.user.profile.save()
		messages.success(request,'removed')
		return  redirect(f'/following/{request.user}')
	return  HttpResponse('user not found')

#to remove user from followers list
@login_required
def removeme1(request,username):
	user = User.objects.filter(username=username).first()
	if user is not None:
		request.user.profile.follwers.remove(user)

		request.user.save()
		request.user.profile.save()
		user.profile.following.remove(request.user)
		user.profile.save()
		
		messages.success(request,'removed from followers')
		return  redirect(f'/follwer/{request.user}')
	return  HttpResponse('user not found')

@login_required
def followinguser(request,username):
    user = User.objects.filter(username=username).first()
    if user is not None:
        c=1
        if request.user in user.profile.follwers.all() or request.user.username == username or user.profile.typee==0:
            c = 2
        if c==2:
            users = user.profile.following.all()

            return render(request,'users/follwinguser.html',{'users':users,'myuser':user})
        messages.info(request,'you must follow that user to see profile')
        return redirect(f'/search/?user={username}')
    messages.info(request,'user not found')
    return redirect('/')
@login_required
def follwersuser(request,username):
    user = User.objects.filter(username=username).first()
    if user is not None:
        c = 1
        if request.user in user.profile.follwers.all() or request.user.username == username or user.profile.typee==0:
            c = 2
        if c==2:
            users = user.profile.follwers.all()
            return render(request,'users/followeruser.html',{'users':users,'myuser':user})

        messages.info(request,'you must follow that user to see profile')
        return redirect(f'/search/?user={username}')
    messages.info(request,'user not found')
    return redirect('/')

@login_required
def savepost(request,pk):
    post = Questions.objects.filter(id=pk).first()
    if post is not None:
        request.user.profile.mysave.add(post)
        request.user.profile.save()
        return HttpResponse('saved to favourites')
    return HttpResponse('post does not exist')
@login_required
def showsave(request):
    context = {'data':request.user.profile.mysave.all().order_by('-date_posted'),'tags':Tags.objects.all()}
    return render(request,'users/savepost.html',context)
@login_required
def unsavepost(request,pk):
    post = Questions.objects.filter(id=pk).first()
    if post is not None:
        request.user.profile.mysave.remove(post)
        request.user.profile.save()
        messages.info(request,'removed from saved')
        return redirect('/')
    return HttpResponse('post does not exist')


def see(request):
    return render(request,'users/see.html')
    
@login_required
def settings(request):
    return render(request,'users/settings.html')
@login_required
def collab(request):
    user = User.objects.filter(username=request.GET['user']).first()
    try:
        if request.method=="POST":
            image1= request.FILES['image']
            title =request.POST['caption']
            typee = int(request.POST['typee'])

            q = Collab(poller=request.user,image1=image1,typee=typee,other=user,question=title)
            q.save()
            user.share.done.add(q)
            user.share.save()
            request.user.share.pend.add(q)
            request.user.share.save()
            messages.info(request,'collab send successfully')
            return redirect(f'/search/?user={user.username}')
    except Exception as e:
        return redirect('/')
    user = User.objects.filter(username=request.GET['user']).first()
    if user is not None:
        if request.user in user.profile.following.all() and user in request.user.profile.follwers.all():
            return render(request,'users/collab.html',{'username':user.username})
        else:
            messages.info(request,f'{user.username} and you must follow each other')
            return redirect(f'/search/?user={user.username}')
@login_required
def showcollab(request):
    q = request.user.share.done.all()

    return render(request,'users/showcollab.html',context={'q':q,'len':len(q)})

@login_required
def acceptcollab(request,id):
    q = Collab.objects.filter(id=id).first()
    if request.method=="POST":
        q.image2= request.FILES['image']
        q.save()
        
        y = Questions(poller=q.poller,question=q.question,image1=q.image1,image2=q.image2,kick=1)
        
        y.save()
        l1 =likes1(poll=y)
        l2 =likes2(poll=y)
        l1.save()
        l2.save()
        dl1 =dlikes1(poll=y)
        dl2  = dlikes2(poll=y)
        dl1.save()
        dl2.save()
        w = Watch(poll=y)
        w.save()
        tag = Tags(poll=y)
        tag.save()
        tag.users.add(request.user)
        tag.save()

        q.delete()
        user = User.objects.filter(username=q.other.username).first()
        request.user.share.done.remove(q)
        request.user.save()
        user.share.pend.remove(q)
        user.save()
        
        messages.info(request,f'posted')
        return redirect(f'/votes/{y.id}')
    if q is not None:
        return render(request,'users/acceptcollab.html',context={'i':q})
    else:
        return HttpResponse('collab does not exits')
@login_required
def removecollab(request,id):
    q = Collab.objects.filter(id=id).first()
    if q is not None:
        user = User.objects.filter(username=q.poller.username).first()
        user2 = User.objects.filter(username=q.other.username).first()
        user2.share.done.remove(q)
        user2.share.save()
        user.share.pend.remove(q)
        user.share.save()
        #os.remove(q.image1.url)
        messages.info(request,'collab removed')
        return redirect('/settings/')
@login_required
def send(request):
    q = request.user.share.pend.all().order_by('-date_posted')
    return render(request,'users/send.html',context={'q':q,'len':len(q)})
@login_required
def recieved(request):
    q = request.user.share.done.all().order_by('-date_posted')
    return render(request,'users/recieved.html',context={'q':q,'len':len(q)})

    