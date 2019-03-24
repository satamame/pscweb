from django.shortcuts import render

def scripts(request):
    context = {}
    return render(request, 'scripts/index.html', context)


def convert(request):
    context = {}
    return render(request, 'scripts/convert.html', context)
