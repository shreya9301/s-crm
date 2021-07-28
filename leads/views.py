from django import contrib
import django
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorandLoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Lead,Category
#from django.contrib.auth.forms import UserCreationForm
from .forms import (
    LeadForm,
    LeadModelForm,
    CustomUserCreationForm,
    AssignAgentForm,
    LeadCategoryUpdateForm,
    CategoryModelForm
)


class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


""" def signup(request):
    if request.user.is_authenticated:
        return redirect("/leads")
    else:
        form = CustomerCreateUserForm()
        if request.method=="POST":
            form = CustomerCreateUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data.get('username')
                messages.success(request,'Account created for ' + user)
                return redirect("login")

    context ={
        "form" : form
    }
    return render(request,"registration/signup.html",context) """


def home_page(request):
    return render(request,"landing_page.html")

""" @login_required(login_url="/login")
def lead_list(request):
    leads = Lead.objects.all()
    context={
        "leads" : leads
    }
    return render(request,"lead_list.html",context) """

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "lead_list.html"
    #queryset = Lead.objects.all()
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organization=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):  #overriding the get_context_data method to filter the queryset for unassigned_leads
        context = super(LeadListView,self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile,
            agent__isnull=True #this filter is to check if the foreign key field is NULL 
            )
        context.update(
            {
                "unassigned_leads": queryset
            }
        )
        return context



@login_required(login_url="/login")
def lead_detail(request , pk):
    lead = Lead.objects.get(id = pk)
    context={
        "lead":lead
    }
    return render(request,"lead_detail.html",context)


class LeadCreateView(OrganisorandLoginRequiredMixin,generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self ,form):
        lead = form.save(commit = False) 
        lead.organization = self.request.user.userprofile
        lead.save()
        return super(LeadCreateView,self).form_valid(form)

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form) 

""" @login_required(login_url="/login")
def lead_create(request):
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():    
            form.save()
            send_mail(
                "Lead created",
                'Just go to the site to check the list of leads',
                'test@gmail.com',
                ['test2@gmail.com'],    
            )  
            return redirect("/leads")
    context={
        "form" : LeadModelForm()
    }
    return render(request,"lead_create.html",context)
 """


class LeadUpdateView(OrganisorandLoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)

""" @login_required(login_url="/login")
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "lead_update.html", context) """


""" @login_required(login_url="/login")
def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads") """

class LeadDeleteView(OrganisorandLoginRequiredMixin ,generic.DeleteView):
    template_name = "lead_delete.html"
    context_object_name = "lead"

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk" : self.get_object().id})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            return Lead.objects.filter(organization=user.userprofile)


class AssignAgentView(OrganisorandLoginRequiredMixin,generic.FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs): #function to pass extra arguments in the form
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request" : self.request
        }) 
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id = self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)


class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    #the function below is for adding an extra row in the template table for the uncategorized leads
    def get_context_data(self,**kwargs):
        context = super(CategoryListView,self).get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
        
        context.update({
            "unassigned_lead_count" : queryset.filter(category__isnull = True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset
    """ def get_context_data(self,**kwargs):

        context = super(CategoryDetailView,self).get_context_data(**kwargs)
        #qs = Lead.objects.filter(category = self.get_object())
        leads = self.get_object().leads.all() #to do this we have to add the realted name field in the Lead table for the foreign key field
        #the above query do the reverse lookup to find the leads associated with the current category
        context.update({
            "leads" : leads
        })
        return context """


class CategoryCreateView(OrganisorandLoginRequiredMixin, generic.CreateView):
    template_name = "category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("leads:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadUpdateView, self).form_valid(form)


class CategoryDeleteView(OrganisorandLoginRequiredMixin, generic.DeleteView):
    template_name = "category_delete.html"

    def get_success_url(self):
        return reverse("leads:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organization=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization
            )
        return queryset
class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(organization = user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user = user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail",kwargs={"pk" : self.get_object().id})

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this lead")
        return super(LeadCategoryUpdateView, self).form_valid(form)