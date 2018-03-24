from django.contrib import admin
from .models import IssueCategory, IssueStatus, IssueIssue

admin.site.register(IssueCategory)
admin.site.register(IssueStatus)
admin.site.register(IssueIssue)
