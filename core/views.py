from django.shortcuts import render


def home(request):
    """
    Представление для отображения главной страницы.
    """
    return render(request, "core/home.html")
