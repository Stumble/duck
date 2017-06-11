# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

import logging
from parseJson.parseJson import parse
import os
import sys

logger = logging.getLogger(__name__)

def index(request):
    context = {'mytest': "latest_question_list"}
    return render(request, 'website/index.html', context)

def collapsibletree(request):
	context = {}
	return render(request, 'website/collapsibletree.html', context)


def zoomablesunburst(request):
	context = {}
	return render(request, 'website/zoomablesunburst.html', context)

def getResult(request, projectName):
	projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json"
	print projectDir
	if not os.path.exists(projectDir):
		os.makedirs(projectDir)

	resultJson = projectDir + "/result.json"

	if not os.path.exists(resultJson):
		return HttpResponse("json file doesn't exist, please upload project first")

	#try:
	parse(resultJson, projectDir)

	#except:
	#	return HttpResponse("unexpected error!")





	return HttpResponse("Hello, there")

def parseProject(request, projectName):
	print projectName
	return HttpResponse("parse program")

# Create your views here.
