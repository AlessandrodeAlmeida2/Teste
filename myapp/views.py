from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import MyModel
from supabase import create_client, Client
import os
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from dotenv import load_dotenv
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Cadastrar um novo usuário
def sign_up(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            result = supabase.auth.sign_up({"email": email, "password": password})
            print('Usuário cadastrado com sucesso:', result.data)
        except Exception as e:
            print('Erro ao cadastrar:', str(e))
        return redirect('create')

# Autenticar um usuário
# Autenticar um usuário
def sign_in(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        session = supabase.auth.sign_in_with_password({"email": email, "password": password})
        print(session.user)

        # Get the Django user model
        User = get_user_model()

        # Try to get the Django user corresponding to the Supabase user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If the Django user does not exist, create it
            user = User.objects.create_user(email, password)

        # Log in the Django user
        django_login(request, user)

        return redirect('create')

# Desconectar um usuário
def sign_out(request):
    result = supabase.auth.sign_out()
    return redirect('read')

def create_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Criar um novo registro na tabela
        data = {'name': name, 'description': description}
        result = supabase.table('tabela1').insert([data]).execute()

        # Redirecionar para a página de upload de foto
        return redirect('read')
    elif request.method == "GET":
        return render(request, 'myapp/create_template.html')
    else:
        return HttpResponse('Método HTTP não permitido', status=405)


def upload_photo(request, pk):
    if request.method == "POST":
        photo = request.FILES['photo'] if 'photo' in request.FILES else None

        if photo:
            # Fazer o upload de um arquivo para o bucket existente
            bucket = 'PI_Bucket'
            path = f'{photo.name}'
            file = photo.read()
            result = supabase.storage.from_(bucket).upload(file=file, path=path)

            if result.error:
                print('Erro ao fazer upload do arquivo:', result.error.message)
            else:
                print('Arquivo enviado com sucesso:', result.data)

                # Atualizar o campo photo_url na tabela1
                photo_url = f'{bucket}/{path}'  # Substitua isso pela URL real da foto
                data = {'photo_url': photo_url}
                result = supabase.table('tabela1').update(data).eq('id', pk).execute()

        return render(request, 'myapp/upload_template.html')
    else:
        return HttpResponse('Método HTTP não permitido', status=405)

def read_view(request):
    # Obter todos os registros da tabela
    result = supabase.table('tabela1').select("*").execute()
    objects = result.data if result.data else []
    return render(request, 'myapp/read_template.html', {'objects': objects})

def update_view(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Update the record in Supabase
        
        supabase.table('countries').update({'name': name, 'description': description}).eq('id', pk).execute()

        # Fetch the updated record
        obj = supabase.table('tabela1').select().eq('id', pk).execute()

    else:
        # Fetch the current record for GET request
        obj = supabase.table('tabela1').select().eq('id', pk).execute()

    return render(request, 'myapp/update_template.html', {'object': obj})


def delete_view(request, pk):
    if request.method == "POST":
        # Excluir um registro da tabela
        result = supabase.table('tabela1').delete().eq('id', pk).execute()

        return redirect('read')

