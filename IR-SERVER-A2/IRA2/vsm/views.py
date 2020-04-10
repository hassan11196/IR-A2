from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import View
from django.middleware.csrf import get_token
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import os
from .helpers import  build_index, get_vector_query
from .models import VectorSpaceModel
from inverted_index.views import DocumentRetreival
FILE_PATH = os.path.dirname(__file__) + '../../data/' + 'Trump Speechs/speech_'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Test(View):
    def get(self, request):
        return JsonResponse({'status':True, 'message':'Server is up'}, status=200)


class Indexer(View):
    def get(self, request):

        return JsonResponse({'status':True, 'message':'Indexer Status'}, status=200)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        options = request.POST
        status = build_index(tf_func = options['tf_func'], idf_func = options['idf_func'], norm_func = options['norm_func'])
        return JsonResponse({'status':status, 'message':'Starting Indexing'}, status=200)

class QueryEngine(View):
    def get(self, request):
        query_options = [
            ('Boolean Query', 0),
            ('Phrasal Query', 1),
            ('Proximity Query', 2)
        ]
        return JsonResponse({'status':True, 'message':'Query Engine Status', 'options':query_options}, status=200)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # try:
        result = []
        print(request.POST)
        if request.POST['query'] == '':
            raise ValueError('Invalid Query')
        
        result = get_vector_query(request.POST['query'], alpha=float(request.POST['alpha']))
        print(type(result))
        print(result)
        if(len(result) == 0):
            raise ValueError('Term not in any Documents.')
        if isinstance(result, set):
            return JsonResponse({'status':True, 'message':'Query Result', 'result':list(result), 'type':'set', 'docs':list(result)}, status=200)
        if isinstance(result, dict):
            
            # res = result.occurrance
            # doc_ids = list(map(lambda pos: pos,result.occurrance.keys()))

            return JsonResponse({'status':True, 'message':'Query Result', 'result':result['occurrance'], 'type':'PostingList', 'docs':result['doc_ids']}, status=200)
        else:
            return JsonResponse({'status':True, 'message':'Something Went Wrong', 'result':list(result), 'type':'Unknown'}, status=200)
            

        # except BaseException as e:
        #     print(e)
        #     return JsonResponse({'status':False, 'message':str(e), 'result' : ''}, status=400)