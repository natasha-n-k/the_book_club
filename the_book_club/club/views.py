from django.shortcuts import render

def club(request):
    return render(request, 'club/club.html')