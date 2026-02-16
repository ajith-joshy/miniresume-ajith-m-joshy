import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CandidateSerializer
from django.conf import settings

# In-memory storage
candidates_db = {}

if not os.path.exists(settings.MEDIA_ROOT):
    os.makedirs(settings.MEDIA_ROOT)
identity=1

from rest_framework.decorators import api_view
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"}, status=200)

class CandidateViewSet(viewsets.ViewSet):
    serializer_class = CandidateSerializer

    # CREATE (Upload Resume)
    def create(self, request):
        global identity
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            candidate_id = identity
            identity += 1

            skills_string = data["skill_set"]
            skills_list = [s.strip().lower() for s in skills_string.split(",")]
            data["skill_set"] = skills_list

            file = data["resume"]
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in ["pdf", "doc", "docx"]:
                return Response(
                    {"error": "Only PDF, DOC, DOCX allowed"},
                    status=400
                )
            file_path = os.path.join(settings.MEDIA_ROOT, f"{candidate_id}_{file.name}")
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            data["id"] = candidate_id
            data["resume"] = file_path
            candidates_db[candidate_id] = data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

    # LIST with Filters
    def list(self, request):
        skill = request.query_params.get("skill")
        experience = request.query_params.get("experience")
        grad_year = request.query_params.get("graduation_year")
        results = list(candidates_db.values())
        if skill:
            results = [
                c for c in results
                if skill.lower() in [s.lower() for s in c["skill_set"]]
            ]
        if experience:
            results = [
                c for c in results
                if int(c["years_of_experience"]) >= int(experience)
            ]
        if grad_year:
            results = [
                c for c in results
                if int(c["graduation_year"]) == int(grad_year)
            ]
        if not results:
            return Response(
                {"message": "No candidates found"},
                status=200
            )
        return Response(results)

    # RETRIEVE by ID
    def retrieve(self, request, pk=None):
        pk=int(pk)
        candidate=candidates_db.get(pk)
        if not candidate:
            return Response({"error": "No candidate found"}, status=404)
        return Response(candidate)

    # DELETE
    def destroy(self, request, pk=None):
        pk=int(pk)
        candidate = candidates_db.pop(pk, None)
        if not candidate:
            return Response({"error": "Not found"}, status=404)
        file_path=candidate["resume"]
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response({"message": "Deleted successfully"})