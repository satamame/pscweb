from django.shortcuts import render

def scripts(request):
    context = {}
    return render(request, 'scripts/index.html', context)


def convert(request):
    context = {}
    return render(request, 'scripts/convert.html', context)


def label(request):
    script = b''
    uploaded = request.FILES['file']
    for chunk in uploaded.chunks():
        script += chunk
    script = script.decode('utf-8')
    
    lines = script.split('\n')
    
    context = {'lines' : lines}
    return render(request, 'scripts/label.html', context)
