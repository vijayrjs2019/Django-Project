from rest_framework import serializers
from jobs.models import Jobs, ReceiveJobApplication

# Enquiry
class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'