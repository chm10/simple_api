"""
This Module start the route and start Flask
"""

from flask import Flask, make_response, request
from flask_restx import Api, Resource, fields

from src.users import UsersDAO

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="UserMVC API",
    description="A simple UserMVC API",
)

doc_user = api.namespace("users", description="Users list")
doc_balance = api.namespace("balance", description="How to get balance")
doc_reset = api.namespace("reset", description="Reset list of users")
doc_event = api.namespace("event", description="Activate event")
user = api.model(
    "UsersDAO",
    {
        "id": fields.Integer(required=True, description="The unique identifier"),
        "balance": fields.Integer(required=True, description="The user balance"),
    },
)

event1 = api.model(
    "Operation",
    {
        "type": fields.String(
            required=True,
            default="deposit",
            description="Type of transaction, deposit or withdraw",
        ),
        "destination": fields.Integer(
            required=True, default=1234, description="User id"
        ),
        "amount": fields.Integer(
            required=True, default=15, description="Value to deposit or withdraw"
        ),
    },
)

DAO = UsersDAO()
DAO.create(0, 100)
DAO.create(1, 200)
DAO.create(3, 300)


@doc_user.route("/")
class UsersList(Resource):
    """Shows a list of all users"""

    @doc_user.doc("list_users")
    @doc_user.marshal_list_with(user)
    @classmethod
    def get(cls):
        """List all tasks"""
        return DAO.users, 200


@doc_balance.route("", doc={"params": {"account_id": "An user id"}})
class Balance(Resource):
    """Show the user balance"""

    @doc_balance.doc("show_balance")
    @doc_balance.response(200, "Success")
    @doc_balance.response(404, "User <user_id> does not exist")
    @classmethod
    def get(cls):
        """Get the balance of id"""
        user_id = request.args.get("account_id", None)
        _, user_ = DAO.get(user_id)
        if user_ is None:
            return 0, 404
        return user_.balance, 200


@doc_reset.route("")
class Reset(Resource):
    """Reset  all the data"""

    @doc_reset.doc("reset_data")
    @classmethod
    def post(cls):
        """Reset all data"""
        while len(DAO.users) > 0:
            DAO.users.clear()
        response = make_response("OK", 200)
        response.mimetype = "text/plain"
        return response


@doc_event.route("")
class Event(Resource):
    """Reset  all the data"""

    @doc_event.doc("event_data")
    @doc_event.expect(event1)
    @classmethod
    def post(cls):
        """Execute deposit, withdraw and transfer"""
        post_data = request.get_json()
        response_object = {}
        type_ = post_data.get("type")
        if type_ == "deposit":
            destination = post_data.get("destination")
            amount = post_data.get("amount")
            _, user_ = DAO.get(destination)
            if not user_:
                user_updated = DAO.create(destination, amount)
            else:
                user_updated = DAO.update(user_.id, user_.balance + amount)
            response_object = {
                "destination": {"id": user_updated.id, "balance": user_updated.balance}
            }
            return response_object, 201
        if type_ == "withdraw":
            origin = post_data.get("origin")
            amount = post_data.get("amount")
            _, user_ = DAO.get(origin)
            if not user_:
                return 0, 404
            if user_.balance - amount >= 0:
                user_updated = DAO.update(user_.id, user_.balance - amount)
            else:
                return 0, 404
            response_object = {
                "origin": {"id": user_updated.id, "balance": user_updated.balance}
            }
            return response_object, 201
        if type_ == "transfer":
            origin = post_data.get("origin")
            destination = post_data.get("destination")
            amount = post_data.get("amount")
            _, user1 = DAO.get(origin)
            _, user2 = DAO.get(destination)
            if not user1 or (origin == destination):
                return 0, 404
            if user1.balance - amount >= 0:
                user1 = DAO.update(user1.id, user1.balance - amount)
                if not user2:
                    user2 = DAO.create(destination, amount)
                else:
                    user2 = DAO.update(user2.id, user2.balance + amount)
                response_object = {
                    "origin": {"id": user1.id, "balance": user1.balance},
                    "destination": {"id": user2.id, "balance": user2.balance},
                }
                return response_object, 201
            else:
                return 0, 404
        api.abort(404, f"Invalid type {type} does not exist")


if __name__ == "__main__":
    app.run(debug=True)
