from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortURL
import string
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


def generate_short_code():
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(5))
        if not ShortURL.objects.filter(short_code = code).exists():
            return code

def home(request):
    shortened_url = None

    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        if long_url:
            if not long_url.startswith(('http://', 'https://')):
                long_url = 'http://' + long_url

            existing_entry = ShortURL.objects.filter(original_url = long_url).first()
            if existing_entry:
                code = existing_entry.short_code
            else:
                code = generate_short_code()
                ShortURL.objects.create(original_url = long_url, short_code = code)
            shortened_url = f"127.0.0.1:8000/{code}"
    return render(request, "shortener/index.html", {"shortened_url": shortened_url})

def redirect_url(request, short_code):
    url_mapping = get_object_or_404(ShortURL, short_code = short_code)
    return redirect(url_mapping.original_url)

class LogoutView(APIView):
    # Only logged-in users with a valid token can hit this endpoint
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Grab the refresh token sent by the frontend
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            # Blacklist it permanently
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_250_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Blocks any user who isn't logged in with a valid JWT
def api_shorten_url(request):
    long_url = request.data.get("long_url")
    if not long_url:
        return Response({"error": "URL is required."}, status=status.HTTP_400_BAD_REQUEST)
        
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'https://' + long_url
        
    # Check if this URL already exists
    existing_entry = ShortURL.objects.filter(original_url=long_url).first()
    
    if existing_entry:
        code = existing_entry.short_code
    else:
        code = generate_short_code()
        ShortURL.objects.create(original_url=long_url, short_code=code)
        
    shortened_url = f"127.0.0.1:8000/{code}"
    return Response({"shortened_url": shortened_url}, status=status.HTTP_201_CREATED)