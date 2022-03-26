from email.policy import default
from pydoc import describe
from flask import Flask, request, make_response
from flask_restx import Api, Resource, fields
import json
app = Flask(__name__)
api = Api(app, version='1.0', title='UserMVC API',
    description='A simple UserMVC API',
)

doc_user = api.namespace('users', description='Users list')
doc_balance = api.namespace('balance', description="How to get balance")
doc_reset = api.namespace('reset', description="Reset list of users")
doc_event = api.namespace('event', description="Activate event")
user = api.model('UsersDAO', {
    'id': fields.Integer(required=True, description='The unique identifier'),
    'balance': fields.Integer(required=True, description='The user balance')
})

event1 = api.model('Operation', {
    'type': fields.String(required=True,default='deposit', description='Type of transaction, deposit or withdraw'),
    'destination': fields.Integer(required=True, default=1234, description='User id'),
    'amount':fields.Integer(required=True, default=15 , description='Value to deposit or withdraw')
})
class Users:
    def __init__(self, id, balance) -> None:
        self.id = id
        self.balance = balance

class UsersDAO(object):
    def __init__(self) -> None:
        self.users = []
    def create(self, id, balance):
        new_user = Users(id, balance)
        for user in self.users:
            if user.id == new_user.id:
                api.abort(404, 0)
        self.users.append(new_user)
        return self.users[-1]
    def get(self, id):
        for idx,user in enumerate(self.users):
            if user.id == id:
                return idx, self.users[idx]
        return -1, None
    def update(self, id, balance):
        idx, user = self.get(id)
        if user in self.users:
            self.users[idx].balance = balance
        else:
            api.abort(404, 0)
        return self.users[idx]
    def delete(self, id):
        idx, user = self.get(id)
        self.users.remove(idx)

    
        
DAO = UsersDAO()
DAO.create(0, 100)
DAO.create(1, 200)
DAO.create(3, 300)


@doc_user.route('/')
class UsersList(Resource):
    '''Shows a list of all users'''
    @doc_user.doc('list_users')
    @doc_user.marshal_list_with(user)
    def get(self):
        '''List all tasks'''
        return DAO.users, 200
    #@doc_user.doc('create_user')
    #@doc_user.expect(user)
    #@doc_user.marshal_with(user, code=201)
    #def post(self):
    #    '''Create a new task'''
    #    resp = api.payload
    #    return DAO.create(resp['id'], resp['balance']), 201

@doc_balance.route("",doc={'params':{'account_id': 'An user id'}})
class Balance(Resource):
    ''''Show the user balance'''
    @doc_balance.doc('show_balance')
    @doc_balance.response(200, "Success")
    @doc_balance.response(404, "User <user_id> does not exist") 
    def get(self):
        user_id = request.args.get('account_id', None)
        idx, user = DAO.get(user_id)
        if user is None:
            return 0, 404
        return user.balance, 200

@doc_reset.route("")
class Reset(Resource):
    '''Reset  all the data'''
    @doc_reset.doc('reset_data')
    def post(self):
        while len(DAO.users) > 0 :
            DAO.users.clear()
        response = make_response("OK", 200)
        response.mimetype = "text/plain"
        return response

@doc_event.route("")
class Event(Resource):
    '''Reset  all the data'''
    @doc_event.doc('event_data')
    @doc_event.expect(event1)
    def post(self):
        post_data = request.get_json()
        response_object = {}
        type = post_data.get('type')
        if type == 'deposit':
            destination = post_data.get('destination')
            amount = post_data.get('amount')
            idx, user = DAO.get(destination)
            if not user:
                user_updated = DAO.create(destination, amount)
            else:
                user_updated = DAO.update(user.id, user.balance + amount)
            response_object = {"destination":{"id":user_updated.id,"balance":user_updated.balance}}
            return response_object, 201
        elif type == 'withdraw':
            origin = post_data.get('origin')
            amount = post_data.get('amount')
            idx, user = DAO.get(origin)
            if not user:
                return 0, 404
            if user.balance - amount >= 0:
                user_updated = DAO.update(user.id, user.balance - amount)
            else:
                return 0, 404
            response_object = {"origin":{"id":user_updated.id,"balance":user_updated.balance}}
            return response_object, 201
        elif type == 'transfer':
            origin = post_data.get('origin')
            destination = post_data.get('destination')
            amount = post_data.get('amount')
            idx1 ,user1 = DAO.get(origin)
            if not user1:
                return 0, 404
            idx2, user2 = DAO.get(destination)
            if not user2:
                return 0, 404
            if origin == destination:
                return 0, 404
            if  user1.balance - amount >= 0:
                DAO.update(user1.id, user1.balance - amount)
                DAO.update(user2.id, user2.balance + amount)
                response_object = {"origin":{"id":user1.id,"balance":user1.balance},"destination":{"id":user2.id,"balance":user2.balance}}
                return response_object, 201
            else:
                return 0,404     
        else:
            api.abort(404, f"Invalid type {type} does not exist")


if __name__ == '__main__':
    app.run(debug=True)