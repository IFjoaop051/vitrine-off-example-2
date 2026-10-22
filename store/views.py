from django.shortcuts import render

# Create your views here.

def render_index(req):
  return render(req, "index.html")
