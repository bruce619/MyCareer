from django.contrib import admin
from .models import Job, Applicants, Certification, Notification


admin.site.register(Job)
admin.site.register(Applicants)
admin.site.register(Certification)
admin.site.register(Notification)

