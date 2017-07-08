
from flask import Flask, request, Response, jsonify, render_template
from functools import wraps
import json
import os
import socket
import _random

# Initialize the Flask application
app = Flask(__name__)
 
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
    net = request.form['net'] #collects user input for type of network they selected
    note = request.form['note'] # collects user input in textbox
    malware = request.files["file"].read()
    file = open('malware.exe','w') #overwrites the old file. save it to a folder.
    file.write(malware)
    file.close()

    return "project name %s os %s net %s note %s"%(projectname,os,net,note)

def clone(os,projectname): #combine with network
    os.system('lxterminal', '-e') #starts command prompt #no
    #Create a directory if it does not exist#no need to do this
    if (os.path.isdir(Path + projectname) == False):
        debug("Creating a directory")
        os.system("mkdir " + (Path) + (projectname))
    os.system('lxterminal', '-e') # starts a command prompt (actually a terminal in linux)
    os.system([VBoxManage, 'clonevm' + (os) + '-name ' + (projectname) + '--register'])

def network(projectname, net): #combine with clone
    #project name specified by user required for naming the virtual machine
    #net specified by dropdown box and specifies the virtual machine network configuration
    #quality from 0 - 100 specifying the quality of the display.
    #ip 
    os.system('lxterminal', '-e') #starts command prompt


    #if (net=="inetsim"):
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --intnet1 "inetsim" --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality)
    #elif (net=="vpn"):
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --intnet1 "vpn" --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality)
    #elif (net=="tor"):
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --intnet1 "tor" --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality)
    #elif (net=="direct"):
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' hostonlyif create --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality) #creates host only interface
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --nic1 Host-only --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality) # attaches VM to host-only interface
    #elif (net=="none"):
    #    os.system(VBoxManage, 'modifyvm ' + (projectname) + ' --nic1 none --vrdemulticon on --vrdevideochannel on --vrdevideochannelquality ' + quality)


    
    #The method below reduces potential code by just 'building' the command string required to modify the virtual machine.
    #I don't know which properties in modifyvm i'll need, so this will help make things quicker for me.
    #start with 'modifyvm PROJECTNAME '
    commandString = "modifyvm " + (projectname) + " "
    #this looks fine
    if (net == "inetsim" or net == "vpn" or net == "tor"):
        #if net is equal to either of those above, just put in the value of net next to --intnet1 .
        commandString += "--intnet1 " + net + " "
    elif (net == "direct"): #Should be NAT, fix this.
        #otherwise, add this
        commandString += "--hostonlyif create "
    elif (net == "none"):
        #otherwise, add this
        commandString += "--nic1 none "

    #these are the extra settings that are always added
    #vrde: allow remote desktop connections
    #vrdemulticon: allow simultanious(spelling) connections to same VM (this can allow a group to connect to same VM)
    #vrdeport: specifies the ports that this VM will attempt to bind to. 
    #look up documentation and validate this
    commandString += "--vrde on --vrdemulticon on --vrdeport --vrdeport 5000-5050 --vrdeaddress <IP address>"

    #put the final command into command prompt
    os.system(VBoxManage, commandString);
    
def start(projectname):
    os.system('lxterminal', '-e') # starts a command prompt (actually a terminal in linux)
    os.system([VBoxManage, 'startvm' + (projectname)])

def shutdown(projectname):
    os.system('lxterminal', '-e') # starts a command prompt (actually a terminal in linux)
    os.system([VBoxManage, 'controlvm' + (projectname) + 'poweroff'])


def remote(ip, port):
    #Need the IP of the HOST computer, and the port of the running VM

    #Windows syntax:    mstsc 1.2.3.4:3389
    #Linux syntax:  rdesktop -a 16 -N 1.2.3.4:3389
    

    #...probably...
    os.system(rdesktop, " -a 16 -N " + ip + ":" + port)


#This can only be used after the Virtual Machine has been started.
def getVMPort(vmname):
    #first step in retrieving what port the specified VM is connected to.
    #apparent ouput:
    #VRDE:            enabled (Address 0.0.0.0, Ports 3398, MultiConn: off, ReuseSingleConn: off, Authentication type: null)
    os.system([VBoxManage, "showvminfo " + vmname + "  | grep VRDE:"])

    #this is a guess at what could get the value I need.
    os.system([VBoxManage, "showvminfo " + vmname + "  | grep Ports"])
    #^^^How to return output of this?
    return -1;
    
    
    
