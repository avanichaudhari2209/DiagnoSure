# Create your models here.
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FamilyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_members')
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.relation})"


class Symptom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.CharField(max_length=100)
    severity = models.IntegerField()

    def __str__(self):
        return self.symptom


class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    category = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)

    symptoms = models.JSONField()
    precautions = models.JSONField()
    risk_factors = models.JSONField(blank=True)
    diet = models.TextField(blank=True, null=True)

    contagious = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # disease = models.CharField(max_length=100)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    risk = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease.name


class ChatbotMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=10)  # user or bot
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]

class MedicalHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_histories')
    patient_name = models.CharField(max_length=100)
    diseases_predicted = models.CharField(max_length=255)
    symptom_severity = models.CharField(max_length=50, choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')])
    recommended_diet = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.diseases_predicted} on {self.date.date()}"