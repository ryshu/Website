from django.shortcuts import render, redirect, get_object_or_404

from asso.models import Asso as AssoModel
from news.models import News as NewsModel

import json
import operator

def index(request):

	context = {
        'assos' : AssoModel.objects.filter(homepage_highlight = True).order_by('priority').all(),
        'news' : NewsModel.objects.filter(homepage_highlight = True ).order_by('homepage_highlight')[:3]
    }
	return render(request, "homepage/index.html", context)

