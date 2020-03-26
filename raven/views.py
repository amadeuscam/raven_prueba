import json
import os

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse,QueryDict
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from .models import RavenFiles


# Create your views here.
@login_required
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        mb = uploaded_file.size / (1024 * 1024)
        if uploaded_file:
            rave = RavenFiles.objects.filter(title=uploaded_file.name).exists()
            if not rave:
                rv = RavenFiles.objects.create(
                    title=uploaded_file.name,
                    size=f"{str(mb)[:4]} mb",
                    r_file=uploaded_file
                )

                return redirect('upload')

    if request.method == 'GET':
        if request.GET.get("id"):
            id = request.GET.get("id")
            raves = RavenFiles.objects.get(id=id)
            print(f"{raves.r_file.url}")
            url = f"{raves.r_file.url}"
            print(url)
            return HttpResponse(json.dumps(url))



    rave = RavenFiles.objects.all().order_by('-created')
    return render(request, "raven/file_list.html", {"raven_obj": rave})


def remove_upload(request):

    put = json.loads(request.body.decode('utf-8'))
    if put:
        print("dentro 1")
        id = put.get("id")
        raves = RavenFiles.objects.get(id=id)
        print(raves.r_file.path)
        os.remove(f"{raves.r_file.path}")
        raves.delete()
        return HttpResponse(json.dumps(True))



class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'raven/signup.html'