from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_tables2 import RequestConfig
from django.template import RequestContext
from .models import WearingSession, ExercisePeriod
from .tables import WearingSessionTable, ExercisePeriodTable


def index(request):
	""" View function for the home page """
	# Preview of the latest records
	latestSessions = WearingSession.objects.order_by('-timeStamp')[:5]
	latestPeriods = ExercisePeriod.objects.order_by('-timeStamp')[:5]
	
	# Convert into tabular form
	sessionsT = WearingSessionTable(list(latestSessions))
	periodsT = ExercisePeriodTable(list(latestPeriods))
	return render(request, 'index.html', {'latestSessions':sessionsT, 'latestPeriods':periodsT})

def sessionDetail(request, sessionID):
	# Query the wearing session database with matching sessionID
	session = WearingSession.objects.filter(sessionID=sessionID).get()

	# Query the exercise period database with matching sessionID
	pResult = ExercisePeriod.objects.filter(sessionID_id=sessionID).select_related('sessionID').all()
	periods = [ExercisePeriod.objects.filter(periodID=pID).get() for pID in pResult]

	# Put it in a tabular form 	
	table = ExercisePeriodTable(periods)
	RequestConfig(request).configure(table)
	
	wearingSession = get_object_or_404(WearingSession.objects, pk=sessionID)
	return render(request, 'sessionDetail.html', {'session':session, 'periods':periods, 'table':table})

