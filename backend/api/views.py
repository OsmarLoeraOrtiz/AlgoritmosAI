from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SVMParamSerializer
from ml_engine.controller import MLController

class VisualizeSVMView(APIView):
    def get(self, request):
        # Validar parámetros de la URL
        serializer = SVMParamSerializer(data=request.query_params)
        
        if serializer.is_valid():
            params = serializer.validated_data
            # Llamar al motor de ML
            data = MLController.get_svm_visualization(
                kernel=params['kernel'],
                C=params['C'],
                gamma=params['gamma']
            )
            return Response(data)
        
        return Response(serializer.errors, status=400)