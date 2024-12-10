from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb,
    CfnOutput,
    Stack,
    App,
)
from constructs import Construct

class DynamodbLambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create dynamo table
        demo_table = aws_dynamodb.Table(
            self, "VisitorTimeTable",
            partition_key=aws_dynamodb.Attribute(
                name="key",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        my_lambda = _lambda.Function(self, "my_lambda_function",
                                     runtime=_lambda.Runtime.PYTHON_3_8,
                                     handler="main.handler",
                                     code=_lambda.Code.from_asset("./lambda"))

        f = open("version.txt", "r")
        version = f.read() or "0.0"

        my_lambda.add_environment("TABLE_NAME", demo_table.table_name)
        my_lambda.add_environment("VERSION", version )

        my_lambda_url = _lambda.FunctionUrl(
            self, 'MyFunctionUrl',
            function=my_lambda,
            auth_type=_lambda.FunctionUrlAuthType.NONE
        )

        demo_table.grant_read_write_data(my_lambda)

        CfnOutput(
            self, 'FunctionUrlOutput',
            value=my_lambda_url.url
        )

app = App()
Stack(app, "MyStack")
app.synth()
