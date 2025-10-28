from rest_framework import serializers
from jobs.models import Jobs, ReceiveJobApplication

# Job List
class jobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'

# apply Job
class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiveJobApplication
        fields = "__all__"