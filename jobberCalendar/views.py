from django.shortcuts import render, redirect   
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os
import dotenv
import datetime
from dateutil import relativedelta

from .tasks import scrape_spiffy

# Create your views here.
@login_required(login_url='/home/')
def loading(request):
    return render(request, "loading.html")

def home(request):
    return render(request, "home.html")

@login_required(login_url='/home/')
def index(request):
    num_jobs = {
            "current": [], 
            "next": []
    }
    task = scrape_spiffy.delay(num_jobs)
    return render(request, "index.html", {"data": json.dumps(num_jobs)})
