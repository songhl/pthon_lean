__author__ = 'wangyakun'
#coding:utf8
import functools
from config import authorized_ip_file
from utils import *
from flask import Flask,request
from flask.ext.restful import Api, Resource
from flask_httpauth import HTTPBasicAuth
from flask.ext.restful import reqparse
app = Flask(__name__)
api = Api(app)

from flask import make_response
from flask import url_for
authorized_ips=[val.strip() for val in open(authorized_ip_file).readlines()]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

############################################################3

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'jone':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
##########################################################

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

users = {
    "jone": "python",
    "wyk": "tiger"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

def check_source_ip(func):
    @functools.wraps(func)
    def wrap(*args, **kv):
        ip=request.remote_addr
        if ip not in authorized_ips:
            ret={'code' : 1, 'desc' :'{0} is not authorized'.format(ip), 'data': [] }
        else:
            ret = func(*args, **kv)
        return ret

    return wrap



class MyResource(Resource):
    decorators = [auth.login_required,check_source_ip]
class CheckDb(MyResource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(name='dbAddr', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='dbPort', type = int,ignore=True, case_sensitive=False,trim=True,required=True,location = ('values','args'))
        super(CheckDb, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        try:
            db=DbModel(host=args.dbAddr,port=args.dbPort)
            dbs=db.get_dbs()
            ret={'code' : 0, 'desc' : 'ok', 'data': dbs }
        except Exception,e:
            ret={'code' : 1, 'desc' : str(e), 'data': [] }
        msg={"args":args,"return":ret}
        logger.info(repr(msg))
        return ret

class CheckUser(MyResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(name='dbAddr', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='dbPort', type = int,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='dbName', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='privilege', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        super(CheckUser, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        try:
            db = DbModel(host=args.dbAddr, port=args.dbPort,database=args.dbName,priv=args.privilege)
            is_new,list_user=db.get_users()
            # return {'code' :0, 'desc' : 'ok','is_new':is_new, 'data' :list_user}
            ret= {'code' :0, 'desc' : 'ok','data' :list_user,"is_new":is_new}

        except Exception,e:
            ret= {'code' : 1, 'desc' : str(e), 'data': [],'is_new':0 }
        msg={"args":args,"return":ret}
        logger.info(repr(msg))
        return ret

class CheckReferIp(MyResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(name='dbAddr', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='dbPort', type = int,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='dbName', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='privilege', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        self.reqparse.add_argument(name='userName', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = ('values','args'))
        super(CheckReferIp, self).__init__()
    def get(self):
        args = self.reqparse.parse_args()
        try:
            db = DbModel(host=args.dbAddr, port=args.dbPort, database=args.dbName, priv=args.privilege,dbuser=args.userName)
            list_referip=db.get_referip()
            if list_referip is None:# user not exists
                raise Exception('user %s does not exist'%args.userName)
            ret= {'code' :0, 'desc' : 'ok','data' :list_referip}

        except Exception,e:
            ret= {'code' : 1, 'desc' : str(e),'data': [] }
        msg={"args":args,"return":ret}
        logger.info(repr(msg))
        return ret
class GrantApi(MyResource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(name='submitter', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = 'json')
        self.reqparse.add_argument(name='grantInfo', type = str,ignore=True,case_sensitive=False, trim=True,required=True,location = 'json')
        super(GrantApi, self).__init__()

    def post(self):

        args = self.reqparse.parse_args()

        return args



api.add_resource(CheckDb, '/api/v1.0/checkdb', endpoint = 'checkdb')
api.add_resource(CheckUser, '/api/v1.0/checkuser', endpoint = 'checkuser')
api.add_resource(CheckReferIp, '/api/v1.0/checkreferip', endpoint = 'checkreferip')
# api.add_resource(Grant, '/api/v1.0/grant/<int:task_id>', endpoint = 'grant')
api.add_resource(GrantApi, '/api/v1.0/grant', endpoint = 'grant')


#####################


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
