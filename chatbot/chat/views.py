from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.

import os, sys

cwd=os.getcwd()
cwd+="/template"
sys.path.insert(0, cwd)

def chatbot_reply(input_text):
    import os
    import aiml
    
    BRAIN_FILE="brain.dump"
    
    kernel = aiml.Kernel()
    
    # To increase the startup speed of the bot it is
    # possible to save the parsed aiml files as a
    # dump. This code checks if a dump exists and
    # otherwise loads the aiml from the xml files
    # and saves the brain dump.
    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        kernel.loadBrain(BRAIN_FILE)
    else:
        print("Parsing aiml files")
        kernel.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
        print("Saving brain file: " + BRAIN_FILE)
        kernel.saveBrain(BRAIN_FILE)
    
    response = kernel.respond(input_text)
    return response


def index(request):
    return render(request, 'home.html')

def Post(request):
    if request.method == "POST":
        query = request.POST.get('msgbox', None)
        return JsonResponse({'response': chatbot_reply(query), 'query': query})
    else:
        return HttpResponse('Request must be post')
