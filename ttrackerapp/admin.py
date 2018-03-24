from django.contrib import admin
from .models import IssueCategory, IssueStatus, IssueIssue

class IssueCategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)

class IssueStatusAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)

class IssueIssueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':
                    [('reporter', 'owner'),
                     ('status', 'category'),
                     ('created', 'is_solved', 'solved')
                     ]
                }
         ),
        (None, {'fields': ['description']})
        ] 

admin.site.register(IssueCategory, IssueCategoryAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(IssueIssue, IssueIssueAdmin)
