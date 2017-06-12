# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse

import logging
from parseJson.parseJson import parse
import os
import sys

logger = logging.getLogger(__name__)

def handle_uploaded_file(f, projectName):
		projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json/" + projectName
		if not os.path.exists(projectDir):
			os.makedirs(projectDir)
		with open(projectDir+'/result.json', 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)

def changeProgram(request, program):
	projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json/"
	print 'in change program'
	request.session['project'] = program

	context = {}
	if 'project' in request.session:
		context['project'] = request.session['project']

	projectList = []
	for item in os.listdir(projectDir):
		if os.path.isdir(projectDir+item):
			projectList.append(item)
	context['projectList'] = projectList
	return render(request, 'website/index.html', context)

def index(request):
		projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json/"

		projectList = []
		for item in os.listdir(projectDir):
			if os.path.isdir(projectDir+item):
				if not 'project' in request.session:
					request.session['project'] = item
				projectList.append(item)

		context = {}
		if 'project' in request.session:
			context['project'] = request.session['project']

		context['projectList'] = projectList
		return render(request, 'website/index.html', context)

def uploadProjectJsonFile(request):
	handle_uploaded_file(request.FILES['inputFile'], request.POST['inputProjectName'])
	getResult(request.POST['inputProjectName'])
	request.session['project'] = request.POST['inputProjectName']

	context = {}
	if 'project' in request.session:
		context['project'] = request.session['project']

	for item in os.listdir(projectDir):
		if os.path.isdir(projectDir+item):
			projectList.append(item)
	context['projectList'] = projectList
	return render(request, 'website/index.html', context)


def collapsibletree(request, matrix="linesOfCode", query="inherited"):
	context = {}
	context['matrix'] = matrix
	context['query'] = query
	if 'project' in request.session:
		context['project'] = request.session['project']
	if "selectType" in request.POST:
		context['query'] = request.POST['query']
	if "selectMetrix" in request.POST:
		context['matrix'] = request.POST['selectMetrix']
	print context

	return render(request, 'website/collapsibletree.html', context)


def zoomablesunburst(request, matrix="linesOfCode", query="inherited"):
	context = {}
	context['matrix'] = matrix
	context['query'] = query
	if 'project' in request.session:
		context['project'] = request.session['project']
	if "selectType" in request.POST:
		context['query'] = request.POST['selectType']
	if "selectMetrix" in request.POST:
		context['matrix'] = request.POST['selectMetrix']
	print context
	return render(request, 'website/zoomablesunburst.html', context)

def edgebundling(request, matrix="linesOfCode", query="inherited"):
	context = {}
	context['matrix'] = matrix
	context['query'] = query
	if 'project' in request.session:
		context['project'] = request.session['project']
	if "selectType" in request.POST:
		context['query'] = request.POST['query']
	if "selectMetrix" in request.POST:
		context['matrix'] = request.POST['selectMetrix']
	print context
	return render(request, 'website/edgebundling.html', context)

def circlepacking(request, matrix="linesOfCode", query="inherited"):
	context = {}
	context['matrix'] = matrix
	context['query'] = query
	if 'project' in request.session:
		context['project'] = request.session['project']
	if "selectType" in request.POST:
		context['query'] = request.POST['query']
	if "selectMetrix" in request.POST:
		context['matrix'] = request.POST['selectMetrix']
	print context
	return render(request, 'website/circlepacking.html', context)

def bubblechart(request, matrix="linesOfCode", query="inherited"):
	context = {}
	context['matrix'] = matrix
	context['query'] = query
	if 'project' in request.session:
		context['project'] = request.session['project']
	if "selectType" in request.POST:
		context['query'] = request.POST['query']
	if "selectMetrix" in request.POST:
		context['matrix'] = request.POST['selectMetrix']
	print context
	return render(request, 'website/bubblechart.html', context)


def getResult(projectName):
	print "get result"
	projectDir = os.path.dirname(os.path.dirname(__file__)) + "/duckPolyMetrix/static/json/" + projectName
	print projectDir

	resultJson = projectDir + "/result.json"

	if not os.path.exists(resultJson):
		print resultJson+"project doesn't exist"
		return False

	#try:
	print "ready to parse"
	parse(resultJson, projectDir)

	#except:
	#	return HttpResponse("unexpected error!")

	return True


def parseProject(request, projectName):
	print projectName
	return HttpResponse("parse program")

# Create your views here.
