from django import forms

class UpdateForm(forms.Form):
    api_key = forms.CharField(min_length=10)
    cv_link = forms.CharField(min_length=1, required=False)
    
    skill_abbr = forms.CharField(label='Skill Abbreviation (Min. of three letters)', max_length=3, min_length=2, required=False)
    skill_name = forms.CharField(label='Skill name', max_length=25, required=False)
    description = forms.CharField(max_length=90, 
        widget=forms.Textarea(), required=False)
    
    project_title = forms.CharField(max_length=15, required=False)
    project_display_image = forms.ImageField(required=False)
    project_link = forms.URLField(max_length=60, required=False)
    project_description = forms.CharField(max_length=110, 
                                          widget=forms.Textarea(), required=False)