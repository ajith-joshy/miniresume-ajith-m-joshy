from rest_framework import serializers

class CandidateSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=30)
    dob = serializers.DateField()
    contact_number = serializers.CharField(max_length=15)
    contact_address = serializers.CharField()
    education_qualification = serializers.CharField()
    graduation_year = serializers.IntegerField(min_value=1900, max_value=2100)
    years_of_experience = serializers.IntegerField(min_value=0)
    skill_set = serializers.CharField(help_text="Enter skills separated by commas")
    resume = serializers.FileField()