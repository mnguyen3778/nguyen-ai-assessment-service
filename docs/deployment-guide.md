# Deployment Guide

This repository deploys as a dedicated AWS Lambda assessment service.

- Lambda handler: `lambda_function.lambda_handler`
- Runtime: Python 3.14
- Region: `us-east-2`
- Package root: contents of `src/`

The Lambda deployment archive must place `lambda_function.py` and the
`assessment/` package at the zip root:

```text
lambda_function.py
assessment/
  __init__.py
  config.py
  handler.py
  models.py
  schema.py
  scoring.py
  validation.py
```

## IAM Role Requirements

Create an execution role for the Lambda function with:

- Trust policy allowing `lambda.amazonaws.com` to assume the role.
- CloudWatch Logs permissions, usually via the AWS managed policy
  `service-role/AWSLambdaBasicExecutionRole`.

The current assessment service does not call Bedrock, DynamoDB, S3, or other
AWS data-plane services. Do not attach those permissions unless future service
behavior requires them.

## Deployment Package Creation

From the repository root:

```bash
rm -rf build dist
mkdir -p build/lambda-package dist

python3.14 -m pip install -r requirements.txt -t build/lambda-package
cp src/lambda_function.py build/lambda-package/
cp -R src/assessment build/lambda-package/

find build/lambda-package -type d -name '__pycache__' -prune -exec rm -rf {} +
find build/lambda-package -type d -name '.pytest_cache' -prune -exec rm -rf {} +
find build/lambda-package -name '*.py[cod]' -delete

cd build/lambda-package
zip -r ../../dist/nguyen-ai-assessment-service.zip .
cd ../..
```

`requirements.txt` intentionally contains no third-party dependencies today, so
the pip install step is a no-op unless a future production dependency is added.

## Lambda Creation Steps

Create the function:

```bash
aws lambda create-function \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --runtime python3.14 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::<account-id>:role/<lambda-execution-role-name> \
  --zip-file fileb://dist/nguyen-ai-assessment-service.zip
```

Update an existing function:

```bash
aws lambda update-function-code \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --zip-file fileb://dist/nguyen-ai-assessment-service.zip
```

Confirm the configured handler and runtime:

```bash
aws lambda get-function-configuration \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --query '{Runtime:Runtime,Handler:Handler,State:State,LastUpdateStatus:LastUpdateStatus}'
```

## API Gateway Integration

Create an HTTP API or REST API in `us-east-2` with a protected assessment route:

- Method: `POST`
- Path: `/assessment`
- Integration type: Lambda proxy integration
- Lambda function: `nguyen-ai-assessment-service`
- Payload format version: `2.0` for HTTP API, or proxy integration for REST API

For an HTTP API:

```bash
aws apigatewayv2 create-integration \
  --region us-east-2 \
  --api-id <api-id> \
  --integration-type AWS_PROXY \
  --integration-uri arn:aws:lambda:us-east-2:<account-id>:function:nguyen-ai-assessment-service \
  --payload-format-version 2.0
```

Add a `POST /assessment` route using the integration ID returned by the command:

```bash
aws apigatewayv2 create-route \
  --region us-east-2 \
  --api-id <api-id> \
  --route-key 'POST /assessment' \
  --target integrations/<integration-id>
```

Allow API Gateway to invoke the Lambda function:

```bash
aws lambda add-permission \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --statement-id allow-api-gateway-assessment \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn 'arn:aws:execute-api:us-east-2:<account-id>:<api-id>/*/POST/assessment'
```

## Cognito Authorizer Attachment

Attach a Cognito user-pool authorizer to `POST /assessment`.

For HTTP API JWT authorization:

```bash
aws apigatewayv2 create-authorizer \
  --region us-east-2 \
  --api-id <api-id> \
  --authorizer-type JWT \
  --name nguyen-ai-cognito-authorizer \
  --identity-source '$request.header.Authorization' \
  --jwt-configuration Audience=<app-client-id>,Issuer=https://cognito-idp.us-east-2.amazonaws.com/<user-pool-id>
```

Then update the route:

```bash
aws apigatewayv2 update-route \
  --region us-east-2 \
  --api-id <api-id> \
  --route-id <route-id> \
  --authorization-type JWT \
  --authorizer-id <authorizer-id>
```

Clients should send:

```http
Authorization: Bearer <cognito-id-token-or-access-token>
```

Use the token type expected by the configured authorizer audience and issuer.

## CORS Configuration

Configure CORS at API Gateway so browser clients can call the assessment route.
Use the exact production origin instead of `*` when credentials or
authorization headers are used.

Recommended HTTP API CORS settings:

- Allowed origins: production web app origin, such as `https://app.example.com`
- Allowed methods: `POST`, `OPTIONS`
- Allowed headers: `Authorization`, `Content-Type`
- Exposed headers: none required
- Max age: `300`

Example:

```bash
aws apigatewayv2 update-api \
  --region us-east-2 \
  --api-id <api-id> \
  --cors-configuration AllowOrigins=https://app.example.com,AllowMethods=POST,OPTIONS,AllowHeaders=Authorization,Content-Type,MaxAge=300
```

## Post-Deployment Smoke Test

After deployment, invoke the API with a valid Cognito bearer token:

```bash
curl -i \
  -X POST 'https://<api-id>.execute-api.us-east-2.amazonaws.com/assessment' \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "assessmentVersion": "nguyen-ai-readiness-v1",
    "organization": {"name": "Nguyen AI"},
    "respondent": {"role": "Founder"},
    "answers": {"future.question.1": 3}
  }'
```

Expected result: HTTP `200` with a JSON assessment response, or HTTP `400` with
a structured validation error for invalid request bodies.
