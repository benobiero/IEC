from django.shortcuts import render
import json
# Create your views here.
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Iec
from .forms import PositionForm

from django.db.models import Sum,Q

import pandas as pd

class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')




class IecList(LoginRequiredMixin, ListView):
    model = Iec
    template_name='request/home.html'
    context_object_name = 'iec_list'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        if self.request.user=='admin':
            print('m')
            context['iec_list'] = context['iec_list'].filter(issued=True)
            context['count'] = context['iec_list'].filter(issued=False).count()
            
        if  self.request.user !='admin':
            context['iec_list'] = context['iec_list'].filter(user=self.request.user)
            context['count'] = context['iec_list'].filter(issued=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['iec_list'] = context['iec_list'].filter(
                title__name__contains=search_input)

        context['search_input'] = search_input

        return context


class IecDetail(LoginRequiredMixin, DetailView):
    model = Iec
    context_object_name = 'iec_detail'
    template_name = 'request/iec_detail.html'


class IecRequest(LoginRequiredMixin, CreateView):
    model = Iec
    template_name='request/request.html'
    fields = ['title', 'thematic','description', 'copies']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(IecRequest, self).form_valid(form)


class IecUpdate(LoginRequiredMixin, UpdateView):
    template_name='request/request.html'
    model = Iec
    fields = ['title','thematic', 'description', 'copies']
    success_url = reverse_lazy('home')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Iec
    template_name='request/iec_delete.html'
    context_object_name = 'iec_delete'
    success_url = reverse_lazy('home')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('home'))
def negate(col):
    if col==False:
        col=1
    else:
        col=-1
    return col
def issued(col):
    if col<0:
        col=-(col)
    else:
        col=0
    return col
def main(request):
    global srhr_table
    srhr=Iec.objects.filter( thematic='SRHR')
    srhr_df=pd.DataFrame(srhr.values('title__name','copies','issued','description','user','created'))
    srhr_df['negation']=srhr_df['issued'].apply(negate)
    srhr_df['new_copies']=srhr_df['copies']*srhr_df['negation']
    srhr_df['balance']=srhr_df['new_copies']

    srhr_df['issued']=srhr_df['balance'].apply(issued)
    srhr_df=srhr_df[['title__name','balance','issued']]
    srhr_df=srhr_df.groupby('title__name').sum().reset_index()
    srhr_df['copies_in']=srhr_df['balance'] + srhr_df['issued']

    

    json_srhr=srhr_df.to_json(orient='records')
    srhr_table=[]
    srhr_table=json.loads(json_srhr)
    return render(request,'main.html', {'srhr':srhr,'json_table':srhr_table})

def all_books(request):
    all_books=Iec.objects.all()
    return render(request,'books.html', {'all':all_books})

def hg(request):
    global json_table
    srhr=Iec.objects.filter( thematic='H&G')
    srhr_df=pd.DataFrame(srhr.values('title__name','copies','issued','description','user','created'))
    srhr_df['negation']=srhr_df['issued'].apply(negate)
    srhr_df['new_copies']=srhr_df['copies']*srhr_df['negation']
    srhr_df['balance']=srhr_df['new_copies']

    srhr_df['issued']=srhr_df['balance'].apply(issued)
    srhr_df=srhr_df[['title__name','balance','issued']]
    srhr_df=srhr_df.groupby('title__name').sum().reset_index()
    srhr_df['copies_in']=srhr_df['balance'] + srhr_df['issued']

    

    json_srhr=srhr_df.to_json(orient='records')
    json_table=[]
    json_table=json.loads(json_srhr)
    return render(request,'thematic/hg.html', {'hg':srhr,'json_hg':json_table})

def wlpr(request):
    global wlpr_table
    srhr=Iec.objects.filter( thematic='WLPR')
    srhr_df=pd.DataFrame(srhr.values('title__name','copies','issued','description','user','created'))
    srhr_df['negation']=srhr_df['issued'].apply(negate)
    srhr_df['new_copies']=srhr_df['copies']*srhr_df['negation']
    srhr_df['balance']=srhr_df['new_copies']

    srhr_df['issued']=srhr_df['balance'].apply(issued)
    srhr_df=srhr_df[['title__name','balance','issued']]
    srhr_df=srhr_df.groupby('title__name').sum().reset_index()
    srhr_df['copies_in']=srhr_df['balance'] + srhr_df['issued']

    

    json_srhr=srhr_df.to_json(orient='records')
    wlpr_table=[]
    wlpr_table=json.loads(json_srhr)
    return render(request,'thematic/wlpr.html', {'hg':srhr,'json_wlpr':wlpr_table})
def hiv_tb(request):
    global hiv_table
    srhr=Iec.objects.filter( thematic='HIV/TB')
    srhr_df=pd.DataFrame(srhr.values('title__name','copies','issued','description','user','created'))
    srhr_df['negation']=srhr_df['issued'].apply(negate)
    srhr_df['new_copies']=srhr_df['copies']*srhr_df['negation']
    srhr_df['balance']=srhr_df['new_copies']

    srhr_df['issued']=srhr_df['balance'].apply(issued)
    srhr_df=srhr_df[['title__name','balance','issued']]
    srhr_df=srhr_df.groupby('title__name').sum().reset_index()
    srhr_df['copies_in']=srhr_df['balance'] + srhr_df['issued']

    

    json_srhr=srhr_df.to_json(orient='records')
    hiv_table=[]
    hiv_table=json.loads(json_srhr)
    return render(request,'thematic/hiv_tb.html', {'hg':srhr,'json_hiv':hiv_table})
def silu(request):
    global silu_table
    srhr=Iec.objects.filter( thematic='SILU')
    srhr_df=pd.DataFrame(srhr.values('title__name','copies','issued','description','user','created'))
    srhr_df['negation']=srhr_df['issued'].apply(negate)
    srhr_df['new_copies']=srhr_df['copies']*srhr_df['negation']
    srhr_df['balance']=srhr_df['new_copies']

    srhr_df['issued']=srhr_df['balance'].apply(issued)
    srhr_df=srhr_df[['title__name','balance','issued']]
    srhr_df=srhr_df.groupby('title__name').sum().reset_index()
    srhr_df['copies_in']=srhr_df['balance'] + srhr_df['issued']

    

    json_srhr=srhr_df.to_json(orient='records')
    silu_table=[]
    silu_table=json.loads(json_srhr)
    return render(request,'thematic/silu.html', {'hg':srhr,'json_silu':silu_table})

def print_iec(request):
    hg(request)
    global json_table
    return render(request,'thematic/download_hg.html', {'json_hg':json_table})
def download_wlpr(request):
    wlpr(request)
    global wlpr_table
    return render(request,'thematic/download_wlpr.html', {'json_hg':wlpr_table})
def download_hiv(request):
    hiv_tb(request)
    global hiv_table
    return render(request,'thematic/download_hiv.html', {'json_hg':hiv_table})
def download_srhr(request):
    main(request)
    global srhr_table
    return render(request,'thematic/download_srhr.html', {'json_hg':srhr_table})
def download_silu(request):
    silu(request)
    global silu_table
    return render(request,'thematic/download_silu.html', {'json_hg':silu_table})


from django.http import HttpResponse
from django.views.generic import View
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import Iec

class IecListDownloadView(View):
    def get(self, request):
        iec_list = Iec.objects.all()

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="request.pdf"'

        # Create a PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()

        # Create a table with the data
        data = []
        table_style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), '#e53935'),
    ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, -1), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, '#e53935'),
    
])

        table_header = ['Title','Copies','Description']
        data.append(table_header)
        for iec in iec_list:
            data.append([iec.title.name, iec.copies,''])

        # Add the table to the PDF document
        table = Table(data)
        table.setStyle(table_style)
        doc.build([Paragraph("Request List", styles['Heading1']), table])

        return response



