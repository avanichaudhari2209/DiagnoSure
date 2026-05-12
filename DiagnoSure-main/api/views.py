from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from .models import *
from .serializers import *

# CREATE USER
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email).first()
    if user and check_password(password, user.password):
        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        })
    return Response({"error": "Invalid credentials"}, status=401)


import re

# AI LOGIC (FIXED)
def predict_disease(user_symptoms):
    diseases = Disease.objects.all()
    best_match = None
    max_score = 0

    # Isolate valid words naturally out of any format the frontend sends
    user_text = " ".join(user_symptoms).lower()
    stop_words = {"i", "have", "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "with", "my", "am", "feeling", "of", "some", "very", "it", "is", "got", "been"}
    user_words = set(re.findall(r'\b[a-z]{2,}\b', user_text)) - stop_words

    for disease in diseases:
        score = 0

        for disease_symptom in disease.symptoms:
            ds_lower = disease_symptom.lower()
            
            # High priority: The exact symptom phrase appears in the user's sentence
            if ds_lower in user_text:
                score += 3
            else:
                # Fallback: Keyword intersection. (e.g. "headache" matches with "mild headache")
                ds_words = set(re.findall(r'\b[a-z]{2,}\b', ds_lower)) - stop_words
                common = user_words.intersection(ds_words)
                if common:
                    score += len(common)

        # Update if it's the strongest match so far AND has at least 1 validated point
        if score > max_score and score >= 1:
            max_score = score
            best_match = disease

    return best_match


# ANALYSIS API (FIXED)
@api_view(['POST'])
def analyze(request):
    user_id = request.data.get("user_id")
    symptoms = request.data.get("symptoms", [])

    # Support if frontend sends array or string
    if isinstance(symptoms, str):
        symptoms_list = [s.strip() for s in symptoms.split(",")]
    else:
        symptoms_list = symptoms

    disease = predict_disease(symptoms_list)

    if not disease:
        return Response([{"disease": "No match found", "score": 0, "precautions": [], "risk": "Low"}])

    # For presentation: grab fallback user if user_id missing
    user = User.objects.filter(id=user_id).first() if user_id else User.objects.first()

    if user:
        Report.objects.create(
            user=user,
            disease=disease,
            risk=disease.severity
        )

    # Calculate a simple UI risk score based on severity length or fallback
    score = 85 if disease.severity.lower() == "high" else 65 if disease.severity.lower() == "medium" else 45

    # Return exactly what final1/script.js expects in a list so .forEach works
    return Response([{
        "disease": disease.name,
        "score": score,
        "risk": disease.severity,
        "precautions": disease.precautions,
        "description": disease.description,
        "symptoms": disease.symptoms,
        "diet": disease.diet
    }])


# CHATBOT (same)
@api_view(['POST'])
def chatbot(request):
    msg = request.data.get("message").lower()

    if "fever" in msg:
        reply = "You may have an infection."
    elif "headache" in msg:
        reply = "Take rest and hydrate."
    else:
        reply = "Please describe symptoms clearly."

    return Response({"reply": reply})

@api_view(['GET'])
def user_reports(request, user_id):
    reports = Report.objects.filter(user_id=user_id).select_related('disease').order_by('-created_at')
    data = []
    for report in reports:
        data.append({
            "id": report.id,
            "disease_name": report.disease.name,
            "risk": report.risk,
            "created_at": report.created_at.strftime("%B %d, %Y at %I:%M %p"),
            "diet": report.disease.diet,
            "precautions": report.disease.precautions,
            "symptoms": report.disease.symptoms
        })
    return Response(data)

@api_view(['GET', 'POST', 'DELETE'])
def manage_family(request):
    if request.method == 'POST':
        serializer = FamilyMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'GET':
        user_id = request.query_params.get('user_id')
        if user_id:
            family = FamilyMember.objects.filter(user_id=user_id)
            serializer = FamilyMemberSerializer(family, many=True)
            return Response(serializer.data)
        return Response({"error": "user_id required"}, status=400)
        
    elif request.method == 'DELETE':
        member_id = request.data.get('member_id')
        try:
            member = FamilyMember.objects.get(id=member_id)
            member.delete()
            return Response({"message": "Member deleted"})
        except FamilyMember.DoesNotExist:
            return Response({"error": "Member not found"}, status=404)
