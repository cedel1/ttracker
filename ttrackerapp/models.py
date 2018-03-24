# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.conf.urls.static import static


class IssueCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    default = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'issue_category'
        verbose_name = 'Issue Category'
        verbose_name_plural = 'Issue Categories'
        

    def __str__(self):
        return self.name


class IssueStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)
    default = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'issue_status'
        verbose_name = 'Issue Status'
        verbose_name_plural = 'Issue Statuses'

    def __str__(self):
        return self.name


class IssueIssue(models.Model):
    """
    Issue
    """

    @staticmethod
    def defaultcategory():
        """Provide a default category for issue"""
        #NOTE: Takes the first category set as default. If there are more of these, it takes whichever is first.
        c = IssueCategory.objects.filter(default=True)
        if len(c) > 0:
            return c[0].id

    @staticmethod
    def defaultreporter():
        """Provide default reporter, in case one isn't provided"""
        #NOTE: Takes the first reporter.
        return 1

    @staticmethod
    def defaultstatus():
        """Provide default status, in case one isn't provided"""
        #NOTE: Takes the first status set as default. If there are more of these, it takes whichever is first.
        s = IssueStatus.objects.filter(default=True)
        if len(s) > 0:
            return s[0].id


    id = models.BigAutoField(primary_key=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, db_column='reporter', related_name='reporters', default=defaultreporter)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='owner', blank=True, null=True, related_name='owners')
    description = models.TextField()
    status = models.ForeignKey('IssueStatus', models.PROTECT, db_column='status', default=defaultstatus)
    category = models.ForeignKey('IssueCategory', models.PROTECT, db_column='category', default=defaultcategory)
    created = models.DateTimeField()
    is_solved = models.BooleanField()
    solved = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'issue_issue'
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

    def __str__(self):
        return self.description

