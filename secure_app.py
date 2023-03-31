from flask import Flask, request, jsonify
from peewee import *
import bcrypt
import jwt
from os import environ

db = SqliteDatabase("primary.db")
JWT_PASS = environ.get("JWT_PASS")

app = Flask(__name__)


class User(Model):
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=200)

    class Meta:
        database = db


class PaymentCard(Model):
    card_number = CharField(max_length=255, unique=True)
    expiration = IntegerField()
    cvv = IntegerField()
    user = ForeignKeyField(User, backref="cards")

    class Meta:
        database = db


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    if "email" in data and "password" in data:
        new_user = User(
            email=data.get("email"),
            password=bcrypt.hashpw(data.get("password").encode(), bcrypt.gensalt(12)),
        )
        new_user.save()
        return jsonify(
            {
                "success": True,
                "error": False,
                "message": "User '{}' created".format(data.get('email')),
            }
        )
    else:
        return jsonify(
            {
                "success": False,
                "error": True,
                "message": "Mandatory parameters 'email' and 'password' not present for user signup",
            },
            400,
        )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if "email" in data and "password" in data:
        try:
            ref_user = User.get(User.email == data.get('email'))
            if bcrypt.checkpw(data.get('password').encode(), ref_user.password.encode()):
                token = jwt.encode({"user": data.get('email')}, JWT_PASS, algorithm="HS256")
                return jsonify(
                    {
                        "success": True,
                        "error": False,
                        "message": "Successfully Authenticated user",
                        "data": {"token": token.decode()},
                    }
                )
            else:
                return jsonify(
                    {"success": False, "error": True, "message": "Invalid credentials"},
                    401,
                )
        except DoesNotExist:
            return jsonify(
                {
                    "success": False,
                    "error": True,
                    "message": "Unable to find user with email {}".format(data.get('email')),
                },
                404,
            )
    else:
        return jsonify(
            {
                "success": False,
                "error": True,
                "message": "Mandatory parameters 'email' and 'password' not present for user signup",
            },
            400,
        )


@app.route("/create-card", methods=["POST"])
def create_card():
    data = request.get_json()
    if "card_num" in data and "cvv" in data and "exp" in data:
        if request.headers.get("Authorization"):
            validate_token = jwt.decode(
                request.headers.get("Authorization"), JWT_PASS, algorithms=["HS256"]
            )
            if validate_token:
                try:
                    ref_user = User.get(User.email == validate_token.get("user"))
                    new_card = PaymentCard(
                        card_number=data.get('card_num'),
                        expiration=data.get('exp'),
                        cvv=data.get('cvv'),
                        user=ref_user,
                    )
                    new_card.save()
                    return jsonify(
                        {
                            "success": True,
                            "error": False,
                            "message": "Card successfully created for user",
                        }
                    )
                except DoesNotExist:
                    return jsonify(
                        {
                            "success": False,
                            "error": True,
                            "message": "Unable to find user with email {}".format(
                                data.email
                            ),
                        },
                        404,
                    )
            else:
                return jsonify(
                    {"success": False, "error": True, "message": "Invalid credentials"},
                    403,
                )
        else:
            return jsonify(
                {
                    "success": False,
                    "error": True,
                    "message": "No Authorization Header found",
                },
                400,
            )
    else:
        return jsonify(
            {
                "success": False,
                "error": True,
                "message": "Mandatory values for 'card_num', 'cvv' and 'exp' not in request",
            },
            400,
        )


@app.route("/get-cards/<email>", methods=["GET"])
def get_cards(email):
    if email:
        validate_token = jwt.decode(
            request.headers.get("Authorization"), JWT_PASS, algorithms=["HS256"]
        )
        if validate_token:
            card_ds = []
            ref_cards = PaymentCard.select().join(User).where(User.email == validate_token.get('user'))
            for card in ref_cards:
                card_dict = {
                    "card_number": card.card_number,
                    "cvv": card.cvv,
                    "expiration": card.expiration,
                }
                card_ds.append(card_dict)
            return jsonify({"success": True, "error": False, "data": card_ds})
        else:
            return jsonify(
                {"success": False, "error": True, "message": "Invalid credentials"},
                403,
            )
    else:
        return jsonify(
            {
                "success": False,
                "error": True,
                "message": "Mandatory values for 'email' not in request",
            },
            400,
        )

@app.route("/get-card/<card_id>", methods=["GET"])
def get_card(card_id):
    if card_id:
        validate_token = jwt.decode(
            request.headers.get("Authorization"), JWT_PASS, algorithms=["HS256"]
        )
        if validate_token:
            try:
                ref_user = User.get(User.email == validate_token.get('user'))
                ref_card = PaymentCard.get(PaymentCard.id == int(card_id), PaymentCard.user == ref_user)
                return jsonify(
                    {
                        "success": True,
                        "error": False,
                        "data": {
                            "id": ref_card.id,
                            "card_number": ref_card.card_number,
                            "expiration": ref_card.expiration,
                            "cvv": ref_card.cvv,
                        },
                    }
                )
            except DoesNotExist:
                return jsonify(
                    {
                        "success": False,
                        "error": True,
                        "message": "Unable to find card number",
                    },
                    404,
                )
        else:
            return jsonify(
                {"success": False, "error": True, "message": "Invalid credentials"},
                403,
            )
    else:
        return jsonify(
            {
                "success": False,
                "error": True,
                "message": "Mandatory params not present",
            },
            404,
        )

if __name__ == "__main__":
    db.create_tables([User, PaymentCard], safe=True)
    app.run(debug=True)

