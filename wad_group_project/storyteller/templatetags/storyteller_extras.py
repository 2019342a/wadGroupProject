from django import template
from storyteller.models import Category
from django.db.models import Count


register = template.Library()

@register.inclusion_tag('storyteller/cats.html')
def get_category_list(cat = None):
    return {'cats': Category.objects.annotate(num_stories=Count('story')).order_by('-num_stories'), 'act_cat': cat}
