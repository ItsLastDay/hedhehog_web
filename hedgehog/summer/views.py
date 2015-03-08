from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

# Create your views here.

@require_GET
def main_page(request):
    return render(request, 'base.html', dict())
