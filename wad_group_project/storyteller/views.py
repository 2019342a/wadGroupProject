from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from storyteller.models import Category, OngoingStory, CompletedStory

def index(request):
    category_list = Category.objects.order_by('-stories')[:5]
    completed_story_list = CompletedStory.objects.order_by('-rating')[:5]
    ongoing_story_list = OngoingStory.objects.order_by('-creation_date')[:5]
    
    context_dict = {'categories': category_list, 'completed_stories': completed_story_list,
    'ongoing_stories': ongoing_story_list}

    response = render(request,'storyteller/index.html', context_dict)

    return response