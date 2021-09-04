import os

from aws_cdk import core as cdk
from aws_cdk import aws_cognito as cognito
from chalice.cdk import Chalice


RUNTIME_SOURCE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), os.pardir, "runtime"
)


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        self.user_pool = self._create_auth_user_pool()
        self.chalice = Chalice(
            self,
            "ChaliceApp",
            source_dir=RUNTIME_SOURCE_DIR,
            stage_config={
                "environment_variables": {
                    "COGNITO_USER_POOL_ARN": self.user_pool.user_pool_arn
                }
            },
        )

    def _create_auth_user_pool(self):
        user_pool = cognito.UserPool(
            self,
            "UserPool",
            self_sign_up_enabled=False,
            password_policy=cognito.PasswordPolicy(min_length=8),
            standard_attributes=cognito.StandardAttributes(
                nickname=cognito.StandardAttribute(required=True)
            ),
        )
        return user_pool
