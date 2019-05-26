# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from models import Usuarios,Registro
import json
from dicttoxml import dicttoxml
from django.core import serializers
from datetime import date, datetime
from decorators import user_is_entry_author



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
 


def index(request):
    return render(request, 'home.html', {})

def registro(request):
    if request.method == 'POST':
        r = Registro()
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        carrera = request.POST.get('carrera')
        nocontrol = request.POST.get('nocontrol')
        r.nombre = nombre
        r.correo = correo
        r.carrera = carrera
        r.nocontrol = nocontrol
        r.save()
        return render(request, 'registrado.html',{})
    return render(request, 'registro.html',{})


def login(request):
    
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        if password == 'admin' and username == 'admin':
            request.session['name'] = {"username":username,"admin":True}                            
            return render(request, 'login.html', {"session_var":request.session})
    return render(request, 'login.html', {"session_var":request.session})

def logout(request):
    request.session['name'] = None
    return HttpResponseRedirect('/portal')
    
@user_is_entry_author
def admins(request):
    registros = Registro.objects.filter()
    action = request.GET.get('accion')
    if  action == 'borrar':
        id = request.GET.get("id") 
        Registro.objects.filter(pk=id).delete()

    if action == 'generarpdf':
        id = request.GET.get("idd") 
        reg = Registro.objects.filter(pk=id).first()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="itt.pdf"'        
        doc = canvas.Canvas(response)


        #doc = canvas.Canvas("form.pdf", pagesize=letter)
        doc.setLineWidth(.3)
        doc.setFont('Helvetica', 12)
        

        #-----------------------#
        #      |        |       #
        #      |        |       #
        #-----------------------#

        # cuadro grande
        doc.drawString(300,750 , 'Formato de solicitud de')
        doc.drawString(300,740 , 'mantenimiento correctivo:')
        doc.line(5,790,590,790)
        doc.line(5,700,590,700)
        
        # cuadritos

        doc.line(250,790,250,700)
        doc.line(450,790,450,700)

        # lineas divisorias
        doc.line(5,790,5,700)
        doc.line(590,790,590,700)
        
        #-----------------------#
        #         |             #
        #         |             #
        #-----------------------#

         
        # cuadro grande
        doc.line(5,690,590,690)
        doc.line(5,600,590,600)
        
        # cuadritos
        doc.setFont('Helvetica', 8)
        doc.drawString(30,674 , 'DATOS DE SOLICITANTE:')
        doc.drawString(120,662 , str(reg.nombre))
        doc.drawString(325,674 , 'REGISTRO DE LA SOLICITUD:')
        doc.drawString(350,654 , 'Folio:')
        doc.drawString(325,640 , 'Fecha:')
        doc.drawString(325,620 , 'Ingeniero de soporte asignado:')
        
        doc.drawString(10,662 , 'Nombre de usuario:')
        doc.line(5,670,595,670)
        doc.drawString(10,652 , 'Departamento:')
        doc.line(5,660,300,660)
        doc.drawString(120,652 , str(reg.carrera))
        doc.drawString(10,642 , 'No de control:')
        doc.line(5,650,300,650)
        doc.drawString(120,642 , str(reg.nocontrol))
        doc.drawString(10,632 , 'Nombre del jefe inmediato:')
        doc.line(5,640,300,640)
        doc.drawString(10,622 , 'No de serie del equipo:')
        doc.line(5,630,595,630)
        doc.drawString(10,612 , 'No de inventario del equipo:')
        doc.line(5,620,300,620)
        doc.line(5,610,300,610)
        

        # lineas divisorias
        doc.line(5,690,5,600)
        doc.line(590,690,590,600)
        doc.line(300,690,300,600)


        # cuadro mas grande de abajo
        doc.drawString(200,590 , 'INFORMACION DEL SERVICIO SOLICITADO:')
        doc.line(5,600,590,600)
        doc.line(5,600,5,30)
        doc.line(5,30,590,30)
        doc.line(590,600,590,30)        
        doc.line(5,580,590,580)

        #ilera 1
        
        cx1 = 20
        cy1 = 560
        cx2 = 25
        cy2 = 560

        doc.drawString(35,555 , 'EQUIPO DE COMPUTO:')
        doc.drawString(35,550 , 'no enciende')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)



        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(35,515 , 'EQUIPO DE COMPUTO:')
        doc.drawString(35,509 , 'configurar/instalar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(35,475 , 'EQUIPO DE COMPUTO:')
        doc.drawString(35,470 , 'reubicar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)



        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.line(cx1,cy1,cx2,cy2)
        doc.drawString(35,435 , 'CPU:')
        doc.drawString(35,428 , 'Se reinicia/ esta lento/ ase ruido')
        doc.drawString(35,419 , 'se apaga/ muestra pantalla azul')
        doc.drawString(35,412 , 'No arranca sistema operativo')
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(35,395 , 'IMPRESORA:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(35,355 , 'UNIDAD DE CD:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(35,315 , 'CONTRASENA DE USUARIO:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1 = 20
        cy1 = 80
        cx2 = 25
        cy2 = 80

        doc.drawString(35,80 , 'OTROS:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)
    


        # ilera 2

        cx1 = 220
        cy1 = 560
        cx2 = 225
        cy2 = 560

        doc.drawString(230,555 , 'CARPETAS:')
        doc.drawString(230,550 , 'compartir/ problemas de acceso/permisos:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)

        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,515 , 'INFORMACIO:')
        doc.drawString(230,510 , 'acceso/Recuperar/ respaldar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,475 , 'MONITOR:')
        doc.drawString(230,470 , 'sin senal/con lineas/instable')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,435 , 'TECLADO:')
        doc.drawString(230,430 , 'revicion / limpieza')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,395 , 'MOUSE:')
        doc.drawString(230,390 , 'revicion/ adquisicion')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)

        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,355 , 'DICTAMEN TECNICO:')
        doc.drawString(230,350 , 'baja/ adquisicion')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(230,315 , 'ANTIVIRUS:')
        doc.drawString(230,310 , 'instalar/actualizar/eliminar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)



        # ilera 3

        cx1 = 420
        cy1 = 560
        cx2 = 425
        cy2 = 560

        doc.drawString(430,555 , 'INTERNET:')
        doc.drawString(430,550 , 'sin acceso/ falata/ lento:')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(430,515 , 'INTERNET:')
        doc.drawString(430,510 , 'acceso apagina web')
        doc.drawString(430,505 , 'acceso a sistema SII')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(430,475 , 'DIRECCION IP:')
        doc.drawString(430,470 , 'duplicada/ asignar/configurar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)

        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(430,435 , 'CORREO INSTITUCIONAL ')
        doc.drawString(430,430 , 'ELETRONICO: ')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)


        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(430,395 , 'PORTAL:')
        doc.drawString(430,390 , 'tectijuana.edu.mx')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)
        
        
        cx1
        cy1 -= 40
        cx2
        cy2 -= 40

        doc.drawString(430,355 , 'SOFTWARE:')
        doc.drawString(430,350 , 'instalar/revisar')
        doc.drawString(430,345 , 'configurar/ actualizar')
        doc.line(cx1,cy1,cx2,cy2)
        doc.line(cx1,cy1,cx2-5,cy2-5)
        doc.line(cx1,cy1-5,cx2,cy2-5)
        doc.line(cx1+5,cy1,cx2,cy2-5)




        print "test"
        
        
        doc.save()    
        return response    

    if action == 'generarxml':        
        qs_json = []
        for q in registros:
            qs_json.append({
                "name":q.nombre,
                "nocontrol":q.nocontrol,
                "carrera":q.carrera
            })
        
        xml = dicttoxml(qs_json, custom_root='registros', attr_type=False)
        return HttpResponse(xml, content_type='text/xml')

    return render(request, 'admin.html', {"registros":registros})
