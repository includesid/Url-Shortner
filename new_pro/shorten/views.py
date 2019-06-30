from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
#to use the dynamic url
from django.urls import reverse
from .models import bitly
from .forms import bitlyForm, editBitly
#to authenticatethe user 
from  django.contrib.auth.decorators import login_required

def index(request):
    objects = bitly.objects.all()[::-1]
    print(objects)

    context = {'objs': objects}
    return render(request, "index.html", context)

def create(request):
    from .utils import create_shortcode
    form = bitlyForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.shortcode = create_shortcode()
        instance.datewise = ""
        instance.save()

        return HttpResponseRedirect(reverse(index))

    context = {"urlform": form}
    return render(request, "create.html", context)

def goto(request, shortcode=None):
    import json
    qs = get_object_or_404(bitly, shortcode__iexact=shortcode)
    if qs:
       instance=json.loads(qs.datewise)
       crt_date=current_date()
       if crt_date in instance:
        instance[crt_date]+=1
       else:
        instance[crt_date]=1
       qs.datewise=json.dumps(instance)
       qs.save()
    return HttpResponseRedirect(qs.long_url)

def update(request, pk=None):
  if request.user.is_authenticate:
    qs =  get_object_or_404(bitly, id=pk)
    form = editBitly(request.POST or None, instance=qs)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('index'))

    context = {'urlform': form}
    return render(request, "create.html", context)
  return HttpResponseRedirect(reverse('index'))
#we can use @login_required()
def delete(request,pk=None):
  if request.user.is_authenticate(): 
   qs=get_object_or_404(bitly,id=pk)
   qs.delete()
  return HttpResponseRedirect(reverse('index'))