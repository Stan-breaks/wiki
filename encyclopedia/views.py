from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown
from django import forms

class Newform(forms.Form):
    title=forms.CharField(label="Enter the title")
    text=forms.CharField(widget=forms.Textarea)

entries=util.list_entries()

def index(request):
    entries=util.list_entries()
    if(request.method=='GET'):
        search_results=[]
        search=request.GET.get('q', '')
        for entry in entries:
            if search.lower() in entry.lower():
                search_results.append(entry)
        if(search_results):
            return render(request,"encyclopedia/index.html", {
            "entries": search_results,
            })
        else:
            return render(request,"encyclopedia/index.html",{
                "result":1,
                "search":search
            })
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
    })

def title(request,title):
    md_entry=util.get_entry(title)
    if (md_entry==None):
        return render(request,"encyclopedia/error.html",{
            "num":0
        })
    try:
        html_entry=markdown.markdown(md_entry)
    except:
        html_entry=markdown.markdown(md_entry,output_format="html5")
    return render(request,"encyclopedia/entry.html",{
        "entry":html_entry,
        "title":title
    })

def create(request):
    if(request.method =='POST'):
        form=Newform(request.POST)
        if form.is_valid():
            mytitle=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            if(util.get_entry(mytitle)!=None):
                return render(request,"encyclopedia/error.html",{
                "num":1
                })
        util.save_entry(mytitle,text)
        return HttpResponseRedirect(reverse("title",args=(mytitle,)))
    else:
        form=Newform()
    return render(request,"encyclopedia/new.html",{
      "form":form
    })

def random_page(request):
    entry=random.choice(entries)
    return title(request,entry)

def edit(request,title):
    if(request.method=='POST'):
        form=Newform(request.POST)
        if form.is_valid():
            mytitle=form.cleaned_data["title"]
            text=form.cleaned_data["text"]
            util.save_entry(mytitle,text)
            return HttpResponseRedirect(reverse("title",args=(mytitle,)))
    else:
        text=util.get_entry(title)
        form=Newform(initial={'title':title,'text':text})
    return render(request,"encyclopedia/edit.html",{
        "form":form,
        "title":title
    })