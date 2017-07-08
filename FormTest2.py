
from flask import Flask, request, Response, jsonify, render_template
from functools import wraps
import json, os

# Initialize the Flask application
app = Flask(__name__)

#path to VBoxManage on Windows...will change for Linux
VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

@app.route('/')
def index():
    return "HELLO"
 
@app.route('/webui')
def webui():
    return render_template("webui.html")

 #collects user input from webui form
@app.route('/upload',methods=['POST'])
def incoming():
    projectname = request.form['projectname'] #collects user input for project name
    os = request.form['os'] #collects user input for what type of OS they selected
    clone('os','projectname') # creates clone 
    net = request.form['net'] #collects user input for type of network they selected
    network('projectname' ,'net') #modifies clones network settings
    note = request.form['note'] # collects user input in textbox
    malware = request.files["file"].read() #Fix this! Save the file without reading
    file = open('malware.exe','wb') #Add path so you don't overwrite things. Path should contain projectname
    file.write(malware)
    file.close()

    return "project name %s os %s net %s note %s"%(projectname,os,net,note)

def clone(os,projectname):
    os.system('lxterminal', '-e') #Don't need to open a terminal, just run commands
    #we're assuming that this is a new project. we can ignore checking for directories
    if (os.path.isdir(Path + projectname) == False):
        debug("Creating a directory")
        os.system("mkdir " + (Path) + (projectname))
    os.system('lxterminal', '-e') # Don't need to open terminal again
    os.system([VBoxManage, 'clonevm' + (os) + '-name ' + (projectname) + '--register']) #This has to be a string. 

def network(projectname, net): #combine clone and network function
    os.system('lxterminal', '-e') #STOP IT
    
    if (net == "inetsim" or net == "vpn" or net == "tor"):
        os.system(VBoxManage, Modify + net)
    elif (net=="vpn"):
        os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --intnet1 "vpn" ')
    elif (net=="tor"):
        os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --intnet1 "tor" ')
    elif (net=="direct"):
        os.system(VBoxManage, 'modifyvm ' + (projectname) + ' hostonlyif create') #creates host only interface
        os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --nic1 Host-only ') # attaches VM to host-only interface
    elif (net=="none"):
        os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --nic1 none ')
    
def start(projectname):
    os.system('lxterminal', '-e') # WHY???????????????!??!?!!!
    os.system([VBoxManage, 'startvm' + (projectname)])

def shutdown(projectname): #Dont really need this
    os.system('lxterminal', '-e') # YOU'RE FIRED
    os.system([VBoxManage, 'controlvm' + (projectname) + 'poweroff'])
