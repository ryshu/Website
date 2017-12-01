from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from . import models
import json

def index(request):
	return render(request, "homepage/index.html")
