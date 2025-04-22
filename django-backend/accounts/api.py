from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VerifyCredentialsAPIView(APIView):
    """
    API endpoint to verify user credentials (username and password).
    Accepts POST requests with 'username' and 'password'.
    Returns 200 OK if credentials are valid, 401 Unauthorized otherwise.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
