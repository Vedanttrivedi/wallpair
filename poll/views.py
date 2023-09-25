from django.shortcuts import render,redirect,get_object_or_404,reverse,get_list_or_404
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Questions,Comments,Reviews,Apppolls,Tags,likes1,dlikes1,likes2,dlikes2,Watch,Collab
from .forms import QuestionCreateForm
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
import requests,json
from apiclient.discovery import build



def PollListView(request):
    color = "white"
    if request.user.is_authenticated:
        request.session.set_expiry(60*60*24*50)
        current_user = request.user
        users = current_user.profile.following.all()
        questions = Questions.objects.exclude(typee="reddit",iscontest=1).order_by('-date_posted')
        q = []
        for i in questions:
            
            if i.poller.id == request.user.id or i.poller in request.user.profile.following.all():
                if i.iscontest == 0:
                    q.append(i)
                
        return render(request,'poll/poll-base.html',{'tags':Tags.objects.all(),'questions':q,'len':len(q)})
    else:
        #return HttpResponse('wallpair')
        questions = Questions.objects.filter(typee="general").order_by('-date_posted')
        questions = [i for i in questions if i.poller.profile.typee!=1 and i.iscontest==0]
        return render(request,'poll/poll-base.html',{'tags':Tags.objects.all(),'questions':questions,'len':len(questions)})
        


def explore(request):
    users = [i for i in User.objects.all() if i.profile.typee == 0 and i not in request.user.profile.following.all() and i!=request.user]
    q = []

    for i in  Questions.objects.filter(typee="general").order_by('-date_posted'):
        for j in users:
            if i.poller==j and i.iscontest==0:
                q.append(i)
             
    tags = Tags.objects.all()
    #q = Questions.objects.all()
    return render(request,'poll/explore.html',{'data':q,'tags':tags,'len':len(q)})

def savecode(poll):
	l1d = len(Reviews.objects.filter(pid=poll,l1=1))
	dl1d = len(Reviews.objects.filter(pid=poll,dl1=1))
	l2d = len(Reviews.objects.filter(pid=poll,l2=1))
	dl2d = len(Reviews.objects.filter(pid=poll,dl2=1))
	poll.vote1 = l1d
	poll.dvote1 = dl1d
	poll.vote2 = l2d
	poll.dvote2 = dl2d
	poll.save()


@login_required
def PollCreateViewd(request):
	try:
		if request.method=="POST":
			data = request.POST['question']
			img1 = request.FILES['img1']
			img2 = request.FILES['img2']
			string = str(request.POST['doe'])
			string =string.split(',')
			x = 0
			print(string)
			if len(string)!=0:
				for i in range(len(string)-1):
					for j in range(i+1,len(string)-1):
						if(string[i]==string[j]):
							x+=1
							print(len(string))
							messages.warning(request,'you cannot add same friend')
							return redirect('/create')
					if(string[i]==request.user.username):
						del string[i]

			print(data,request.FILES['img1'])
			if(str(img1).endswith('.gif') and not str(img2).endswith('.gif')) or (str(img2).endswith('.gif') and not str(img1).endswith('.gif')):
			    messages.warning(request,'both must be either gifs or images '.title())
			    return redirect('/create')
			if  not str(img1).endswith('.jpg'):
				if not str(img1).endswith('.jpeg'):
					if not str(img1).endswith('.png') :
					    if not str(img1).endswith('.gif') :
						    messages.warning(request,'invalid file format'.title())
						    return redirect('/create')
			if  not str(img2).endswith('.jpg'):
				if not str(img2).endswith('.jpeg'):
					if not str(img2).endswith('.png'):
					    if not str(img2).endswith('.gif'):
						    messages.warning(request,'invalid file format'.title())
						    return redirect('/create')
			if(request.POST.get('show',None)):
				if len(string)<5:
					messages.warning(request,'you must select 4 or more friends')
					return redirect('/create')
				image = Questions(show=1,poller=request.user,question=data,image1=img1,image2=img2,typee=request.POST['type'])
			else:
				image = Questions(show=0,poller=request.user,question=data,image1=img1,image2=img2,typee=request.POST['type'])
			tag  = Tags(poll=image)
			image.save()
			l1 = likes1(poll=image)

			l1.save()
			dl1 = dlikes1(poll=image)
			dl1.save()
			l2 = likes2(poll=image)
			l2.save()
			dl2 = dlikes2(poll=image)
			watch = Watch(poll=image)
			watch.save()
			dl2.save()
			tag.save()
			for i in range(len(string)-1):
				user  = User.objects.filter(username=string[i]).first()
				tag.users.add(user)
			tag.save()
			return redirect('/')
	except Exception as e:
		print(e)
		return redirect(f'/votes/{image.id}')
	return render(request,'poll/forms.html')


@login_required
def YPollCreateView(request):
	if request.method=="POST":
		data = request.POST['question']
		url1 = request.POST['urlo']
		url2= request.POST['urlt']

		if url1==url2:
			messages.warning(request,f'youtubers cannot be same!')
			return redirect('/ycreate/')
		if not 'http' in url1 or (not 'http' in url2):
		    messages.warning(request,f'invalid url!')
		    return redirect('/ycreate/')


		string = str(request.POST['doe'])
		string =string.split(',')
		x = 0
		print(string)
		if len(string)!=0:
			for i in range(len(string)-1):
				for j in range(i+1,len(string)-1):
					if(string[i]==string[j]):
						x+=1
						print(len(string))
						messages.warning(request,'you cannot add same friend')
						return redirect('/ycreate')
				if(string[i]==request.user.username):
					del string[i]
		try:
			path = requests.get(f'https://www.googleapis.com/youtube/v3/search/?key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs&part=snippet&q={url1}')
			path1 = requests.get(f'https://www.googleapis.com/youtube/v3/search/?key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs&part=snippet&q={url2}')
			t = json.loads(path.text)
			t1 = json.loads(path1.text)
			cid1 = t['items'][0]['snippet']['channelId']
			cid2 = t1['items'][0]['snippet']['channelId']
			username1 = t['items'][0]['snippet']['channelTitle']
			username2 = t1['items'][0]['snippet']['channelTitle']
			if cid1==cid2:
				messages.warning(request,f'youtubers must be different!')
				return redirect('/ycreate/')

			ytube = build('youtube','v3',developerKey='AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			req= ytube.channels().list(part='statistics',id=cid1)
			ress = req.execute()
			video_count1 = ress['items'][0]['statistics']['videoCount']
			subs_count1 = ress['items'][0]['statistics']['subscriberCount']
			view_count1 = ress['items'][0]['statistics']['viewCount']
			req= ytube.channels().list(part='snippet',id=cid1)
			ress = req.execute()
			image_url1 =ress['items'][0]['snippet']['thumbnails']['medium']['url']

			ytube = build('youtube','v3',developerKey='AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			req= ytube.channels().list(part='statistics',id=cid2)
			ress = req.execute()
			video_count2 = ress['items'][0]['statistics']['videoCount']
			subs_count2 = ress['items'][0]['statistics']['subscriberCount']
			view_count2 = ress['items'][0]['statistics']['viewCount']
			req= ytube.channels().list(part='snippet',id=cid2)
			ress = req.execute()
			image_url2 =ress['items'][0]['snippet']['thumbnails']['medium']['url']

			q = Questions(poller=request.user,typee='y',question=data)
			q.save()
			l1 = likes1(poll=q)
			l1.save()
			dl1 = dlikes1(poll=q)
			dl1.save()
			l2 = likes2(poll=q)
			l2.save()
			dl2 = dlikes2(poll=q)
			dl2.save()
			tag = Tags(poll=q)
			tag.save()
			watch = Watch(poll=q)
			watch.save()

			for i in range(len(string)-1):
			    user  = User.objects.filter(username=string[i]).first()
			    tag.users.add(user)

			p = Apppolls(question=q,image1=image_url1,image2=image_url2,
			subs1=subs_count1,subs2=subs_count2,views1=video_count1,views2=video_count2,
			channel1=username1,channel2=username2,likes1=view_count1,likes2=view_count2)
			p.save()
			tag.save()

			messages.info(request,f'poll added')
			return redirect(f'/votes/{q.id}')
		except Exception as e:
			messages.warning(request,f'sorry,something went wrong\n,please try again!')
			q.delete()
			return redirect('/ycreate')
	return render(request,'poll/yforms.html')

def ypolls(request):
	questions = Questions.objects.filter(typee='y').order_by('-date_posted')
	context = {'questions':questions}
	return render(request,'poll/poll-youtube.html',context)


class PollCreateView(LoginRequiredMixin,CreateView):
	model = Questions
	fields = ['question','image1','image2']
	success_url = '/'
	template_name = 'poll/forms.html'

	def form_valid(self,form):
		form.instance.poller = self.request.user
		return super().form_valid(form)

def UserCreate(request):
	context = {
	'form':UserRegisterForm()
	}
	return render(request,'poll/poll-u-form.html',context)


def vote(request,pk):
    if not request.user.is_authenticated or request.user == 'AnonymousUser':
        poll = get_object_or_404(Questions,pk=pk)
        comments  = Comments.objects.filter(question=poll).order_by('-date_posted')
        context = {'data':poll,'comments':comments,'len':len(comments),'ul1d':0,'udl1d':0,'ul2d':0,'udl2d':0}
        return render(request,'poll/votes.html',context)
    if request.method=='POST':
        poll = get_object_or_404(Questions,pk=request.POST['pk'])
        if int(request.POST['l1'])==1:
            lt = likes1.objects.filter(poll=poll).first()
            lt.users.add(request.user)
            lt.save()
        else:
            lt = likes1.objects.filter(poll=poll).first()
            lt.users.remove(request.user)
            lt.save()
        if int(request.POST['dl1'])==1:


        	lt = dlikes1.objects.filter(poll=poll).first()
        	lt.users.add(request.user)
        	lt.save()
        else:
        	lt = dlikes1.objects.filter(poll=poll).first()
        	lt.users.remove(request.user)
        	lt.save()
        if int(request.POST['l2'])==1:
        	lt = likes2.objects.filter(poll=poll).first()
        	lt.users.add(request.user)
        	lt.save()
        else:
        	lt = likes2.objects.filter(poll=poll).first()
        	lt.users.remove(request.user)
        	lt.save()

        if int(request.POST['dl2'])==1:
        	lt = dlikes2.objects.filter(poll=poll).first()
        	lt.users.add(request.user)
        	lt.save()
        	return HttpResponse(f'job111 done')
        else:
        	lt = dlikes2.objects.filter(poll=poll).first()
        	lt.users.remove(request.user)
        	lt.save()
        	return HttpResponse(f'job111 done')
        return HttpResponse(f'job done')

    poll = get_object_or_404(Questions,pk=pk)
    comments  = Comments.objects.filter(question=poll).order_by('-date_posted')
    like = Reviews.objects.filter(pid=poll,uid=request.user).first()
    if like is  None:
    	like = Reviews(pid=poll,uid=request.user)
    	like.save()
    	like = Reviews.objects.filter(pid=poll,uid=request.user).first()
    ul1d=0
    udl1d=0
    ul2d=0
    udl2d=0
    print(12)
    l1d = likes1.objects.filter(poll=poll).first()

    for i in l1d.users.all():
    	print(1234)
    	if i.username==request.user.username:
    		ul1d=1
    		break

    l1d = l1d.users.count()
    dl1d = dlikes1.objects.filter(poll=poll).first()

    for i in dl1d.users.all():
    	if i.username==request.user.username:
    		udl1d=1

    dl1d = dl1d.users.count()
    l2d = likes2.objects.filter(poll=poll).first()

    for i in l2d.users.all():
    	if i.username==request.user.username:
    		ul2d=1

    l2d = l2d.users.count()
    dl2d = dlikes2.objects.filter(poll=poll).first()
    for i in dl2d.users.all():
    	if i.username==request.user.username:
    		udl2d=1
    request.session.set_expiry(60*60*24*60)
    dl2d = dl2d.users.count()
    if poll.show==1:
        tag = Tags.objects.filter(poll=poll).first()
        if request.user in tag.users.all() or request.user==poll.poller:
            context = {'data':poll,'comments':comments,'len':len(comments),'ul1d':ul1d,'udl1d':udl1d,'ul2d':ul2d,'udl2d':udl2d}
            return render(request,'poll/votes.html',context)
        else:
            return HttpResponse('<h1 style="color:red;">you are not allowd to view this poll</h1>')

    if poll.poller.profile.typee==1 and request.user in poll.poller.profile.follwers.all():
	    context = {'data':poll,'comments':comments,'len':len(comments),'ul1d':ul1d,'udl1d':udl1d,'ul2d':ul2d,'udl2d':udl2d}
	    return render(request,'poll/votes.html',context)
    if poll.poller.profile.typee==0 or poll.poller==request.user:
        total = ul1d+ul2d
        context = {'data':poll,'comments':comments,'len':len(comments),'ul1d':ul1d,'udl1d':udl1d,'ul2d':ul2d,'udl2d':udl2d,'total':total}
        return render(request,'poll/votes.html',context)
    messages.info(request,f'follow {poll.poller.username} to see this post')
    return redirect(f'/search/?user={poll.poller.username}')



@login_required
def vote1(request):
    if request.method=='GET':
        pk=request.GET['pk']
        poll = get_object_or_404(Questions,id=pk)
        user = User.objects.filter(id=request.user.id).first()
        if int(request.GET['l1'])==1:
            lt = likes1.objects.filter(poll=poll).first()
            lt.users.add(user)
            lt.save()
            if int(request.GET['l2'])==1:
                request.GET['l2'] = 0

        else:
            lt = likes1.objects.filter(poll=poll).first()
            lt.users.remove(user)
            lt.save()
        if int(request.GET['dl1'])==1:


        	lt = dlikes1.objects.filter(poll=poll).first()
        	lt.users.add(user)
        	lt.save()
        else:
        	lt = dlikes1.objects.filter(poll=poll).first()
        	lt.users.remove(user)
        	lt.save()
        if int(request.GET['l2'])==1:
        	lt = likes2.objects.filter(poll=poll).first()
        	lt.users.add(user)
        	lt.save()
        else:
        	lt = likes2.objects.filter(poll=poll).first()
        	lt.users.remove(user)
        	lt.save()

        if int(request.GET['dl2'])==1:
        	lt = dlikes2.objects.filter(poll=poll).first()
        	lt.users.add(user)
        	lt.save()
        	return HttpResponse(f'job111 done')
        else:
        	lt = dlikes2.objects.filter(poll=poll).first()
        	lt.users.remove(user)
        	lt.save()
        	return HttpResponse(f'job111 done')
        return HttpResponse(f'job done')
    raise Http404()

@login_required
def com(request):
	if request.method=='POST':
		question = get_object_or_404(Questions,pk=int(request.POST['qid']))
		user = get_object_or_404(User,username=request.POST['author'])
		com = Comments(author=user,question=question,content=request.POST['content'])
		com.save()
		return redirect(f'/votes/{question.id}')
	else:
		raise Http404()

def up(request,pk):
	autho = User.objects.filter(id=pk).first()
	polls = Questions.objects.filter(poller=autho)
	return render(request,'poll/up.html',{'data':polls})

@login_required
def userlikes(request,pk,string):
	poll = Questions.objects.filter(id=pk).first()
	polls = poll
	user1 = User.objects.filter(id=request.user.id).first()
	if string=="l1":
		poll = likes1.objects.filter(poll=poll).first()
	if string=="l2":
		poll = likes2.objects.filter(poll=poll).first()
	if string=="dl1":
		poll = dlikes1.objects.filter(poll=poll).first()
	if string=="dl2":
		poll = dlikes2.objects.filter(poll=poll).first()
	users = []
	for i in poll.users.all():
	    users.append(i)
	return render(request,'poll/userlikes.html',{'users':users,'len':len(users),'poll':polls})


@login_required
def kickpoller(request,pk):
    user = User.objects.filter(pk=request.user.id).first()
    poll = Questions.objects.filter(pk=pk).first()
    user2 = User.objects.filter(pk=poll.poller.id).first()
    if request.user==poll.poller:
        messages.warning(request,f'you cannot kick yourself!')
        return redirect(f'/votes/{poll.id}')
    t = 0
    watch = Watch.objects.filter(poll=poll).first()
    if user in watch.users.all():
        if user.first_name=="":
            user.first_name=0
        user.first_name = str(int(user.last_name)+1)
        messages.info(request,'lol,you are here after watching likes')
        return redirect(f'/votes/{poll.id}')

    l1 = likes1.objects.filter(poll=poll).first()
    if l1.users.all() is not None:
    	if user2 in l1.users.all():
    		t+=1
    		l1.users.remove(user2)
    l2 = likes2.objects.filter(poll=poll).first()
    if l2.users.all() is not None:
    	if user2 in l2.users.all():
    		t+=1
    		l2.users.remove(user2)
    d1 = dlikes1.objects.filter(poll=poll).first()
    if d1.users.all() is not None:
    	if user2 in d1.users.all():
    		t+=1
    		d1.users.remove(user2)
    d2 = dlikes2.objects.filter(poll=poll).first()
    if d2.users.all() is not None:
    	if user2 in d2.users.all():
    		t+=1
    		d2.users.remove(user2)

    if t!=0:
        if user.first_name=="":
            user.first_name=0
        if user.last_name=="":
            user.last_name=0

        user.first_name = str(int(user.first_name)+1)
        user2.last_name = str(int(user.first_name)+1)
        user.save()
        user2.save()
        poll.kick+=1
        poll.save()
        messages.success(request,f'kicked')
        return redirect(f'/votes/{poll.id}')
    else:
        if user.last_name=="":
            user.last_name=0
        user.last_name = str(int(user.last_name)+1)
        messages.success(request,'lol')
        return redirect(f'/votes/{poll.id}')

def tages(request,pk):
	poll = Questions.objects.filter(pk=pk).first()
	tags = []
	try:
	    tags = poll.tags_set.first().users.all()
	except Exception as e:
	    print(e)
	return render(request,'poll/tagers.html',{'users':tags,'poll':poll,'len':len(tags)})
@login_required
def update(request,pk):
	poll = Questions.objects.filter(pk=pk).first()
	if request.method=="POST" and request.user==poll.poller:
		poll.question = request.POST['q']
		poll.save()
		messages.success(request,'updated!')
		return redirect(f'/votes/{poll.id}')
	return render(request,'poll/poll_update.html',{'poll':poll})
@login_required
def delete(request):
	if request.method=="POST":
		poll = Questions.objects.filter(pk=int(request.POST['dlq'])).first()
		poll.delete()
		messages.success(request,'poll deleted successfully!')
		return redirect('/')
	return HttpResponse('hello')

@login_required
def comupdate(request,pk):
    if request.method=="POST":
        com = Comments.objects.filter(pk=pk).first()
        poll = Questions.objects.filter(pk=com.question.pk).first()
        com.content = request.POST['com']
        com.save()
        messages.success(request,f'comment updated successfully!')
        return redirect(f'/votes/{com.question.pk}')
    com = Comments.objects.filter(pk=pk).first()
    poll = Questions.objects.filter(pk=pk).first()
    if com.author==request.user:
        return render(request,'poll/com_update.html',{'com':com})
    return Http404()
@login_required
def delcom(request):
    com = Comments.objects.filter(pk=int(request.POST['com'])).first()
    f = com.question.pk
    if request.user == com.author:
        com.delete()
        messages.success(request,f'comment deleted successfully!')
        return redirect(f'/votes/{f}')
    return Http404()

def repcom(request):
	if request.method=='POST':
		question = get_object_or_404(Questions,pk=int(request.POST['qid']))
		user = get_object_or_404(User,username=request.POST['author'])
		com1 =Comments.objects.filter(id=request.POST['parent']).first()
		com = Comments(author=user,question=question,content=request.POST['content'],parent=com1)
		com.save()
		messages.success(request,f'Reply Posted!')
		return redirect(f'/votes/{question.id}')
	else:
		raise Http404()


def cat(request,string):
    t = []
    if string=="memes":
        questions = Questions.objects.filter(typee="reddit",).order_by('-date_posted')
        for i in questions:
            t.append(i)
    questions = Questions.objects.filter(typee=string).order_by('-date_posted')
    for i in questions:
            t.append(i)
    if string=="collabs":
        questions =  Questions.objects.filter(kick=1).order_by('-date_posted')
    for i in questions:
            t.append(i)
    tags = Tags.objects.all()
    if string=="y":
        string="youtubers"
    if string=="mpost":
        string = "youtube videos"
    t = [i for i in t if i.poller.profile.typee==0]
    context = {'questions':t,'tags':tags,'len':len(t),'thing':string}
    return render(request,'poll/poll-uba.html',context)



def topcharts(request):
    q = Questions.objects.all().order_by('-date_posted')
    user =len(User.objects.all())
    perc = int(user * 30/100)
    data = []
    new_data  =[]
    for i in q:
    	y = i.likes2_set.first()
    	if y is not None:
    		y = y.users.count()
    	else:
    		y = 0
    	k = i.likes1_set.first()
    	if k is not None:
    		k = k.users.count()
    	else:
    		k = 0
    	h = i.dlikes1_set.first()
    	if h is not None:
    		h = h.users.count()
    	else:
    		h = 0
    	s= i.dlikes2_set.first()
    	if s is not None:
    		s = s.users.count()
    	else:
    		s = 0
    	if(y+k+h)>=perc:
    		data.append(i)

    for  i in range(len(data)):
        for j in range(len(data)):
            y = data[i].likes2_set.first()
            if y is not None:
                y = y.users.count()
            else:
                y = 0
            k = data[i].likes1_set.first()
            if k is not None:
                k = k.users.count()
            else:
                k = 0
            h = data[i].dlikes1_set.first()
            if h is not None:
                h = h.users.count()
            else:
                h = 0
            s= data[i].dlikes2_set.first()
            if s is not None:
                s = s.users.count()
            else:
                s = 0
            p1 = y + k + h +s
            y = data[j].likes2_set.first()
            if y is not None:
                y = y.users.count()
            else:
                y = 0
            k = data[j].likes1_set.first()
            if k is not None:
                k = k.users.count()
            else:
                k = 0
            h = data[j].dlikes1_set.first()
            if h is not None:
                h = h.users.count()
            else:
                h = 0
            s= data[j].dlikes2_set.first()
            if s is not None:
                s = s.users.count()
            else:
                s = 0
            p2 = y + k + h +s

            if p1>p2:
                t = data[i]
                data[i] = data[j]
                data[j] = t

    tags = Tags.objects.all()
    return render(request,'poll/topcharts.html',{'data':data,'tags':tags,'len':len(data)})
@login_required
def lik1(request):
    pk = int(request.GET['pk'])
    poll =Questions.objects.filter(pk=pk).first()
    t = poll.likes1_set.first()
    user = User.objects.filter(id=request.user.id).first()
    if user in t.users.all():
        t.users.remove(user)
        t.save()
    else:
        t.users.add(user)
        t.save()
    t = likes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    t = dlikes1.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()

    return HttpResponse('ok')
@login_required
def dlik1(request):
    pk = request.GET['pk']
    poll =Questions.objects.filter(id=pk).first()
    t = dlikes1.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    else:
        t.users.add(request.user)
        t.save()
    t = dlikes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    t = likes1.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    return HttpResponse('ok')
@login_required
def lik2(request):
    pk = request.GET['pk']
    poll =Questions.objects.filter(id=pk).first()
    t = likes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    else:
        t.users.add(request.user)
        t.save()
    t = likes1.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    t = dlikes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    return HttpResponse('ok')
@login_required
def dlik2(request):
    pk = request.GET['pk']
    poll =Questions.objects.filter(id=pk).first()
    t = dlikes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    else:
        t.users.add(request.user)
        t.save()
    t = likes2.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    t = dlikes1.objects.filter(poll=poll).first()
    if request.user in t.users.all():
        t.users.remove(request.user)
        t.save()
    return HttpResponse('ok')
def random(request):
	return render(request,'poll/random.html')
def randomgame(request,what):
	games = Questions.objects.filter(typee=what,show=0)
	gaming = [i for i in games]
	user = len(User.objects.all())
	if len(gaming)>=2:
		for i in range(len(gaming)):
			for j in range(len(gaming)):
				if i!=j:
					y = gaming[i].likes2_set.first()
					if y is not None:
						y = y.users.count()
					else:
					    y = 0
					k =gaming[i].likes1_set.first()
					if k is not None:
					    k = k.users.count()
					else:
					    k = 0
					h = gaming[i].dlikes1_set.first()
					if h is not None:
					    h = h.users.count()
					else:
					    h = 0
					s= gaming[i].dlikes2_set.first()
					if s is not None:
					    s = s.users.count()
					else:
					    s = 0
					p1 = y + k + h +s
					y = gaming[j].likes2_set.first()
					if y is not None:
					    y = y.users.count()
					else:
					    y = 0
					k = gaming[j].likes1_set.first()
					if k is not None:
					    k = k.users.count()
					else:
					    k = 0
					h = gaming[j].dlikes1_set.first()
					if h is not None:
					    h = h.users.count()
					else:
					    h = 0
					s= gaming[j].dlikes2_set.first()
					if s is not None:
					    s = s.users.count()
					else:
					    s = 0
					p2 = y + k + h +s

					if p1>p2:
					    t = gaming[i]
					    gaming[i] = gaming[j]
					    gaming[j] = t
		imgs = []
		walluser = User.objects.filter(username="wallpall").first()
		fuser  = Questions.objects.filter(id=gaming[0].id).first()
		fuser = fuser.poller
		suser  = Questions.objects.filter(id=gaming[1].id).first()
		suser = suser.poller
		if fuser!=walluser and suser!=walluser:
			if fuser!=suser:
				count = 0
				l1users = likes1.objects.filter(poll=gaming[0]).first().users.count()

				first = ((likes1.objects.filter(poll=gaming[0]).first().users.count() + dlikes1.objects.filter(poll=gaming[0]).first().users.count()  + likes2.objects.filter(poll=gaming[0]).first().users.count() +dlikes2.objects.filter(poll=gaming[0]).first().users.count())  * 100 ) / user
				if int(first)>=40:
					first = likes1.objects.filter(poll=gaming[0]).first().users.count()+ dlikes2.objects.filter(poll=gaming[0]).first().users.count()
					second = likes2.objects.filter(poll=gaming[0]).first().users.count()+ dlikes1.objects.filter(poll=gaming[0]).first().users.count()
					if (int(first)> int(second)):
						imgs.append(gaming[0].image1.name)
						count+=1
					else:
						imgs.append(gaming[0].image2.name)
						count+=1
				second = ((likes1.objects.filter(poll=gaming[1]).first().users.count() + dlikes1.objects.filter(poll=gaming[1]).first().users.count()  + likes2.objects.filter(poll=gaming[1]).first().users.count() +dlikes2.objects.filter(poll=gaming[1]).first().users.count())  * 100 ) / user
				if int(second)>=30:
					first = likes1.objects.filter(poll=gaming[1]).first().users.count()+ dlikes2.objects.filter(poll=gaming[1]).first().users.count()
					second = likes2.objects.filter(poll=gaming[1]).first().users.count()+ dlikes1.objects.filter(poll=gaming[1]).first().users.count()
					if (int(first)> int(second)):
						imgs.append(gaming[1].image1.name)
						count+=1
					else:
						imgs.append(gaming[1].image2.name)
						count+=1
				if count==2:
					image1 = str(imgs[0])

					image2 = str(imgs[1])
					us = User.objects.filter(username="wallpall").first()
					q = Questions.objects.filter(poller=us,typee=what).first()
					if q is not None:
					    if q.image1.name == image1 and q.image2.name == image2:
						    tagers = Tags.objects.all()
						    ert = []
						    ert.append(q)
						    return render(request,'poll/randomgame.html',{'questions':ert,'tags':tagers})

					q = Questions.objects.filter(poller=us,typee=what).all()
					q.delete()
					us = User.objects.filter(username="wallpall").first()
					q = Questions(poller=us,question =f"best in the {what}",image1=image1,image2=image2,typee=what)

					q.save()
					l1 = likes1(poll=q)

					l1.save()
					dl1 = dlikes1(poll=q)
					dl1.save()
					l2 = likes2(poll=q)
					l2.save()
					dl2 = dlikes2(poll=q)
					dl2.save()
					tag = Tags(poll=q)
					tag.save()
					tag.users.add(fuser)
					tag.users.add(suser)

					tags = Tags.objects.all()
					questions = []
					questions.append(q)
					return render(request,'poll/randomgame.html',{'questions':questions,'tags':tags})
				return HttpResponse('no eligble polls for this category')
	return HttpResponse(f'no random poll is available for {what} category')

@login_required
def memers(request):
	if request.method=="POST":
		path = requests.get(f'https://meme-api.herokuapp.com/gimme')
		t = json.loads(path.text)
		poll = Questions(poller=request.user,question="Random Reddit",typee="reddit")
		poll.save()
		apppolls = Apppolls(question=poll,image1=t['url'],channel1=t['postLink'],channel2="e")
		apppolls.save()
		l1 = likes1(poll=poll)

		l1.save()
		dl1 = dlikes1(poll=poll)
		dl1.save()
		l2 = likes2(poll=poll)
		l2.save()
		dl2 = dlikes2(poll=poll)
		dl2.save()
		w = Watch(poll=poll)
		w.save()
		return redirect(f'/neke/{poll.id}')
	return render(request,'poll/rforms.html')

def neke(request,pk):
    q = Questions.objects.filter(id=pk).first()
    apps = Apppolls.objects.filter(question=q).first()
    path = requests.get(f'https://meme-api.herokuapp.com/gimme')
    t = json.loads(path.text)
    if apps.image1!=t['url']:

	    apps.image2 = t['url']
	    apps.channel2 = t['postLink']
	    if t['url']=="lol":
	        messages.info(request,'sorry,something went wrong!')
	        messages.success(request,'try again')
	        q.delete()
	        apps.delete()
	        return redirect('/memes/')

	    apps.save()
	    return redirect(f'/votes/{q.id}')
    q.delete()
    messages.info(request,'something went wrong')
    return redirect('/memes/')

def cate(request,string):
	questions = Questions.objects.filter(typee=string).order_by('-date_posted')
	tags = Tags.objects.all()
	context = {'questions':questions,'tags':tags,'len':len(questions),'thing':string}
	return render(request,'poll/mik.html',context)
@login_required
def mypost(request):
	if request.method=="POST":
		data = request.POST['question']
		url1 = request.POST['urlo']
		url2= request.POST['urlt']

		if url1==url2:
			messages.warning(request,f'things cannot be same!')
			return redirect('/ycreate/')
		if not 'https' in url1 or not 'https' in url2:
			messages.warning(request,f'invalid url')
			return redirect('/ycreate')
		url1 = ''.join([url1[i] for i in range(len(url1)-1,len(url1)-12,-1)])
		url1 = ''.join([url1[i] for i in range(len(url1)-1,-1,-1)])
		url2=''.join([url2[i] for i in range(len(url2)-1,len(url2)-12,-1)])
		url2 = ''.join([url2[i] for i in range(len(url2)-1,-1,-1)])

		try:
			path = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={url1}&key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			path1 = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={url2}&key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			t = json.loads(path.text)
			t1 = json.loads(path1.text)
			
			image_url1 =t['items'][0]['snippet']['thumbnails']['standard']['url']
			image_url2 =t1['items'][0]['snippet']['thumbnails']['standard']['url']
			username1 = t['items'][0]['snippet']['title']
			username2 = t1['items'][0]['snippet']['title']
			path = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={url1}&key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			path1 = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={url2}&key=AIzaSyCr1xw-9xA_vrY4v0xZriasXnZRD8DNyvs')
			t = json.loads(path.text)
			t1 = json.loads(path1.text)
			cid1 = request.POST['urlo']
			cid2 = request.POST['urlt']

			view_count1 = t['items'][0]['statistics']['viewCount']
			view_count2 = t1['items'][0]['statistics']['viewCount']
			like_count1 = t['items'][0]['statistics']['likeCount']
			like_count2 = t1['items'][0]['statistics']['likeCount']
			commet_count1 = t['items'][0]['statistics']['commentCount']
			commet_count2 = t1['items'][0]['statistics']['commentCount']

			 

			q = Questions(poller=request.user,typee='mpost',question=data)
			q.save()
			l1 = likes1(poll=q)
			l1.save()
			dl1 = dlikes1(poll=q)
			dl1.save()
			l2 = likes2(poll=q)
			l2.save()
			dl2 = dlikes2(poll=q)
			dl2.save()
			watch = Watch(poll=q)
			watch.save()



			p = Apppolls(question=q,image1=image_url1,image2=image_url2,
			plink1=cid1,plink2=cid2,views1=view_count1,views2=view_count2,
			channel1=username1,channel2=username2,likes1=like_count1,likes2=like_count2,subs1=commet_count1,subs2=commet_count2)
			p.save()


			messages.info(request,f'saved')
			return redirect(f'/votes/{q.id}')
		except Exception as e:
			messages.info(request,'something went wrong !try again')
			return redirect('/mycreate/')
	return render(request,'poll/kforms.html')

def suggest(request):
    users = [i for i in User.objects.all().order_by('-date_joined') if i not in request.user.profile.following.all()]
    return render(request,'poll/suggestions.html',{'users':users})

def repost(request,pk):
    if request.method=="POST":
        q=  Questions.objects.filter(id=pk).first()
        title = request.POST['content']
        post = Questions(poller=request.user,question=title,image1=q.image1.name,image2=q.image2.name,kick=pk)
        post.save()
        l1 = likes1(poll=post)
        l1.save()
        dl1 = dlikes1(poll=post)
        dl1.save()
        l2 = likes2(poll=post)
        l2.save()
        dl2 = dlikes2(poll=post)
        watch = Watch(poll=post)
        watch.save()
        dl2.save()
        tag = Tags(poll=post)
        tag.save()
        tag.users.add(q.poller)
        tag.save()
        messages.info(request,'Reposted')
        return redirect(f'/votes/{post.id}')

    q=  Questions.objects.filter(id=pk).first()
    if q is not None and q.typee!="reddit" and q.typee!="mpost" and q.typee!="y" and q.poller.profile.clone ==  0:
        return render(request,'poll/repost.html',{'question':q})
    messages.info(request,'not allowd to repost')
    return redirect('/create/')

def showreposts(request,pk):
    q = Questions.objects.filter(id=pk).first()
    if q is not None:
        return redirect(f'/votes/{pk}')
    return HttpResponse('post does not exist')
    
def pcollabs(request):
	q = Questions.objects.exclude(typee="reddit")
	q = [i for i in q if 'mpost' not in i.typee or 'y' not in i.typee]
	m = []
	for i in q:
		for j in request.user.profile.following.all():
			if i.poller.id == j.id and i.kick !=0:
				m.append(i)

	return render(request,'poll/poll-collab.html',{'questions':m,'tags':Tags.objects.all()})
@login_required
def letsdo(request,pk):
	q = Questions.objects.filter(id=pk).first()
	if q is not None:
		l1 = likes1.objects.filter(poll=q).first()
		if l1:
			if request.user not in l1.users.all():
				l1.users.add(request.user)
				l1.save()
				return HttpResponse('likes added')
			else:
				l1.users.remove(request.user)
				l1.save()
				return HttpResponse('likes remove')
	return HttpResponse('post does not exist')
