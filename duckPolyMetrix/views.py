# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

import logging
import json

logger = logging.getLogger(__name__)

def index(request):
    context = {'mytest': "latest_question_list"}
    return render(request, 'duckPolyMetrix/index.html', context)

def getResult(request, projectName):
	print request
	print projectName
	print "123"
	logger.info("123")

	return HttpResponse("Hello, there")

# Create your views here.
