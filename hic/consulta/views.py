from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
# def nueva_consulta(request):
#     form = ConsultaForm()
#     if request.method == 'POST':
#         form = ConsultaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/consultas/listado')
#     context = {
#         'form': form
#     }
#     return render(request, 'consulta/nueva_consulta.html', context=context)
#
# @login_required
# def editar_consulta(request, consulta_id):
#     consulta = Consulta.objects.get(pk=consulta_id)
#     form = ConsultaForm(instance=consulta)
#     if request.method == 'POST':
#         form = ConsultaForm(request.POST, instance=consulta)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/consultas/listado')
#     context = {
#         'form': form
#     }
#     return render(request, 'consulta/editar_consulta.html', context=context)
#
#
# @login_required
# def listado_consultas(request):
#     consultas = Consulta.objects.all().order_by('-id')
#     context = {
#         'consultas': consultas
#     }
#     return render(request, 'consulta/listado_consultas.html', context=context)