from dataclasses import dataclass
import encodings
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
import re
from urllib.request import Request, urlopen
import urllib
import ast
from lxml import html


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
                header_data = "-"
                if header:
                    header_data = header.strip()
                job_breadcrumb = soup.find('div', {'class': 'cfe-ui-job-breadcrumbs d-inline-block mr-10'}).get_text()
                job_breadcrumb_data = "-"
                if job_breadcrumb:
                    job_breadcrumb_data = job_breadcrumb.strip()
                content = soup.find("div", class_="job-description").get_text()

                job_features = soup.find('ul', {'class': 'cfe-ui-job-features p-0 fluid-layout-md'}).findAll("li", recursive='"false"')
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
                experience_level = "-"
                project_duration = "-"
                type_of_job = "-"
                project_type = "-"
                job_location = "-"
                fixed_price_hourly_rate = "-"
                weekly_hour_limit = "-"
                for key,value in jobfeature_dict.items():
                    if key == "Experience Level":
                        experience_level = value
                    if key == "Duration":
                        project_duration = value
                    if key == "Hourly":
                        type_of_job = key
                        weekly_hour_limit = value
                    if key == "Fixed-price":
                        type_of_job = key
                        fixed_price_hourly_rate = value
                    if key == "Project Type":
                        project_type = value
                    if key == "location":
                        job_location = value
                    if key == "Hourly Rate":
                        fixed_price_hourly_rate = value

                
                # tree = html.fromstring(response.content)
                # print("tree",tree)
                
                # element1 = tree.xpath('//*[@id="main"]/div/div/div/div[1]/div/div[1]/section[4]/div/div/div[1]')
                # element2 = tree.xpath('//*[@id="main"]/div/div/div/div[1]/div/div[1]/section[4]/div/div/div[2]/div/strong')
                # element3 = tree.xpath('//*[@id="main"]/div/div/div/div[1]/div/div[1]/section[4]/div/div/div[3]/div/strong')
                # for i in element1:
                #     print(i.text)
                skills = soup.find(class_="fluid-layout").findAll("div", recursive='"false"')
                skilldetail = []
                for skill in skills:
                    skilldetail.append(skill.stripped_strings)
                # print("skill detail ----",skilldetail)
                skills_dict = {}
                print(skilldetail)
                for i in skilldetail:
                    value_list = []
                    for id,line in enumerate(i):
                        print(id,line)
                        if id == 0:
                            key = line
                        else:
                            value = line
                            value_list.append(value)
                            # break
                    skills_dict[key] = value_list
                    break
                print("6666666666-------",skills_dict)
                primary_skill_list = []
                secondry_skill_list = []
                other_skill_list = []
                primary_skill = "-"
                secondry_skill = "-"
                other_skill = "-"
                if len(skills_dict) == 1:
                    for key,value in skills_dict.items():
                        primary_skill_list.append(key)
                        for i in value:
                            primary_skill_list.append(i)
                else:
                    for key,value in skills_dict.items():
                        print("key",key)
                        print("value",value)
                        if key == "Full Stack Development Deliverables":
                            primary_skill_list.append(key)
                            for i in value:
                                primary_skill_list.append(i)
                        if key == "Business Size Experience":
                            secondry_skill_list.append(key)
                            for i in value:
                                secondry_skill_list.append(i)
                        if key == "Other":
                            print("hello")
                            for i in value:
                                print(i)
                                other_skill_list.append(i)
                print(primary_skill_list)
                print("other_skill_list",other_skill_list)
                if primary_skill_list:
                    primary_skill = ','.join(primary_skill_list)
                if secondry_skill_list:
                    secondry_skill = ','.join(secondry_skill_list)
                if other_skill_list:
                    other_skill = ','.join(other_skill_list)
                print("primary_skill",primary_skill)
                print("secondry_skill",secondry_skill)
                print("other_skill",other_skill)

                activitys = soup.find("ul", class_="list-unstyled mb-0").findAll("li", recursive='"false"')
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
                client_total_spent_text = "-"
                if client_spend:
                    client_total_spent_text = client_spend.text
                client_hires_text = "-"
                client_total_hire = "-"
                if client_hires:
                    client_hires_text = client_hires.text
                    client_total_hire = client_hires_text.split(",")[0]
                client_hourly_rate_text = "-"
                if client_hourly_rate:
                    client_hourly_rate_text = client_hourly_rate.text
                client_hours_text = "-"
                if client_hours:
                    client_hours_text = client_hours.text
                client_hiring_rate = "-"
                client_open_job = "-"
                client_job_posted_job = "-"
                if client_job_posting_state:
                    client_hiring_rate_list = re.findall('\d*%', client_job_posting_state)
                    client_hiring_rate = ','.join(client_hiring_rate_list)
                    client_open_job = client_job_posting_state.split(",")[-1]
                    client_job_posted_job_1 = client_job_posting_state.split(",")[0]
                    client_job_posted_job_2 = re.findall('\d+', client_job_posted_job_1)
                    client_job_posted_job = client_job_posted_job_2[0]
                
                client_company_profile_text = "-"
                if client_company_profile:
                    client_company_profile_text = client_company_profile
                client_membership = "-"
                if client_contract_date:
                    client_membership = client_contract_date.strip()
                client_open_job_data = "-"
                if client_open_job:
                    client_open_job_data = client_open_job.strip()
                client_total_spent_text_data = "-"
                if client_total_spent_text:
                    client_total_spent_text_data = client_total_spent_text.strip()

                data = {
                    "Task Name":header_data,
                    "Type of Job":type_of_job,
                    "category":job_breadcrumb_data,
                    "experience level":experience_level,
                    "project type":project_type,
                    "client location":client_location,
                    "client membership":client_membership,
                    "client hiring rate":client_hiring_rate,
                    "client open job":client_open_job_data,
                    "client total spent":client_total_spent_text_data,
                    "hourly average rate":client_hourly_rate_text,
                    "job post url":url,
                    "fixed price/hourly rate":fixed_price_hourly_rate,
                    "job location":job_location,
                    "primary skill":primary_skill,
                    "secondary skill":secondry_skill,
                    "other skill":other_skill,
                    "total hour paid by client":client_hours_text,
                    "client total hire":client_total_hire,
                    "client total posted job":client_job_posted_job,
                    "weekly hour limit":weekly_hour_limit,
                    "project duration":project_duration,
                    "client company profile":client_company_profile_text,
                    "Task Description":content,

                }
                return render(request, 'myapp/index.html', {"tags":data})
            except:
                data = {
                    "message":"Please Provide Valid Upwork website url"
                }
                return render(request, 'myapp/index.html', {"error_message":data})
        return render(request, 'myapp/index.html')


class ResultView(View):

    def post(self, request):
        print("hello")
        data = request.POST
        for key,value in data.items():
            print(key,value)
            if key != "csrfmiddlewaretoken":
                data1 = key
        # print(data1)
        vardata1 = bytes(data1, 'utf-8')
        print(type(vardata1))
        dict_str = vardata1.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        print(repr(mydata))
        print(type(mydata))
        print("-----",mydata['Type of Job'])
        print("-----",type(mydata['Type of Job']))
        if mydata['Type of Job'] == "Hourly":
            type_of_job_value = 1
        else:
            type_of_job_value = 0
            
        value_dict = {
                "id": "23ebp2z",
                "custom_id": {},
                "name": mydata['Task Name'],
                "text_content": mydata['Task Description'],
                "description": mydata['Task Description'],
                "orderindex": "7169309.00000000000000000000000000000000",
                "archived": "false",
                "creator": {
                    "id": 3739924,
                    "username": "Paras Chodavadiya",
                    "color": "#03A2FD",
                    "email": "paras@sarvadhi.com",
                    "profilePicture": "https://attachments.clickup.com/profilePictures/3739924_o7C.jpg"
                },
                "assignees": [],
                "watchers": [
                    {
                    "id": 3739924,
                    "username": "Paras Chodavadiya",
                    "color": "#03A2FD",
                    "initials": "PC",
                    "email": "paras@sarvadhi.com",
                    "profilePicture": "https://attachments.clickup.com/profilePictures/3739924_o7C.jpg"
                    }
                ],
                "checklists": [],
                "tags": [],
                "points": {},
                "time_spent": 0,
                "custom_fields": [
                    {
                    "id": "e27bb994-fb6e-4934-9ca2-848abc23c9f3",
                    "name": "Category",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['category'],
                    "required": "false"
                    },
                    {
                    "id": "5fa81aa1-340f-497f-b2d8-c213ae1d0908",
                    "name": "Client Company Profile",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client company profile'],
                    "required": "false"
                    },
                    {
                    "id": "07400e5a-eaf6-4300-980e-4df3ade3d4a6",
                    "name": "Client's hiring rate",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client hiring rate'],
                    "required": "false"
                    },
                    {
                    "id": "18b147ce-b1ac-4abd-a01a-b7a129edaa92",
                    "name": "Client's location",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value":mydata['client location'],
                    "required": "false"
                    },
                    {
                    "id": "c78767b1-a2c7-40ad-8d2d-7028d9dccc0e",
                    "name": "Client's membership",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client membership'],
                    "required": "false"
                    },
                    {
                    "id": "b51ae5c0-c549-4bbd-9b5b-d56621b2c886",
                    "name": "Client's open jobs",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client open job'],
                    "required": "false"
                    },
                    {
                    "id": "3add9e80-1918-4391-b96b-c2618f490595",
                    "name": "Client's total hires",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client total hire'],
                    "required": "false"
                    },
                    {
                    "id": "028a911e-be4a-4caf-b2fc-d6d550acc4c7",
                    "name": "Client's total posted jobs",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client total posted job'],
                    "required": "false"
                    },
                    {
                    "id": "b287f060-ac7f-42fc-85e7-c24fbe107262",
                    "name": "Client's total spent",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['client total spent'],
                    "required": "false"
                    },
                    {
                    "id": "36ac8426-39f4-495c-b4fa-781f2f436071",
                    "name": "Experience Level",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['experience level'],
                    "required": "false"
                    },
                    {
                    "id": "41af3fa8-cf11-4869-9509-f4426fc9fe33",
                    "name": "Fixed Price / Hourly Rate",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['fixed price/hourly rate'],
                    "required": "false"
                    },
                    {
                    "id": "9733f6ad-bb4b-4ed3-8aa4-0f481a1cadb7",
                    "name": "Hourly Average rate",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['hourly average rate'],
                    "required": "false"
                    },
                    {
                    "id": "d413bee7-4c2f-44dc-84b2-e04bc1267af6",
                    "name": "Job Location",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['job location'],
                    "required": "false"
                    },
                    {
                    "id": "bbc7c539-38b2-408e-8fa7-a11d15c87b6a",
                    "name": "Job post URL",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['job post url'],
                    "required": "false"
                    },
                    {
                    "id": "acf36e4a-5ca1-46eb-96dc-c538e0aa1b90",
                    "name": "Other Skills",
                    "type": "text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['other skill'],
                    "required": "false"
                    },
                    {
                    "id": "506d38bd-a6e2-49bb-b376-05e314cd70c3",
                    "name": "Primary Skills",
                    "type": "text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['primary skill'],
                    "required": "false"
                    },
                    {
                    "id": "d5e94415-3802-43a0-ab4b-2100f1540527",
                    "name": "Project Duration",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['project duration'],
                    "required": "false"
                    },
                    {
                    "id": "7f1840e8-4558-41c4-a48e-b28f6dec9a97",
                    "name": "Project Type",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['project type'],
                    "required": "false"
                    },
                    {
                    "id": "1af7e84a-3061-4580-bbc2-ec2d266e9319",
                    "name": "Secondary Skills",
                    "type": "text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['secondary skill'],
                    "required": "false"
                    },
                    {
                    "id": "ebd59fa4-5c44-4a62-8c24-f7e3870187e9",
                    "name": "Total hours paid by client",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['total hour paid by client'],
                    "required": "false"
                    },
                    {
                    "id": "fde9585d-6104-4473-b33c-a7a1e6f815c2",
                    "name": "Type of Job",
                    "type": "drop_down",
                    "type_config": {
                        "default": 0,
                        "placeholder": {},
                        "options": [
                        {
                            "id": "07b51327-92b2-4fe9-9ba1-f3ef3c25231a",
                            "name": "Fixed",
                            "color": {},
                            "orderindex": 0
                        },
                        {
                            "id": "28d4f728-ea84-40a4-8890-dba528c185a1",
                            "name": "Hourly",
                            "color": {},
                            "orderindex": 1
                        }
                        ]
                    },
                    "date_created": "1647166163217",
                    "hide_from_guests": "false",
                    "value": type_of_job_value,
                    "required": "false"
                    },
                    {
                    "id": "338cb162-3940-4a18-a931-7b1ef4649f37",
                    "name": "Weekly Hour Limit",
                    "type": "short_text",
                    "type_config": {},
                    "hide_from_guests": "false",
                    "value": mydata['weekly hour limit'],
                    "required": "false"
                    }
                ],
                "dependencies": [],
                "linked_tasks": [],
                "team_id": "3672779",
                "url": "https://app.clickup.com/t/23ebp2z",
                "permission_level": "create",
                "list": {
                    "id": "175339326",
                    "name": "Proposals",
                    "access": "true"
                },
                "project": {
                    "id": "103457058",
                    "name": "Proposals",
                    "hidden": "false",
                    "access": "true"
                },
                "folder": {
                    "id": "103457058",
                    "name": "Proposals",
                    "hidden": "false",
                    "access": "true"
                },
                "space": {
                    "id": "55498314"
                },
                "attachments": []
                }
        
        # varAllValues ="""value_dict"""

        
        headers = {
        'Authorization': 'pk_3739924_7H8HYUCGO3N6CZJOMNBIQ8VJV0SVB33O',
        'Content-Type': 'application/json'
        }
        
        # varBinData = bytes(varAllValues, 'utf-8')
        varBinData = json.dumps(value_dict).encode('utf-8')
        # varBinData = bytes(varAllValues, 'utf-8')
        aaa = Request('https://api.clickup.com/api/v2/list/175339326/task', data=varBinData, headers=headers)

        response_body = urlopen(aaa).read()
        return render(request, 'myapp/index.html', {"response_body":"The proposal has been added to ClickUp successfully"})