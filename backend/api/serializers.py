from rest_framework import serializers

class SVMParamSerializer(serializers.Serializer):
    kernel = serializers.ChoiceField(choices=['linear', 'rbf', 'poly', 'sigmoid'], default='rbf')
    C = serializers.FloatField(min_value=0.01, max_value=100.0, default=1.0)
    gamma = serializers.ChoiceField(choices=['scale', 'auto'], default='scale')