from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home.html")


def bookclub_view(request):
    return render(request, "book_club.html")


def book_view(request):
    return render(request, "book_sample.html")


def chapterdiscussion_view(request):
    return render(request, "book_sample.html")
