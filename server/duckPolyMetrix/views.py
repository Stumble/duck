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


def collapsibletree(request, matrix="linesOfCode"):
	context = {'matrix':matrix}
	return render(request, 'website/collapsibletree.html', context)


def zoomablesunburst(request, matrix="linesOfCode"):
	context = {'matrix':matrix}
	return render(request, 'website/zoomablesunburst.html', context)
    
def edgebundling(request):
	context = {}
	return render(request, 'website/edgebundling.html', context)

def circlepacking(request):
	context = {}
	return render(request, 'website/circlepacking.html', context)


def getResult(request, attribute='linesOfCode', projectName='default'):
	print "get result"
	projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json"
	print projectDir
	if not os.path.exists(projectDir):
		os.makedirs(projectDir)

	resultJson = projectDir + "/result.json"

	if not os.path.exists(resultJson):
		return HttpResponse("json file doesn't exist, please upload project first")

	#try:
	print "ready to parse"
	parse(resultJson, projectDir)

	#except:
	#	return HttpResponse("unexpected error!")

	return HttpResponse("parse success")


def parseProject(request, projectName):
	print projectName
	return HttpResponse("parse program")

# Create your views here.
