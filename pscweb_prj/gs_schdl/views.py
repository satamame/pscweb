from django.shortcuts import render

def prods(request):
    """
    A view function
    Shows index of productions
    """
    return render(request, 'gs_schdl/prods.html')
