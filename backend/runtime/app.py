import os
from chalice import Chalice
from chalice import CognitoUserPoolAuthorizer


app = Chalice(app_name="backend")

authorizer = CognitoUserPoolAuthorizer(
    "UserPool", provider_arns=[os.environ.get("COGNITO_USER_POOL_ARN", "")]
)


@app.route("/", authorizer=authorizer)
def index():
    return {"hello": "world"}
