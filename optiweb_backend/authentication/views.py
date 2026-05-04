from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from agent_monitoring.models import ServerMetrics
from agent_monitoring.serializers import ServerMetricsSerializer
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework import permissions
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny

User = get_user_model()

class RegisterUserView(APIView): 
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            web_server_ip = serializer.validated_data['web_server_ip']
            
            # Check if the web_server_ip already exists in the database
            if User.objects.filter(web_server_ip=web_server_ip).exists():
                return Response({"error": "Web server IP already registered."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginUserView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            web_server_ip = serializer.validated_data["web_server_ip"]
            password = serializer.validated_data["password"]

            try:
                user = User.objects.get(web_server_ip=web_server_ip)
                if user.check_password(password):
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key, "message": "Login successful"}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMetricsView(APIView):
    """Handles both GET and POST for user-specific metrics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Return latest metrics for the authenticated user's web server IP"""
        user = request.user
        metrics = ServerMetrics.objects.filter(server_id=user.web_server_ip).order_by('-timestamp')[:1]
        serializer = ServerMetricsSerializer(metrics, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Allow posting server metrics from the agent"""
        serializer = ServerMetricsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Metrics received successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
