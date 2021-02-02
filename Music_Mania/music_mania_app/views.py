from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
import requests
from datetime import datetime
from django.http import HttpResponse, Http404,JsonResponse,HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator



# Create your views here.


# class MusicManiaView(ListView):
#     model=Song
#     template_name = 'index.html'
#     # context_object_name = 'song'
#     paginate_by = 4
#     ordering=['id']
#     queryset = Song.objects.all()
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         query = self.request.GET.get('query')
#         if query:
#             context['song'] = Song.objects.filter(Q(title__icontains=query)|Q(description__icontains=query))
#             context['Category'] = Category.objects.all()
#         else:
#             context['song'] = Song.objects.all()
#             context['Category'] = Category.objects.all()

#         return context


class MusicManiaView(TemplateView):    
    template_name = "index.html"
    def get(self, request):
        query = self.request.GET.get('query')
        if query:
            context = {
            'song': Song.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)),
            'Category': Category.objects.all()
            }
        else:
           context = {
            'song': Song.objects.all().order_by('?'),
            'Category': Category.objects.all()
            }    
        # print(Song.objects.filter(Q(title__icontains=query)|Q(description__icontains=query)).query) To get the SQL query
        return self.render_to_response(context) 

    
class MusicManiaCatView(TemplateView):    
    template_name = "index.html"
    def get(self, request,pk):
        get_cat=Category.objects.get(pk=pk)
        query = self.request.GET.get('query')
        if query:
            context = {
            'Category': Category.objects.all(),
            'song': Song.objects.filter(Q(title__icontains=query) & Q(cat=get_cat)),
            }
        else:
            context = {
            'Category': Category.objects.all(),
            'song': Song.objects.filter(cat=get_cat),
            }
        return self.render_to_response(context)

class MusicManiaListenLaterView(TemplateView):
    template_name='watch_later.html'
    # @method_decorator(login_required(login_url='/signup'))
    def post(self, request):
        user = request.user
        music_id = self.request.POST.get('song_id')
        watch_later_songs = Listen_Later(user=user,music_id=music_id)
        watch_later_songs.save()
        
        if watch_later_songs:
            music_id=Listen_Later.objects.values_list('music_id', flat=True)
            print(music_id)
            for i in music_id:
                song=Song.objects.filter(id=i)
            # return self.render_to_response({'Song_added':True})
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')

    @method_decorator(login_required(login_url='/signup'))
    def get(self, request):
        music_user=Listen_Later.objects.filter(user=self.request.user)
        print("user",music_user)
        # music_id=Listen_Later.objects.filter(user=self.request.user).values_list('music_id', flat=True)
        # lis=[]
        # for i in music_id:
        #     lis.append(int(i))
        #     print(lis)
        # song=Song.objects.filter(id__in=lis)
    
        music_id=Listen_Later.objects.filter(user=self.request.user).values('music_id')
        print(music_id)
        song=Song.objects.filter(id__in=music_id)
        print(song)

        return self.render_to_response({'listen_later':song})

class MusicManiaListenRemoveView(TemplateView):
    template_name='watch_later.html'
    def post(self, request):
        user = request.user
        music_id = int(self.request.POST.get('remove_song_id'))
        print(type(music_id))
        
        # watch_later_songs = Watch_Later(user=user,music_id=music_id)
        remove_song=Listen_Later.objects.filter(music_id=music_id)
        remove_song.delete()

        return HttpResponseRedirect('/listen_later')


class MusicManiaAutosuggestSearchView(View):
    def get(self, request):
        get_query_autosuggest = request.GET.get('term')
        queryset=Song.objects.filter(title__icontains=get_query_autosuggest)
        print(queryset)
        my_list=[]
        my_list += [x.title for x in queryset]
        return JsonResponse(my_list,safe=False)

    

        




            






