from django.urls import path
from . import views


urlpatterns = [
    path("job/details/<int:pk>/", views.JobDetailsView.as_view(), name="job_details"),
    path("apply-job/<int:job_id>/", views.ApplyJobView.as_view(), name="apply_job"),
    path("my_job/", views.MyJobView.as_view(), name="my_jobs"),
    path("", views.HomePageView.as_view(), name="home_page")
]
