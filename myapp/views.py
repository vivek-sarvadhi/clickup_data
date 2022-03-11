from dataclasses import dataclass
from django.shortcuts import render, redirect
from myapp.forms import CustomUserForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from myapp.models import CustomUser
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import json
# Create your views here.
class RegisterView(View):
    
    def get(self, request):
        form = CustomUserForm()
        return render(request, 'myapp/registration_form.html', {'form':form})

    def post(self, request):
        if request.method == "POST":
            form = CustomUserForm(request.POST or request.FILES)
            if form.is_valid():
                print(form)
                form.save()
                return render(request, 'myapp/registration_form.html', {'form':form})
            messages.error(request, "email id already used")
            return render(request, 'myapp/registration_form.html', {'form':form})


class LoginView(View):

    def get(self, request):
        form = CustomUserForm()
        return render(request, 'myapp/login_form.html', {'form':form})

    def post(self, request):
        form = CustomUserForm()
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("hello")
        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "permission not allow")
                return render(request, 'myapp/login_form.html', {'form':form})
        else:
            messages.error(request, "email or password is not correct")
            return render(request, 'myapp/login_form.html', {'form':form})
        # return render(request, 'myapp/login_form.html', {'from':form})


class IndexView(View):

    def get(self, request):
        url = request.GET.get('url')
        if url:
            try:
                print("url",url)
                # url = "https://www.upwork.com/freelance-jobs/apply/Build-Cryptocurrency-Exchange_~01b0b5c4fd2b926732/"
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
                response = requests.get(url, headers=headers)
                htmlContent = response.content
                soup = BeautifulSoup(htmlContent, 'html.parser')
                header = soup.find("header", class_="up-card-header d-flex").get_text()
                job_breadcrumb = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'}).get_text()
                content = soup.find("div", class_="job-description").get_text()

                job_features = soup.find('ul', {'class': 'cfe-ui-job-features p-0 fluid-layout-md'}).findAll("li", recursive=False)
                jobfeaturedetail = []
                for job_feature in job_features:
                    jobfeaturedetail.append(job_feature.stripped_strings)
                jobfeature_dict = {}
                for i in jobfeaturedetail:
                    key1 = ""
                    value1 = ""
                    for id,line in enumerate(i):
                        if id == 1:
                            key = line
                            if key.startswith('-$'):
                                key1 = key
                                key = "Hourly Rate"
                        else:
                            value = line
                            if value.startswith('$'):
                                value1 = value
                        new_value = value1 + key1
                        if value == "Hourly":
                            value = new_value
                    for jobfeature_key in jobfeature_dict.keys():
                        if jobfeature_key == key:
                            key = "location"
                    jobfeature_dict[key] = value


                skills = soup.find(class_="fluid-layout").findAll("div", recursive=False)
                skilldetail = []
                for skill in skills:
                    skilldetail.append(skill.stripped_strings)
                skills_dict = {}
                for i in skilldetail:
                    value_list = []
                    for id,line in enumerate(i):
                        if id == 0:
                            key = line
                        else:
                            value = line
                            value_list.append(value)
                    skills_dict[key] = value_list


                activitys = soup.find("ul", class_="list-unstyled mb-0").findAll("li", recursive=False)
                activitydetail = []
                for activity in activitys:
                    activitydetail.append(activity.stripped_strings)
                activity_dict = {}
                for i in activitydetail:
                    activity_list = []
                    for id,line in enumerate(i):
                        if id == 1:
                            key = line
                        else:
                            value = line
                            activity_list.append(value)
                    activity_dict[key] = activity_list


                client_location = soup.find('li', {'data-qa': 'client-location'}).get_text()
                client_job_posting_state = soup.find('li', {'data-qa': 'client-job-posting-stats'}).get_text()
                client_company_profile = soup.find('li', {'data-qa': 'client-company-profile'}).get_text()
                client_contract_date = soup.find('li', {'data-qa': 'client-contract-date'}).get_text()
                client_spend = soup.find('strong', {'data-qa': 'client-spend'})
                client_hires = soup.find('div', {'data-qa': 'client-hires'})
                client_hourly_rate = soup.find('strong', {'data-qa': 'client-hourly-rate'})
                client_hours = soup.find('div', {'data-qa': 'client-hours'})
                client_hire_spend = ""
                client_rate_hourly = ""
                if client_spend or client_hires is not None:
                    client_hire_spend = client_spend.text, client_hires.text
                if client_hourly_rate or client_hours is not None:
                    client_rate_hourly = client_hourly_rate.text, client_hours.text
                client_total_spent = ""
                if client_spend:
                    client_total_spent = client_spend.text
                client_avarage_rate = ""
                if client_spend:
                    client_avarage_rate = client_hourly_rate.text
                data = {
                    "Task Name":header,
                    "Type of Job":"Type of job",
                    "category":job_breadcrumb,
                    "experience level":"experience level",
                    "project type":"project type",
                    "client location":client_location,
                    "client membership":client_contract_date,
                    "client hiring rate":client_rate_hourly,
                    "client open job":client_job_posting_state,
                    "client total spent":client_total_spent,
                    "hourly average rate":client_avarage_rate,
                    "job post url":url,
                    "fixed price/hourly rate":"fixed price/hourly rate",
                    "job location":"job location",
                    "primary skill":"primary skill",
                    "secondary skill":"secondary skill",
                    "other skill":"other skill",
                    "total hour paid by client":client_rate_hourly,
                    "client total hire":client_hire_spend,
                    "client total posted job":client_job_posting_state,
                    "weekly hour limit":"weekly hour limit",
                    "project duration":"project duration",
                    "client company profile":client_company_profile,
                    "Task Description":content,

                }
                return render(request, 'myapp/index.html', {"tags":data})
            except:
                data = {
                    "message":"Please Provide Valid Upwork website url"
                }
                return render(request, 'myapp/index.html', {"data":data})
        return render(request, 'myapp/index.html')


class ResultView(View):

    def get(self, request):
        try:
            url = request.GET.get('url')
            print("url",url)
            # url = "https://www.upwork.com/freelance-jobs/apply/Build-Cryptocurrency-Exchange_~01b0b5c4fd2b926732/"
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
            response = requests.get(url, headers=headers)
            htmlContent = response.content
            soup = BeautifulSoup(htmlContent, 'html.parser')
            header = soup.find("header", class_="up-card-header d-flex").get_text()
            job_breadcrumb = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'}).get_text()
            job_link = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'})
            posted_on = soup.find('div', {'id': 'posted-on'}).get_text()
            location_restrication = soup.find('div', {'class': 'mt-20 d-flex align-items-center location-restriction'}).get_text()
            job_link_url = job_link.a['href']
            content = soup.find("div", class_="job-description").get_text()

            job_features = soup.find('ul', {'class': 'cfe-ui-job-features p-0 fluid-layout-md'}).findAll("li", recursive=False)
            jobfeaturedetail = []
            for job_feature in job_features:
                jobfeaturedetail.append(job_feature.stripped_strings)
            jobfeature_dict = {}
            for i in jobfeaturedetail:
                key1 = ""
                value1 = ""
                for id,line in enumerate(i):
                    if id == 1:
                        key = line
                        if key.startswith('-$'):
                            key1 = key
                            key = "Hourly Rate"
                    else:
                        value = line
                        if value.startswith('$'):
                            value1 = value
                    new_value = value1 + key1
                    if value == "Hourly":
                        value = new_value
                for jobfeature_key in jobfeature_dict.keys():
                    if jobfeature_key == key:
                        key = "location"
                jobfeature_dict[key] = value


            skills = soup.find(class_="fluid-layout").findAll("div", recursive=False)
            skilldetail = []
            for skill in skills:
                skilldetail.append(skill.stripped_strings)
            skills_dict = {}
            for i in skilldetail:
                value_list = []
                for id,line in enumerate(i):
                    if id == 0:
                        key = line
                    else:
                        value = line
                        value_list.append(value)
                skills_dict[key] = value_list


            activitys = soup.find("ul", class_="list-unstyled mb-0").findAll("li", recursive=False)
            activitydetail = []
            for activity in activitys:
                activitydetail.append(activity.stripped_strings)
            activity_dict = {}
            for i in activitydetail:
                activity_list = []
                for id,line in enumerate(i):
                    if id == 1:
                        key = line
                    else:
                        value = line
                        activity_list.append(value)
                activity_dict[key] = activity_list


            client_location = soup.find('li', {'data-qa': 'client-location'}).get_text()
            client_job_posting_state = soup.find('li', {'data-qa': 'client-job-posting-stats'}).get_text()
            client_company_profile = soup.find('li', {'data-qa': 'client-company-profile'}).get_text()
            client_contract_date = soup.find('li', {'data-qa': 'client-contract-date'}).get_text()
            client_spend = soup.find('strong', {'data-qa': 'client-spend'})
            client_hires = soup.find('div', {'data-qa': 'client-hires'})
            client_hourly_rate = soup.find('strong', {'data-qa': 'client-hourly-rate'})
            client_hours = soup.find('div', {'data-qa': 'client-hours'})
            client_hire_spend = ""
            client_rate_hourly = ""
            if client_spend or client_hires is not None:
                client_hire_spend = client_spend.stripped_strings, client_hires.stripped_strings
            if client_hourly_rate or client_hours is not None:
                client_rate_hourly = client_hourly_rate.stripped_strings, client_hours.stripped_strings
            data = {
                "Header":header,
                "Job Detail":{
                    "Search more":[job_breadcrumb,job_link_url],
                    "jobs":posted_on,
                    "Location":location_restrication
                },
                "Content":content,
                "Job Features":jobfeature_dict,
                "Skills and Expertise": skills_dict, 
                # "Activity on this": activity_dict,
                "About the client": {
                    "client_location":client_location,
                    "client_job_posting_state":client_job_posting_state,
                    "client_company_profile":client_company_profile,
                    "client_contract_date":client_contract_date,
                    "client_hire_spend":client_hire_spend,
                    "client_rate_hourly":client_rate_hourly

                },
            }
            print(data)
            return render(request, 'myapp/result_data.html', {"data":data})
            # return JsonResponse(data)
        except:
            data = {
                "message":"Please Provide Valid Upwork website url"
            }
            return render(request, 'myapp/result_data.html', {"data":data})
            # return JsonResponse(data)