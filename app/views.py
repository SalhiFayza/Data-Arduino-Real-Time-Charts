
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
import serial
import random
import datetime


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


#****************
# data realtime serial arduino
def show_graph_com(request, template_name='index.html'):
    return render(request, template_name)
def fetch_sensor_values_ajax_com(request):
    data={}
    if request.is_ajax():
            sensor_data0=[]
            sensor_val=random.random()
            try:
                ser=serial.Serial("COM3",9600)
                ser_bytes = ser.readline().decode().strip().split(',')
                new_ser_bytes = [float(i) for i in ser_bytes]
                now=datetime.now()
                ok_date=str(now.strftime('%Y-%m-%d %H:%M:%S'))
                humidity = new_ser_bytes[0]
                temperature = new_ser_bytes[1]
                WaterTemp =new_ser_bytes[2]
                ph =new_ser_bytes[3]
                if humidity is not None and temperature is not None and WaterTemp is not None and ph is not None:
               
                    sensor_data0.append(str(humidity)+','+ok_date)
                    sensor_data0.append(str(temperature)+','+ok_date)
                    sensor_data0.append(str(WaterTemp)+','+ok_date)
                    sensor_data0.append(str(ph)+','+ok_date)
                    x=sensor_data0
                else:
                    sensor_data0.append(str(sensor_val)+','+ok_date)
            except Exception as e:
                    sensor_data0.append(str(sensor_val)+','+ok_date)
            data['result']=x
    else:
        data['result']='Not Ajax'
    return JsonResponse(data)