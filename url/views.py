from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import qrcode
from io import BytesIO
from .models import Url
import base64

def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    return buffer.getvalue()

def index(request):
    context = {}
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            # Check if the URL already exists
            url = Url.objects.filter(original_url=original_url).first()
            if url:
                short_url = request.build_absolute_uri('/') + url.short_code
                messages.info(request, "URL already exists. Short URL retrieved!")
            else:
                url = Url.objects.create(original_url=original_url)
                short_url = request.build_absolute_uri('/') + url.short_code
                messages.success(request, "Short URL Generated!")
            
            context['short_url'] = short_url
            qr_code = generate_qr_code(short_url)
            qr_code_base64 = base64.b64encode(qr_code).decode('utf-8')
            context['qr_code'] = qr_code_base64
    return render(request, 'index.html', context)

def redirect_to_original(request, short_code):
    url = Url.objects.get(short_code=short_code)
    return redirect(url.original_url)
