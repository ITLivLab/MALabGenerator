
from flask import Flask, request, Response, jsonify, render_template
from functools import wraps
import json, os

# Initialize the Flask application
app = Flask(__name__)

#path to VBoxManage on Windows...will change for Linux
VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
#Created Path to where users will have their projects saved (will be changed when path is known)
Path = "C:\Users\Admin\Projects\"
# modifying vm varible to shorten code
Modify = "modifyvm " + " " + (projectname) + " "
ModifyNet = "modifyvm " + " " + (projectname) + " --intnet1 "
Clone = os.system(VBoxManage + " " + ' clonevm ' + " " + (os) + ' -name ' + " " +(projectname) + " "  +' --register')

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
    network('projectname' ,'net') #modifies clones network settings
    note = request.form['note'] # collects user input in textbox
    note.save(Path + projectname + 'note.txt', 'wb')
    malware = request.files["file"] #I fixed it
    malware.save(Path + projectname + 'malware.exe','wb') #added path
    file.write(malware)
    file.close()

    return "project name %s os %s net %s note %s"%(projectname,os,net,note)

def clonevm(os,projectname):
        os.system("mkdir " + (Path) + (projectname)) # creates new directory for project

    if (net == "inetsim" or net == "vpn" or net == "tor"):
        Clone # creates clone
        os.system(VBoxManage + " " + ModifyNet + " " + (net)) # modifies clones network
    elif (net=="direct"):
        Clone # creates clone
        os.system(VBoxManage +  " " + Modify + " " +  ' NAT') #modifies clones network
    elif (net=="none"):
        Clone # create clone
        os.system(VBoxManage + " " + Modify + " " + ' --nic1 none ') # modifies clones network
            
def start(projectname):
    os.system(VBoxManage + " " + 'startvm' +  " " + (projectname))# starts vm

#def shutdown(projectname): #Dont really need this
    #os.system([VBoxManage, 'controlvm' + (projectname) + 'poweroff'])
