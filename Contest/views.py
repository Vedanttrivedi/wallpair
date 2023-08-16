from django.shortcuts import render,redirect
from django.http import Http404,HttpResponse
from . models import Contest
from datetime import datetime
from django.utils import timezone
from poll.models import Questions,Comments,Reviews,Apppolls,Tags,likes1,dlikes1,likes2,dlikes2,Watch,Collab
from django.contrib.auth.models import User
from django.contrib import  messages
# Create your views here.
def create(request):
    if request.method=="POST":
        name = request.POST['name']
        images1 = request.FILES['img1']
        images2 = request.FILES['img2']
        images3 = request.FILES['img3']
        images4 = request.FILES['img4']
        images5 = request.FILES['img5']
        contest = Contest(name=name,author=request.user)
        contest.save()
        post = Questions(poller=request.user,question="First Round",image1=images1,image2=images2,iscontest=1)
        post.save()
        l1 = likes1(poll=post)
        l1.save()
        l2 = likes2(poll=post)
        l2.save()
        contest.posts.add(post)
        post = Questions(poller=request.user,question="Second Round",image1=images3,image2=images4,iscontest=1)
        post.save()
        l1 = likes1(poll=post)
        l1.save()
        l2 = likes2(poll=post)
        l2.save()
        contest.posts.add(post)
        post = Questions(poller=request.user,question="Final Round",image1=images5,iscontest=1)
        post.save()
        l1 = likes1(poll=post)
        l1.save()
        l2 = likes2(poll=post)
        l2.save()
        contest.posts.add(post)
        contest.save()
        return redirect('/con/')
        
    return render(request,'Contest/create.html')

def allcontest(request):
    con = Contest.objects.all()
    time = datetime
    return render(request,'Contest/allcontest.html',{'contests':con,'time':time})
def onecontest(request,pk):
    contest = Contest.objects.filter(id=pk).first()
    reg_time = timezone.now().time().minute
    posts = []
    postid = []
    ps = []
    i =0
    notification = ""
    canjoin = True
    if contest:
        if (reg_time - contest.date.time().minute > 15 and reg_time - contest.date.time().minute < 30):
            canjoin = False
            notification ="Second Go Starts Minutes "+ str(30 - (reg_time - contest.date.time().minute))
            for k in contest.posts.all():
                if(i==2):
                    break
                name = k.question
                posts.append(name)
                i+=1
            
        if(reg_time - contest.date.time().minute >= 30 and reg_time - contest.date.time().minute < 45):
            canjoin = False
            notification = notification ="Final Go Starts Minutes "+ str(45 - (reg_time - contest.date.time().minute))
            if contest.second == True:
                i = 0
                for k in contest.posts.all():
                    if i==3:
                        posts.append(k.question)
                        break
                    i = i+1
            else:
                i=0
                for k in contest.posts.all():
                    if(i==2):
                        break
                    name = k.question
                    key = k.id
                    postid.append(key)
                    posts.append(name)
                    i+=1
                q1 = Questions.objects.filter(id=postid[0]).first()
                q2 = Questions.objects.filter(id=postid[1]).first()
                l1 = likes1.objects.filter(poll=q1).first()
                post1_like1_count = l1.users.all().count()
                l2 = likes2.objects.filter(poll=q1).first()
                post1_like2_count = l2.users.count()
                l3 = likes1.objects.filter(poll=q2).first()
                post2_like1_count = l3.users.count()
                l4 = likes2.objects.filter(poll=q2).first()
                post2_like2_count = l4.users.count()
                
                image1 = ""
                image2 = ""
                if(post1_like1_count >= post1_like2_count):
                    image1 = q1.image1
                else:
                    image1 = q1.image2
                if(post2_like1_count >= post2_like2_count):
                    image2 = q2.image1
                else:
                    image2 = q2.image2
                post = Questions(poller=request.user,question="SemiFinal Round",image1=image1,image2=image2,iscontest=1)
                post.save()
                l1 = likes1(poll=post)
                l1.save()
                l2 = likes2(poll=post)
                l2.save()
                contest.posts.add(post)
                contest.second=True
                contest.save()
                posts = []
                posts.append("SemiFinal Round")
        elif (reg_time - contest.date.time().minute >= 45 and reg_time - contest.date.time().minute < 60):
            canjoin = False
            notification = "Result In "+ str(60 - (reg_time - contest.date.time().minute))+" Minutes"
            if  contest.final == True:
                i = 0
                for k in contest.posts.all():
                    if i==2:
                        posts = []
                        posts.append(k.question)
                        break
                    i = i+1
            else:
                i = 0
                posts = []
                postid = []
                final_post = ""
                for k in contest.posts.all():
                    if i==3:
                        posts.append(k.question)
                        postid.append(k.id)
                    if i==2:
                        final_post = k
                    i = i+1
                q3 = Questions.objects.filter(id=postid[0]).first()
                l1 = likes1.objects.filter(poll=q3).first()
                l1_count = l1.users.count()
                l2 = likes2.objects.filter(poll=q3).first()
                l2_count = l2.users.count()
                if l1_count >= l2_count:
                    final_post.image2 = q3.image1
                    
                else:
                    final_post.image2 = q3.image2
                final_post.save()
                contest.final = True
                contest.save()
        
        if notification == " ":
            notification = "First Go Starts Minutes "+ str(15 - (reg_time - contest.date.time().minute))
        return render(request,'Contest/onecontest.html',{'contest':contest,'time':reg_time - contest.date.time().minute,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':len(posts),'notification':notification,'canjoin':canjoin})
    return redirect('/con/all/')
    
def joincontest(request,pk):
    contest = Contest.objects.filter(id=pk).first()
    reg_time = timezone.now().time().hour
    if contest:
        if reg_time - contest.date.time().hour <= 3:
            if request.user in contest.members.all():
                contest.members.remove(request.user)
                contest.save()
                return redirect(f"https://wallpair.com/con/all/")
            else:
                contest.members.add(request.user)
                contest.save()
                return redirect(f"https://wallpair.com/con/all/")
        return HttpResponse("you cannot join or left because contest is started")
        return redirect(f"https://wallpair.com/con/contest/{contest.id}")
    return redirect('https://wallpair.com/con/all/')
    
def members(request,pk):
    contest = Contest.objects.filter(id=pk).first()
    users = User.objects.all()
    if contest:
        user = [i.username for i in contest.members.all()]
        return render(request,'Contest/members.html',{'contest':contest,"users":users,"user":user})
    return HttpResponse("Contest Does Not Exist")


def removeFromContest(request,conpk,pk):
    user = User.objects.filter(id=pk).first()
    contest = Contest.objects.filter(id=conpk).first()
    if user is not None and contest is not None and request.user.username == contest.author.username:
        contest.members.remove(user)
        contest.save()
        return redirect(f"https://wallpair.com/con/members/{contest.id}")
    return HttpResponse("UnAuthorized")
    return HttpResponse("Not Valid Option")

#one contest will be of 1 day
#registration will be open for first 3 hours
#all the go will be of 7 hours
def newcontest(request,pk):
    #return HttpResponse("landed")
    contest = Contest.objects.filter(id=pk).first()
    #if the day is same
    #if day is not same but 24 hours are not over
    #if day is not same and 24 hours are over
    if timezone.now().date().day - contest.date.date().day  == 0:
        #if the day is same and contest is going on
        if contest.over == True:
            #contest is over
            return HttpResponse("contest is  over")
        else:
            if timezone.now().time().hour - contest.date.time().hour < 3:
                messages.info(request,f'contest is not started yet will start in some time  {timezone.now()} {contest.date}')
                posts = []
                return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().minute - contest.date.time().minute,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':len(posts),'notification':"cool",'canjoin':True})
            elif timezone.now().time().hour - contest.date.time().hour >= 3 and timezone.now().time().hour - contest.date.time().hour < 9:
                if contest.canjoin:
                    contest.canjoin=False
                    contest.save()
                i = 0
                posts= []
                for k in contest.posts.all():
                    if i==2:
                        break
                    name = k.question
                    posts.append(name)
                    i = i+1
                messages.info(request,f"{posts} {timezone.now().time().hour - contest.date.time().hour}")
                #posts = []
                return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().hour - contest.date.time().hour,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':len(posts),'notification':"cool",'canjoin':True})
                
                
            elif timezone.now().time().hour - contest.date.time().hour >= 9 and timezone.now().time().hour - contest.date.time().hour <16:
                i = 0
                posts = []
                
                if contest.second==True:
                    for k in contest.posts.all():
                        if i==3:
                            name = k.question
                            posts.append(name)
                            break
                        i = i+1
                    messages.info(request,f'{posts} cool')
                    noti =" third round starts in " +str(16 - (timezone.now().time().hour - contest.date.time().hour))+" hours " 
                    return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().hour - contest.date.time().hour,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':len(posts),'notification':noti,'canjoin':True})
                else:
                    i=0
                    postid = []
                    for k in contest.posts.all():
                        if(i==2):
                            break
                        name = k.question
                        key = k.id
                        postid.append(key)
                        posts.append(name)
                        i+=1
                    q1 = Questions.objects.filter(id=postid[0]).first()
                    q2 = Questions.objects.filter(id=postid[1]).first()
                    l1 = likes1.objects.filter(poll=q1).first()
                    post1_like1_count = l1.users.all().count()
                    l2 = likes2.objects.filter(poll=q1).first()
                    post1_like2_count = l2.users.count()
                    l3 = likes1.objects.filter(poll=q2).first()
                    post2_like1_count = l3.users.count()
                    l4 = likes2.objects.filter(poll=q2).first()
                    post2_like2_count = l4.users.count()
                
                    image1 = ""
                    image2 = ""
                    if(post1_like1_count >= post1_like2_count):
                        image1 = q1.image1
                    else:
                        image1 = q1.image2
                    if(post2_like1_count >= post2_like2_count):
                        image2 = q2.image1
                    else:
                        image2 = q2.image2
                    post = Questions(poller=request.user,question="SemiFinal Round",image1=image1,image2=image2,iscontest=1)
                    post.save()
                    l1 = likes1(poll=post)
                    l1.save()
                    l2 = likes2(poll=post)
                    l2.save()
                    contest.posts.add(post)
                    contest.second=True
                    contest.save()
                    posts = []
                    posts.append("SemiFinal Round")
                    messages.info(request,f'{posts} {timezone.now().time().hour - contest.date.time().hour}')
                    noti =" third round starts in " +str(16 - (timezone.now().time().hour - contest.date.time().hour))+" hours "
                    return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().hour - contest.date.time().hour,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':len(posts),'notification':noti,'canjoin':True}) 
                    
            elif timezone.now().time().hour - contest.date.time().hour > 16 and timezone.now().time().hour - contest.date.time().hour <=24:
                if  contest.final == True:
                    i = 0
                    for k in contest.posts.all():
                        if i==2:
                            posts = []
                            posts.append(k.question)
                            break
                        i = i+1
                else:
                    i = 0
                    posts = []
                    postid = []
                    final_post = ""
                    for k in contest.posts.all():
                        if i==3:
                            posts.append(k.question)
                            postid.append(k.id)
                        if i==2:
                            final_post = k
                        i = i+1
                    q3 = Questions.objects.filter(id=postid[0]).first()
                    l1 = likes1.objects.filter(poll=q3).first()
                    l1_count = l1.users.count()
                    l2 = likes2.objects.filter(poll=q3).first()
                    l2_count = l2.users.count()
                    if l1_count >= l2_count:
                        final_post.image2 = q3.image1
                    
                    else:
                        final_post.image2 = q3.image2
                    final_post.save()
                    contest.final = True
                    contest.save()
                    messages.info(request,f"{posts} {timezone.now().time().hour - contest.date.time().hour} hello")
                    return redirect(f"https://wallpair.com/con/all")
                    
                    
                
    elif timezone.now().date().day - contest.date.date().day !=0:
        #if the day is not same and contest is going on
        if contest.canjoin:
            if not abs(timezone.now().time().hour - contest.date.time().hour) < 3:
                contest.canjoin=False
                contest.save()
                messages.info("press the button again")
                return redirect(f"https://wallpair.com/con/all")
            else:
                noti =" third round starts in " +str(3 - (timezone.now().time().hour - contest.date.time().hour))+" hours "
                return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().hour - contest.date.time().hour,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':[],'len':0,'notification':noti,'canjoin':True}) 
            
        elif contest.second == True and contest.final == False:
            if  contest.final == True:
                    i = 0
                    for k in contest.posts.all():
                        if i==2:
                            posts = []
                            posts.append(k.question)
                            break
                        i = i+1
            else:
                i = 0
                posts = []
                postid = []
                final_post = ""
                for k in contest.posts.all():
                    if i==3:
                        posts.append(k.question)
                        postid.append(k.id)
                    if i==2:
                        final_post = k
                    i = i+1
                q3 = Questions.objects.filter(id=postid[0]).first()
                l1 = likes1.objects.filter(poll=q3).first()
                l1_count = l1.users.count()
                l2 = likes2.objects.filter(poll=q3).first()
                l2_count = l2.users.count()
                if l1_count >= l2_count:
                    final_post.image2 = q3.image1
                
                else:
                    final_post.image2 = q3.image2
                final_post.save()
                contest.final = True
                contest.save()
                messages.info(request,f"{posts} {timezone.now().time().hour - contest.date.time().hour} hello")
                #noti =" third round starts in " +str(3 - (timezone.now().time().hour - contest.date.time().hour))+" hours "
                return render(request,'Contest/onecontest.html',{'contest':contest,'time':timezone.now().time().hour - contest.date.time().hour,'t1':timezone.now().date().day,'t2':contest.date.date().day,'posts':posts,'len':0,'notification':"hii",'canjoin':False})
                
            
        return HttpResponse(f"contest day1 {timezone.now().date().day} {contest.date.date().day}")
    else:
        #contest is over
        return HttpResponse("contest over")
    
    