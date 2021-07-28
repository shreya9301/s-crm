import random
from django.views import generic
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganisorandLoginRequiredMixin

class AgentListView(OrganisorandLoginRequiredMixin,generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        return Agent.objects.all()

class AgentCreateView(OrganisorandLoginRequiredMixin,generic.CreateView):
    template_name = "agents/agent-create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self ,form):
        user = form.save(commit = False) #we are not saving the form detials directly to the database but we can access its details in this instance 
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user = user,
            organization = self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an Agent",
            message="You are now appointed as an Agent on our website DJCRM !",
            from_email="admin12@gmail.com",
            recipient_list = [user.email]
        )
        #agent.organization = self.request.user.userprofile
        #agent.save()
        return super(AgentCreateView,self).form_valid(form)


class AgentDetailView(OrganisorandLoginRequiredMixin , generic.DetailView):
    template_name = "agents/agent-detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        return Agent.objects.all()


class AgentUpdateView(OrganisorandLoginRequiredMixin , generic.UpdateView):
    template_name = "agents/agent-update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(LoginRequiredMixin ,generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        return Agent.objects.all()
