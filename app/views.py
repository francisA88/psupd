import base64

from django.shortcuts import render

from .forms import UpdateForm
from .db_operations import *


def is_valid_str(string) -> bool:
    if string == None: return False
    return string.replace(' ', '')

def are_valid_strs(*strings) -> bool:
    return all(map(is_valid_str, strings))


def index(request):
    form = UpdateForm()
    context = {
        'form': form,
        'errors': []
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

        if match_api_key(api_key):
            if are_valid_strs(cv_link):
                cv_update_successful = update_cv_link(cv_link)
                if not cv_update_successful:
                    context['errors'].append('Error updating CV link')
            
            if are_valid_strs(skill_abbr, skill_name, description):
                skill_update_successful = add_skill(skill_abbr, skill_name, description)
                if not skill_update_successful:
                    context['errors'].append('Error updating skills')
            
            if are_valid_strs(project_title, project_description, project_link) and project_display_image:
                b64_image = base64.b64encode(project_display_image.read())
                projects_update_successful = add_project(project_title, b64_image, project_link, project_description)
                if not projects_update_successful:
                    context['errors'].append('Error updating projects')

        else:
            context['errors'].append('Invalid API key.')
    
    return render(request, 'index.html', context)
