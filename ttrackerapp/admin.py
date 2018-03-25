from django.contrib import admin
from django.core.exceptions import PermissionDenied 
from .models import IssueCategory, IssueStatus, IssueIssue
from datetime import datetime

class IssueCategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)
    view_on_site = False
    list_display = ('name', 'default')

class IssueStatusAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)
    view_on_site = False
    list_display = ('name', 'default')

class IssueIssueAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':
                    [('reporter', 'owner'),
                     ('status', 'category'),
                     ('created', 'is_solved')
                     ]
                }
         ),
        (None, {'fields': ['description']})
        ]
    list_display = ('description', 'reporter', 'owner', 'status', 'category', 'created', 'solved', 'is_solved')
    save_on_top = True
    view_on_site = False

    class Media:
        css = {
             'all': ('admin/css/issue_stats.css',)
        }

    def get_average_issue(self):
        """
        Get average issue resolution time
        """
        return self.question_if_none(IssueIssue.get_average_resolution())
    
    def get_shoretest_issue(self):
        """
        Get shortest issue resolution time
        """
        return self.question_if_none(IssueIssue.get_shortest_resolution())

    def get_longest_issue(self):
        """
        Get longest issue resolution time
        """
        return self.question_if_none(IssueIssue.get_longest_resolution())

    def question_if_none(self, result):
        """
        Return question mark if result is None
        
        @param result: timedelta
        """
        return self.format_timedelta(result) if result is not None else "-"

    def format_timedelta(self, tdelta):
        """
        Format timedelta to suitable string
        
        @param tdelta: timedelta to format
        """
        s = tdelta.total_seconds()
        days, remainder = divmod(s, 3600*24)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return ('{:d} days, {:0=2d}:{:0=2d}:{:0=2d}'.format(int(days), int(hours), int(minutes), int(seconds)))

    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        extra_context['issue_average'] = self.get_average_issue()
        extra_context['issue_longest'] = self.get_longest_issue()
        extra_context['issue_shortest'] = self.get_shoretest_issue()
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if request.method == 'POST':
            if 'is_solved' in request.POST.keys() and request.POST['is_solved'] == 'on':
                obj.solved = datetime.now()
            else:
                obj.solved = None
        super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)

        if not self._has_change_only_permission(request, obj):
            raise PermissionDenied

        return obj

admin.site.site_title = 'Test Tracker administration'
admin.site.site_header = 'Test Tracker administration'
admin.site.index_title = 'Test Tracker administration'
admin.site.register(IssueCategory, IssueCategoryAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(IssueIssue, IssueIssueAdmin)
