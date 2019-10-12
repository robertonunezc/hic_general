from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.

# @login_required
# def nueva_cita(request):
#     form = CitaForm()
#     if request.method == 'POST':
#         form = CitaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/citas/listado')
#     context = {
#         'form': form
#     }
#     return render(request, 'cita/nueva_cita.html', context=context)
#
# @login_required
# def editar_cita(request, cita_id):
#     cita = get_object_or_404(Citas,pk=cita_id)
#     form = CitaForm(instance=cita)
#     msg = None
#     if request.method == 'POST':
#         form = CitaForm(request.POST, instance=cita)
#         if form.is_valid():
#             form.save()
#             msg = "Cita actualizada con éxito"
#
#     context = {
#         'form': form,
#         'msg': msg
#     }
#     return render(request, 'cita/editar_cita.html', context=context)
#
# @login_required
# def listado_citas(request):
#     citas = Citas.objects.all().order_by('-fecha')
#     context = {
#         'citas': citas
#     }
#     return render(request, 'cita/listado_citas.html', context=context)