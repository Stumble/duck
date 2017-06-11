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
    return render(request, 'duckPolyMetrix/index.html', context)

def getResult(request, projectName):
	print request
	print projectName
	print "123"
	logger.info("123")
	projectDir = os.path.dirname(os.path.dirname(__file__)) + "/project/" + projectName
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
