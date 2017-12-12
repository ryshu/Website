from django import forms
from . import models


class WrapperClearableinput(forms.widgets.ClearableFileInput):
    template_with_initial = (
        '<span id="pic"><img src="%(initial_url)s" alt="photo profil" /></span</p><p>'
        '%(clear_template)s</p><p><label>%(input_text)s: </label>%(input)s'
    )

    template_with_clear = '<label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label><span class="align_left"> %(clear)s</span>'

class NewsForm(forms.ModelForm):
    prefix = 'news'

    class Meta:
        model = models.News
        fields = [
            'title',
            'content',
            'picture',
            'homepage_highlight',
        ]

        labels = {
            'title': 'Titre',
            'content': 'Contenu',
            'picture': 'Image',
            'homepage_highlight' : "Afficher sur la page d'accueil",
        }

        widgets = {
            'picture' : WrapperClearableinput
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', ]
        labels = {'content': 'Commentaire'}

