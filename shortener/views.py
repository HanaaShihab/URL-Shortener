from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortURL
import string
import random

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