from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
# from .forms import LogIn
import csv

import os
import json


#py2neo
from py2neo import Graph
from py2neo import *

#django views

graph = Graph("https://hobby-jcjeiccfegdkgbkeeehgjnbl.dbs.graphenedb.com:24780/db/data/", auth=('primus', 'b.wCBgsMWWpehr.aRbAJJrj8T1tRJ9d'))



def homepage(request):
    # if request.method == 'POST':
    #     # form = LogIn(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.save()
    #         graphs = Graphs.objects.all()
    #         print(len(graphs))
    #         context= {
    #             'Graphs':graphs,
    #             'printthis':"hello beautiful"}
    #         return render(request,'admin_panel.html',context)

    # else:
    #     # form = LogIn()
    return render(request,'index.html',{'form':'hithere'})

def edit_favorites(request):
    request_list = request.GET.getlist('a[]',None)
    nodes = []
    edges = []
    node = []
    relational_node = {}
    lent = 0
    for counter,i in enumerate(request_list): 
        node.append(i)
        plant = graph.run("Match (n:Plant {name:'"+i+"'})<-[r]-(m) Return n, r,m").data()
        nodes.append({"id": 1000*counter ,"label" : plant[0]['n']['name']})

        for counter2,rel in enumerate(plant):
            lent += len(rel['m'])
            dis_node = rel['m']['name']
            if dis_node in node:
                print("hi")
                print(relational_node[str(dis_node)])
                edges.append({"from":1000*counter, "to":int(relational_node[dis_node])})
                print('{"from":1000*counter, "to":counter*lent + counter2+1}')
            else:
                node.append(dis_node)
                relational_node[dis_node] = str(counter*lent + counter2 +1)
                nodes.append({"id": counter*lent + counter2 +1,"label" : dis_node})
                edges.append({"from":1000*counter, "to":counter*lent + counter2+1})
    print(relational_node.values())
       
    data = {
        'nodes': nodes,
        'edges':edges
    }
    return JsonResponse(data)

