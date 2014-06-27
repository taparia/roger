# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from sentiment.forms import UploadFileForm
from sentiment.models import Drinker
from django.contrib.auth import authenticate,login,logout
	
def DrinkerRegistration(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile/')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'],email = form.cleaned_data['email'],password = form.cleaned_data['password'])
			user.save()
			drinker = Drinker(user=user, name=form.cleaned_data['name'],birthday = form.cleaned_data['birthday'])			
			drinker.save()
			return HttpResponseRedirect('/profile/')
		else:
			return render_to_response('register.html',{'form':form},context_instance=RequestContext(request))
	else:
		'''user is not submittimg the form, show them a blank form'''
		form = RegistrationForm()
		context = {'form':form}
		return render_to_response('register.html',context,context_instance=RequestContext(request))

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})


