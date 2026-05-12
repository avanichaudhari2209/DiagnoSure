from django.contrib import admin
from .models import User, Symptom, Disease, Report, ChatbotMessage, MedicalHistory

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'gender')
    search_fields = ('name', 'email')

admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(Report)
admin.site.register(ChatbotMessage)

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'patient_name', 'diseases_predicted', 'symptom_severity', 'date')
    search_fields = ('patient_name', 'diseases_predicted', 'user__name', 'user__email')
    list_filter = ('symptom_severity', 'date')

