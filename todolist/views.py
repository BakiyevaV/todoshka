from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from todolist.models import TodoModel, Category


# Create your views here.
def redirect_view(request):
    return redirect(reverse_lazy('category'))

def category(request):
    model_c = Category
    categories = model_c.objects.all()
    if request.method == 'POST':
        if "Add" in request.POST:
            name = request.POST['name']
            category = model_c(name=name)
            category.save()
            return redirect(reverse_lazy('category'))
        elif "Delete" in request.POST:
            check = request.POST.getlist('check')
            for i in range(len(check)):
                try:
                    categ = model_c.objects.filter(id=int(check[i]))
                    categ.delete()
                except BaseException:
                    return HttpResponse('<h1>Сначала удалите задачи, относящиеся к данной категории</h1>')
    return render(request, 'category.html', {'categories': categories})

def todo(request):
    model_t = TodoModel
    model_c = Category
    todos = model_t.objects.all()
    categories = model_c.objects.all()
    if request.method == 'POST':
        if "Add" in request.POST:
            title = request.POST['description']
            date = str(request.POST['date'])
            category = request.POST['category_select']
            content = title + "--" + date + " " + category
            todo = model_t(title=title, content=content, due_time=date, category=Category.objects.get(name=category))
            todo.save()
            return redirect(reverse_lazy('todo'))
        elif "Delete" in request.POST:
            print('Удалить')
            checked_list = request.POST.getlist('checkedbox')
            print(checked_list)
            for i in range(len(checked_list)):
                todo = model_t.objects.filter(id=int(checked_list[i]))
                todo.delete()

    return render(request, 'todo.html', {'todos': todos, 'categories': categories})

