from flask import Flask, render_template, request, redirect, jsonify
import requests
import sys, traceback

##### directory structure - 
##/root/project/viewtask.py
##/root/project/templates/base.html
##/root/project/templates/viewtask.html

###dependencies installed
### yum install -y tree python3 python3-pip
### pip3 install flask requests


app = Flask(__name__)

@app.route('/', methods=['GET']) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
def index(): #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    print(" HTTP GET REQUEST FROM pub-alb for health check ON viewtask PRIVATE IP - {0}".format(request.method)) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH
    return(jsonify({'status':'HEALTH CHECK FROM PUB-ALB'})) #### ONLY APPLICABLE FOR PUB-ALB HEALTHCHECK PATH

@app.route('/viewtask', methods=['GET'])  #REDIRECT REQUESTS FROM /ADDTASK,/DELETETASK/ID, /UPDATETASK/ID

def viewtask():

    try:
        r = requests.get('http://dns-name-of-priv-alb:80/dbtask', params ={'service':'viewtask'})
        resp = r.json() #convert server's json response into python dict()
        print("RECEIVED JSON RESPONSE FROM DBTASK- {0} ".format(resp))

        if len(resp['cursor']) != 0:
            print("TASKS EXISTS IN TODO TABLE")
            print("VALUE OF CURSOR SENT BY DBTASK - {0} AND IT'S DATA TYPE IS - {1}".format(resp['cursor'], type(resp['cursor'])))
            return render_template('viewtask.html', cursor = resp['cursor'] )

        elif len(resp['cursor']) == 0:
            print("TASKS DON'T EXISTS IN TODO TABLE REDIRECTING YOU TO /ADDTASK")
            return redirect('http://dns-name-of-pub-alb:80/addtask')  ##### user has added no tasks therefore redirect him to addtask service, ALWAYS USE PUB IP WITH REDIRECT('')

        elif len(resp['cursor']) == 0 and resp['status'] == 'exception':
            print("EXCEPTION OCCURED IN VIEW OF DBTASK")
            return render_template('viewtask.html', cursor = resp['cursor'] )

    except Exception:
        print("EXCEPTION OCCURED IN /VIEWTASK SERVICE:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)
        return jsonify({'status':'EXCEPTION OCCURED IN /VIEWTASK SERVICE'})
                

    

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port='5000', debug=True)
