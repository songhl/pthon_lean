import sys
from main import app

def work(debug=False):
    global app
        
    app.run(host='0.0.0.0',port=5000,debug=True)
        
if __name__=="__main__":

    work(True)
