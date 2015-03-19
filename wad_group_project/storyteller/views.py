from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from storyteller.models import Category, OngoingStory, CompletedStory, User
from django.db.models import Q

def index(request):
    category_list = Category.objects.order_by('-stories')[:5]
    completed_story_list_top = CompletedStory.objects.order_by('-rating')[:5]
    completed_story_list_new = CompletedStory.objects.order_by('-creation_date')[:5]
    completed_story_list_popular = CompletedStory.objects.order_by('-views')[:5]
    ongoing_story_list = OngoingStory.objects.order_by('-creation_date')[:5]
    
    context_dict = {'categories': category_list, 'completed_stories_top': completed_story_list_top, 'completed_stories_popular': completed_story_list_popular,
    'ongoing_stories': ongoing_story_list, 'completed_stories_new': completed_story_list_new, }

    response = render(request,'storyteller/index.html', context_dict)

    return response
	
def story(request, story_slug):
    context_dict = {}
    
    try:
        story = CompletedStory.objects.get(slug=story_slug)
        context_dict['title']=story.title
        context_dict['text']=story.story_text
        context_dict['creator']=story.creator
    
    except:
        pass
        
    return render(request, 'storyteller/story.html', context_dict)
    
def category(request, category_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_slug)
        context_dict['category_name'] = category.name

        completed_stories = CompletedStory.objects.filter(category=category)

        context_dict['completed_stories'] = completed_stories

        context_dict['category'] = category
        
    except Category.DoesNotExist:
        pass

    return render(request, 'storyteller/category.html', context_dict)
    
def search(request):
    qTerm = request.GET.get('q')
    context_dict = {}
    result_list = []            
    completed_story_list = CompletedStory.objects.filter(Q(title__icontains=qTerm))
    user_list = User.objects.filter(Q(name__icontains=qTerm))
    ongoing_story_list = OngoingStory.objects.filter(Q(title__icontains=qTerm))
    
    context_dict['completed_story_list'] = completed_story_list
    context_dict['ongoing_story_list'] = ongoing_story_list
    context_dict['user_list'] = user_list
    
    return render(request, 'storyteller/search.html', context_dict)
    