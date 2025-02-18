from django.shortcuts import render , redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView,  View
from .models import Job , JobApplication, APPLIED


class HomePageView(ListView):
    template_name = "main/home.html"
    queryset = Job.objects.all().order_by("-created_at")
    
class JobDetailsView(DetailView):
    template_name = "main/job_details.html"
    queryset = Job.objects.all()
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        if self.request.user.is_authenticated:
            application = JobApplication.objects.filter(user = self.request.user, job = job)
            context["has_applied"] = application.exists()
        
        return context

class ApplyJobView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_verified:
            messages.error(self.request, "Please activate your account !")
            return redirect("home_page")
        try:
            if not self.request.user.userpofile.resume:
                messages.error(self.request, "Please upload your resume !")
                return redirect("home_page")
        except:
            messages.error(self.request, "Please complete your profile !")
            return redirect("home_page")
        job_id = kwargs["job_id"]
        job = Job.objects.get(id = job_id)
        JobApplication.objects.create(user = self.request.user, job = job, status = APPLIED)
        messages.success(self.request, "Job applied successfully !")
        return redirect("home_page")
    
class MyJobView(ListView):
    template_name = "main/my_jobs.html"
    def get_queryset(self):
        return JobApplication.objects.filter(user = self.request.user)
    