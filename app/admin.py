from django.contrib import admin
from . import models
# Register your models here.=

class TimeField(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )

admin.site.register(models.User)
admin.site.register(models.Course, TimeField)
admin.site.register(models.Content, TimeField)


admin.site.register(models.Lessons, TimeField)

# admin.site.register(models.Lessons)
admin.site.register(models.CourseMember)
admin.site.register(models.CourseRequest, TimeField)


admin.site.register(models.CourseMenuGroup, TimeField) 
admin.site.register(models.UserDevice)
admin.site.register(models.Notification)