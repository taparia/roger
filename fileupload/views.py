# encoding: utf-8
import json
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture, Document
from .forms import DocumentForm 
from .response import JSONResponse, response_mimetype
from .serialize import serialize
import nagios_summary
import nagios_report
import p4j

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
	    b = p4j.split()
	    print "Value of b is", b

#	    c = p4j.sentiment()
#	    print "Value of c is", c
	    # Redirect to the document list after POST
            return HttpResponseRedirect('')
    
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
#    command = nagios_summary.pretty_print_status()
    a = nagios_summary.pretty_print_status()
    host = a[0]
    state = a[1]
    command  = zip(host, state)
    print documents
    # Render list page with the documents and the form
    return render_to_response(
        'fileupload/picture_basic_form.html',
        {'documents': documents, 'form': form, 'command' : command},
        context_instance=RequestContext(request)
	    )

def result(request):
    # Handle result 
   d = nagios_report.process_info()
   print "Oh no"
   c = p4j.sentiment()
   print "Value of c is", c
   e = p4j.merge()
   print "Value of e is", e
   
   return render_to_response(
      'fileupload/sentiment_output.html',
        context_instance=RequestContext(request)
	    )

class PictureCreateView(CreateView):
    model = Picture

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicVersionCreateView(PictureCreateView):
    template_name_suffix = '_basic_form'


class BasicPlusVersionCreateView(PictureCreateView):
    template_name_suffix = '_basicplus_form'


class AngularVersionCreateView(PictureCreateView):
    template_name_suffix = '_angular_form'


class jQueryVersionCreateView(PictureCreateView):
    template_name_suffix = '_jquery_form'


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


