import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import socketio
import pty
import select
import subprocess
import struct
import fcntl
import termios 
import signal
import docker
import eventlet
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User, Group
from django.conf import settings

sioh = socketio.Server(async_mode="eventlet")

# will be used as global variables
fd2 = None
child_pid = None
# https://docs.python.org/3.10/library/pty.html

from django.forms import ModelForm

from main.models import Container
from main.forms import ContainerForm  


@login_required
def home(request):
    #if request.user.is_authenticated:
    return render(request,'main/home.html')
    #else:
     #   return render (request,'registration/sign_up.html')

@login_required
def host_terminal(request):
    return render(request,'main/host_terminal.html')

@login_required
def containers(request):
	client = docker.from_env()
	return render(request, 'main/containers_index.html',{'containers':client.containers.list(all=True),'info':client.info()})

@login_required
def console(request,id):
	client = docker.from_env()
	container = client.containers.get(id)
	return render(request,'main/console.html',{'id':id, 'container':container})

@login_required
def lessons_list(request):
    client = docker.from_env()
    return render(request,'main/lessons_list.html',{'containers':client.containers.list(all=True),'info':client.info()})

@login_required
def lessons(request,id):
    client = docker.from_env()
    container = client.containers.get(id)
    return render(request,'main/lessons.html',{'id':id, 'container':container})

def read_and_forward_pty_output():
    max_read_bytes = 1024 * 20
    while True:
        sioh.sleep(0)
        timeout_sec = 0
        (data_ready, _, _) = select.select([fd2], [], [], timeout_sec)
        if data_ready:
            output = os.read(fd2, max_read_bytes).decode()
            sioh.emit("pty_output", {"output": output})
       
@sioh.event
def resize(sid, message):   
    if fd2:
        set_winsize(fd2, message["rows"], message["cols"])

@sioh.event
def pty_input(sid, message):
    os.write(fd2, message["input"].encode())

@sioh.event
def disconnect_request(sid):
    sioh.disconnect(sid)

@sioh.event
def connect(sid, environ):
    global fd2
    global child_pid

    if child_pid:
        # already started child process, don't start another
        # write a new line so that when a client refresh the shell prompt is printed
        os.write(fd2, "\n".encode())
        return
    else:
        pass
    # create child process attached to a pty we can read from and write to
    (child_pid, fd2) = pty.fork()
    print("The Process ID for the Current process is: " + str(os.getpid()))
    print("The Process ID for the Child process is: " + str(child_pid))
    print("The Process ID for the fd2 is: " + str(fd2))
    # https://www.tutorialspoint.com/pseudo-terminal-utilities-in-python
    
    if child_pid == 0:
        # this is the child process fork.
        # anything printed here will show up in the pty, including the output
        # of this subprocess
        subprocess.run('bash')

    else:
        # this is the parent process fork.
        sioh.start_background_task(target=read_and_forward_pty_output)

@sioh.event
def disconnect(sid):

    global fd2
    global child_pid

    # kill pty process
    os.kill(child_pid,signal.SIGKILL)
    os.wait()

    # reset the variables
    fd2 = None
    child_pid = None
    print('Client disconnected')

@sioh.event
def start_console(sid,message):
	client = docker.APIClient()
	# check if container is running
	if client.containers(all=True,filters={'id':message["Id"]})[0]["State"] != "running":
		sioh.disconnect(sid)
		return

	socket = client.attach_socket(message["Id"], params={'stdin': 1, 'stream': 1,'stdout':1,'stderr':1})
	
	# save socket object to session	
	sioh.save_session(sid, {'socket': socket,"id":message["Id"]})

	sioh.start_background_task(target=read_and_forward_output_container(sid))

@sioh.event
def disconnect_request_container(sid):
	sioh.disconnect(sid)

@sioh.event
def connect2(sid, environ):
	pass

@sioh.event
def disconnect_container(sid):
	print('Client disconnected')    

@sioh.event
def pty_input_container(sid, message):
	# get socket object 
	socket = sioh.get_session(sid)['socket']
	socket._sock.send(message["input"].encode())    

def read_and_forward_output_container(sid):
	# get socket object
	socket = sioh.get_session(sid)['socket']
	while True:
		sioh.sleep(0)
		timeout_sec = 0
		(data_ready, _, _) = select.select([socket], [], [], timeout_sec)
		if data_ready:
			output = socket._sock.recv(1024)

			# check if client disconnected
			if output == b'':
				sioh.disconnect(sid)
				return 

			# decode("cp437") ; to decode vim's output
			sioh.emit("pty_output_container", {"output": output.decode("cp437")},room=sid)

@sioh.event
def resize_container(sid, message): 
	client = docker.APIClient()
	id = sioh.get_session(sid)['id']
	client.resize(container=id, height=int(message["rows"]), width=int(message["cols"]))

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required
def my_containers(request, template_name='main/my_containers.html'):
    container = Container.objects.all()
    return render(request, template_name, {'object_list':container.filter(student=request.user)})

@login_required
def students_containers(request, template_name='main/students_containers.html'):
    container = Container.objects.all()
    return render(request, template_name, {'object_list':container})

def students_containers_view(request, pk, template_name='main/students_containers_detail.html'):
    container= get_object_or_404(Container, pk=pk)    
    return render(request, template_name, {'object':container})

def students_containers_create(request, template_name='main/students_containers_form.html'):
    form = ContainerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('students_containers')
    return render(request, template_name, {'form':form})

def students_containers_update(request, pk, template_name='main/students_containers_form.html'):
    container= get_object_or_404(Container, pk=pk)
    form = ContainerForm(request.POST or None, instance=container)
    if form.is_valid():
        form.save()
        return redirect('students_containers')
    return render(request, template_name, {'form':form})

def students_containers_delete(request, pk, template_name='main/students_containers_delete.html'):
    container= get_object_or_404(Container, pk=pk)    
    if request.method=='POST':
        container.delete()
        return redirect('students_containers')
    return render(request, template_name, {'object':container})

from main.models import Containers_id
import re

def containers_id(request):
    client = docker.from_env()
    container_id_raw = client.containers.list(all=True)
    container_id = container_id_raw
    for ids in range(len(container_id)):
        the_container_id_raw = container_id[ids]
        the_container_id = str(the_container_id_raw).replace("<Container: ", "").replace(">", "")
        idss = Containers_id()
        idss.cid = the_container_id
        idss.save()
        print(the_container_id)
    print(container_id)    
    return render(request, 'main/id.html',{})
