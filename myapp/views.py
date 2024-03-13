from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyModel

def create_view(request):
    # Se o método for POST, processa os dados do formulário
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        MyModel.objects.create(name=name, description=description)
        return redirect('read')
    # Se o método for GET, exibe a página com o formulário de criação
    elif request.method == "GET":
        return render(request, 'myapp/create_template.html')
    # Se o método HTTP não for nem GET nem POST, retorna um erro 405
    else:
        return HttpResponse('Método HTTP não permitido', status=405)

def read_view(request):
    objects = MyModel.objects.all()
    return render(request, 'myapp/templates/myapp/read_template.html', {'objects': objects})

def update_view(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        obj = MyModel.objects.get(pk=pk)
        obj.name = name
        obj.description = description
        obj.save()
        return redirect('read_view')

def delete_view(request, pk):
    if request.method == "POST":
        obj = MyModel.objects.get(pk=pk)
        obj.delete()
        return redirect('read_view')
