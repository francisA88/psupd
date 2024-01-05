from django.shortcuts import render
import requests


from .forms import UpdateForm

def is_valid_str(string) -> bool:
    if string == None: return False
    return string.replace(' ', '')
def are_valid_strs(*strings):
    return all(map(is_valid_str, strings))


def index(request):
    form = UpdateForm()
    context = {
        'form': form,
        'error': None
    }
    if request.method == 'POST':
        data = request.POST
        api_key = data['api_key']
        #For the CV link
        cv_link = data.get('cv_link')
        #For the skills section
        skill_abbr = data.get('skill_abbr')
        skill_name = data.get('skill_name')
        description = data.get('description')

        #For the projects section
        project_title = data.get('project_title')
        project_display_image = request.FILES.get('project_display_image')
        project_link = data.get('project_link')
        project_description = data.get('project_description')

        print(description)
        print(project_description)
        print(project_display_image, dir(project_display_image))

        PF_SITE = 'https://francis-65e0.onrender.com'
        if are_valid_strs(cv_link):
            response = requests.post(PF_SITE+'/update/cv', data={
                'key': api_key,
                'link': cv_link
            })
            if response.status_code == 401:
                context['error'] = 'Error: API Key Mismatch'
                
        if are_valid_strs(skill_abbr, skill_name, description):
            response = requests.post(PF_SITE+'/update/skill', data={
                'key': api_key,
                'skill_name': skill_name,
                'abbr': skill_abbr,
                'description': description
            })
            if response.status_code == 401:
                context['error'] = 'Error: API Key Mismatch'

        if are_valid_strs(project_title, project_link, project_description) and project_display_image:
            response = requests.post(PF_SITE+'/update/project', data={
                'key': api_key,
                'project_name': project_title,
                'project_description': project_description,
                'image': project_display_image,
                'link': project_link
            })
            if response.status_code == 401:
                context['error'] = 'Error: API Key Mismatch'
    
    return render(request, 'index.html', context)
