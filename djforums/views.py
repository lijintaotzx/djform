#coding=utf-8
from django.contrib.auth.forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from .models import *
def register(request):
        form = UserCreationForm()
        if request.method == 'GET':
                return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))
        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
						form.save()
						new_user = authenticate(username=request.POST['username'],
							password=request.POST['password1'])
						login(request, new_user)					#注册完成之后自动登录
						return redirect("/useradmin")
                return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))
				
def	index(request):
	cates = Category.objects.all()
	top12 = Topic.objects.order_by("-id")[:12]
	if request.user.is_authenticated():
		try:
			u = User.objects.get(id=request.user.id)
			a =UserProfile.objects.get(user=u)
			#a = UserProfile.objects.get(id=request.user.id)
			hottopic  = Topic.objects.all().order_by("-num_views")[:6]
			topicnum  = Topic.objects.filter(author=u).count()
			user_num  = UserProfile.objects.all().count()
			topic_num = Topic.objects.all().count()
			reply_num = Reply.objects.all().count()
			lastreply = Reply.objects.filter().order_by("-id")[0]
			d = {"cates":cates,'top12':top12,'hottopic':hottopic,'a':a,'topicnum':topicnum,'user_num':user_num,'topic_num':topic_num,'reply_num':reply_num}
			return render_to_response('index.html',d,context_instance=RequestContext(request))
		except:
			pass
			
	hottopic = Topic.objects.all().order_by("-num_views")[:6]
	'''
	t = Topic.objects.get(id=(int(id)))
	lastreply = Reply.objects.filter(topic=t).order_by('-id')[0]
	'''
	user_num  = UserProfile.objects.all().count()
	topic_num = Topic.objects.all().count()
	reply_num = Reply.objects.all().count()
	d = {"cates":cates,'top12':top12,'hottopic':hottopic,'user_num':user_num,'topic_num':topic_num,'reply_num':reply_num}
	return render_to_response('index.html',d,context_instance=RequestContext(request))
import json
def addcate(request):
	if request.method == 'POST':
		name = request.POST["name"]
		a = Category.objects.filter(name=name)
		if len(a):
			return HttpResponse(json.dumps({"code":"reply"}))
		else:
			n = Category()
			n.name = name
			n.save()
			return HttpResponse(json.dumps({"code":"ok", "id":n.id}))
			
def cateshow(request,id):
	if request.user.is_authenticated():
			#a = UserProfile.objects.get(id=request.user.id)
			u = User.objects.get(id=request.user.id)
			a =UserProfile.objects.get(user=u)
			cate = Category.objects.get(id=int(id))				#找出我们要获取的板块是哪个，放在cate里。
			topics = Topic.objects.filter(category=cate).order_by("-id")	  	#去Topic数据库中用cate去匹配字段category(主题所属板块)，如果匹配的到，那么将数据取出的放到topics中
			#a = UserProfile.objects.get(id=request.user.id)
			hottopic = Topic.objects.all().order_by("-num_views")[:6]
			topicnum = Topic.objects.all().count()
			user_num  = UserProfile.objects.all().count()
			topic_num = Topic.objects.all().count()
			reply_num = Reply.objects.all().count()
			d = {"topics": topics, "cate":cate, "hottopic":hottopic, "a":a, "topicnum":topicnum,'user_num':user_num,'topic_num':topic_num,'reply_num':reply_num}
			return render_to_response('cateshow.html', d, context_instance=RequestContext(request))
	else:
			cate = Category.objects.get(id=int(id))				#找出我们要获取的板块是哪个，放在cate里。
			topics = Topic.objects.filter(category=cate).order_by("-id")	  	#去Topic数据库中用cate去匹配字段category(主题所属板块)，如果匹配的到，那么将数据取出的放到topics中
			#a = UserProfile.objects.get(id=request.user.id)
			hottopic = Topic.objects.all().order_by("-num_views")[:6]
			user_num  = UserProfile.objects.all().count()
			topic_num = Topic.objects.all().count()
			reply_num = Reply.objects.all().count()
			d = {"topics": topics, "cate":cate, "hottopic":hottopic,'user_num':user_num,'topic_num':topic_num,'reply_num':reply_num}
			return render_to_response('cateshow.html', d, context_instance=RequestContext(request))

def addtopic(request,id):
	if request.method =="POST":
		cate = Category.objects.get(id=int(id))
		t = Topic()
		t.category = cate
		t.subject = request.POST["subject"]
		t.content = request.POST["content"]
		t.author = User.objects.get(id=request.user.id)
		t.save()
		return redirect('/cate/%s'%id)
		
def topicshow(request,id):	
	if request.user.is_authenticated():
		t = Topic.objects.get(id=int(id))
		#a = UserProfile.objects.get(id=request.user.id)
		u = User.objects.get(id=request.user.id)
		a =UserProfile.objects.get(user=u)
		t.num_views += 1
		t.save()
		print request.user.is_superuser
		reply = Reply.objects.filter(topic=t)
		d = {'t':t, 'reply':reply,'a':a}
		return render_to_response('topicshow.html', d, context_instance=RequestContext(request))
	else:
		t = Topic.objects.get(id=int(id))
		#a = UserProfile.objects.get(id=request.user.id)
		t.num_views += 1
		t.save()
		cate = Category.objects.all()	
		reply = Reply.objects.filter(topic=t)
		d = {'t':t, 'reply':reply,'cate':cate}
		return render_to_response('topicshow.html', d, context_instance=RequestContext(request))
	
def replytopic(request,id):
	if request.method =="POST":
		t = Topic.objects.get(id=int(id))
		t.num_replys += 1
		t.save()
		r = Reply()
		r.topic = t
		r.content = request.POST["content"]
		r.author = User.objects.get(id=request.user.id)
		r.save()
		return redirect('/topic/%s'%id)
		
##########################################################################################################
from .forms import *
def	userinfoadmin(request):
	if request.method=="GET":
		u = User.objects.get(id=request.user.id)
		'''
		try:
			profile = UserProfile.objects.get(user=u)
		except:
			profile = UserProfile(user=u)
			profile.save()
		'''
		profile=UserProfile.objects.get_or_create(user=u)[0]
		#profile=UserProfile.objects.get(user=u)
		print profile
		d = {'u':u,'p':profile}
		return render_to_response('userinfoadmin.html',d,context_instance=RequestContext(request))
	if request.method=="POST":
		u = User.objects.get(id=request.user.id)
		profile=UserProfile.objects.get(user=u)
		profile.nick = request.POST['nick']
		profile.email = request.POST['email']
		profile.qq = request.POST['qq']
		profile.save()
		return redirect('/useradmin')
		
def	updatephoto(request):
	u = User.objects.get(id=request.user.id)
	profile = UserProfile.objects.get(user=u)
	if request.method == 'POST':
		p = UserProfileForm(request.POST, request.FILES, instance=profile) #post文件数据 files文件内容 instance原始信息
		print p
		if p.is_valid():
			p.save()
	return redirect('/useradmin')

def defaultimg(request):
	p = Defaultimg.objects.all()
	return render_to_response('defaultimg.html',{'p':p},context_instance=RequestContext(request))

def	updateimg(request):
	if request.method == 'POST':
		p = DefaultimgForm(request.POST, request.FILES)
		if p.is_valid():
			p.save()
	return redirect('/useradmin/defaultimg')
	
def deletedefaultimg(request,id):
	n = Defaultimg.objects.get(id=int(id))
	n.delete()
	return redirect('/useradmin/defaultimg')

def mytopic(request):
	#a = UserProfile.objects.get(id=request.user.id)
	u = User.objects.get(id=request.user.id)
	a =UserProfile.objects.get(user=u)
	t = Topic.objects.filter(author=u).order_by("-id")
	hottopic = Topic.objects.all().order_by("-num_views")[:6]
	topicnum = Topic.objects.filter(author=u).count()
	return render_to_response('mytopic.html',{'a':a,'t':t,'hottopic':hottopic,'topicnum':topicnum}, context_instance=RequestContext(request))	

def edit(request,id):
	if request.method=="GET":
		n = Topic.objects.get(id=int(id))
		return render_to_response('edit.html', {'n':n}, context_instance=RequestContext(request))
	if request.method =="POST":
		#cate = Category.objects.get(id=int(id))
		t = Topic.objects.get(id=int(id))
		#t.category = cate
		t.subject = request.POST["subject"]
		t.content = request.POST["content"]
		#t.author = User.objects.get(id=request.user.id)
		t.save()
		return redirect('/mytopic')
		
			
def deletetopic(request,id):
	n = Topic.objects.get(id=int(id))
	n.delete()
	return redirect('/mytopic')
			
			
def test(request):
	return render_to_response('text.html')			
			
			
			
			
			
			
			
		

		
		

			
			
			
