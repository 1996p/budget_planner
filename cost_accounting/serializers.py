from rest_framework import serializers
from .models import *


class Test(serializers.ModelSerializer):
    class Meta:
        model = Spending
        fields = '__all__'
