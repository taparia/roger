# encoding: utf-8
"""@author Priyanshu Taparia"""

from __future__ import division
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
#import p4j
import test
import datetime

h = datetime.datetime.now()

"""View for file upload/form submit page"""
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
	    print type(newdoc)
            newdoc.save()
	    b = test.split()
	    print "Value of b is", b
            documents = Document.objects.all()
	    print type(documents)
	    from  mimetypes import MimeTypes
            import urllib 
            mime = MimeTypes()
	    url = urllib.pathname2url('/home/priyanshu/git/roger/media/upload.csv')
	    mime_type = mime.guess_type(url)
	    print "Mime type is", mime_type
	    import datetime
	    global h
	    h = datetime.datetime.now()
	    print h
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

"""View for final output after analysis"""

def result(request):
    # Handle result 
   d = nagios_report.process_info()
   print "Oh no"
   k = test.tsentiment()
   print "Value of k is", k
   k = (k/6)*100
   print k
   processes1 = k
   processes2 = 100 - k
   e = test.merge()
   print "Value of e is", e
   documents = Document.objects.all()
   import datetime
   a = nagios_summary.pretty_print_status()
   host = a[0]
   state = a[1]
   command  = zip(host, state) 
   f = datetime.datetime.now()
   print "F is ", f
   print "H is", h
   g = f - h
   time = g.seconds
   return render_to_response(
      'fileupload/sentiment_output.html',{'command':command, 'time':time, 'documents': documents, 'processes1' : processes1, 'processes2' : processes2 },
        context_instance=RequestContext(request)
	    )


