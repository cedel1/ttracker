from django.contrib import admin
from .models import IssueCategory, IssueStatus, IssueIssue

class IssueCategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)
    view_on_site = False

class IssueStatusAdmin(admin.ModelAdmin):
    fields = (('name', 'default'),)
    view_on_site = False

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
        """
        return result if result is not None else "?"

    def changelist_view(self, request, extra_context = None):
        extra_context = extra_context or {}
        extra_context['issue_average'] = self.get_average_issue()
        extra_context['issue_longest'] = self.get_longest_issue()
        extra_context['issue_shortest'] = self.get_shoretest_issue()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(IssueCategory, IssueCategoryAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(IssueIssue, IssueIssueAdmin)
