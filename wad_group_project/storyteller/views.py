from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from itertools import chain
from operator import attrgetter
from storyteller.models import Category, Story, UserProfile
from django.db.models import Q, Count
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from storyteller.forms import UserForm, UserProfileForm, StoryForm

def index(request):
    category_list = Category.objects.annotate(num_stories=Count('story')).order_by('-num_stories')[:5]
    completed_story_list_top = Story.objects.filter(ended=True).order_by('-rating')[:5]
    completed_story_list_new = Story.objects.filter(ended=True).order_by('-creation_date')[:5]
    completed_story_list_popular = Story.objects.filter(ended=True).order_by('-views')[:5]
    ongoing_story_list = Story.objects.filter(ended=False, ending=False).order_by('-creation_date')[:5]

    context_dict = {'categories': category_list, 'completed_stories_top': completed_story_list_top, 'completed_stories_popular': completed_story_list_popular,
    'ongoing_stories': ongoing_story_list, 'completed_stories_new': completed_story_list_new, }

    response = render(request,'storyteller/index.html', context_dict)

    return response

def story(request, story_slug):
    context_dict = {}

    try:
        story = Story.objects.get(slug=story_slug, ended=True)
        story.views = story.views + 1
        story.save()
        context_dict['title']=story.title
        context_dict['text']=story.story_text
        context_dict['creator']=story.creator
        context_dict['views']=story.views
        context_dict['story']=story
    except:
        pass

    return render(request, 'storyteller/story.html', context_dict)

def category(request, category_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_slug)
        context_dict['category_name'] = category.name

        completed_stories = Story.objects.filter(category=category, ended=True)

        context_dict['completed_stories'] = completed_stories

        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'storyteller/category.html', context_dict)

def search(request):
    qTerm = request.GET.get('q')
    context_dict = {}
    result_list = []
    completed_story_list = Story.objects.filter(Q(title__icontains=qTerm), ended=True)
    user_list = User.objects.filter(Q(username__icontains=qTerm))
    ongoing_story_list = Story.objects.filter(Q(title__icontains=qTerm), ended=False)

    context_dict['completed_story_list'] = completed_story_list
    context_dict['ongoing_story_list'] = ongoing_story_list
    context_dict['user_list'] = user_list

    return render(request, 'storyteller/search.html', context_dict)

@login_required
def register_profile(request):
    context_dict = {}
    registered = False
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile_form = UserProfileForm(request.POST, instance=profile)
        except:
            profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
    return render(request, 'registration/profile_registration.html', context_dict)

def profile(request, user_name):
    context_dict = {}
    try:
        user = User.objects.get(username=user_name)
        context_dict['username'] = user
        try:
            contributor_list = Story.objects.filter(contributor=user, ended=True)
            context_dict['contributor_list'] = contributor_list
        except:
            pass
    except:
        pass
    try:
        profile = UserProfile.objects.get(user=user)
        context_dict['profile'] = profile
    except:
        pass
    return render(request, 'storyteller/profile.html', context_dict)


def storyroom(request, storyid):
    try:
        s = Story.objects.get(pk=storyid)
    except:
        return redirect('index')
    if s.ended == True or s.ending == True:
        return redirect('index')
    else:
        return render(request, 'storyteller/room.html', {'storyid': storyid, 'storycategory': s.category.name})

@login_required
def add_story(request):
    context_dict = {}
    if request.method == 'POST':
        story_form = StoryForm(request.POST)
        if story_form.is_valid():
            story = story_form.save(commit = False)
            story.creator = request.user
            story.curr_user = request.user
            story.save()
            return redirect(storyroom, storyid=story.id)
    else:
        story_form = StoryForm()

    return render(request, 'storyteller/add_story.html', {'form': story_form})


@login_required
def rate_story(request):

    story_id = None
    if request.method == 'GET':
        story_id = request.GET['story_id']

    likes = 0
    if story_id:
        story = Story.objects.get(id=story_id, ended=True)

        if story:
            likes = story.rating + 1
            story.rating =  likes
            story.save()

    return HttpResponse(likes)
