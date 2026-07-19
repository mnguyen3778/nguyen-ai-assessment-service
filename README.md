# Nguyen AI Assessment Service

Dedicated AWS Lambda service for Nguyen AI readiness assessment requests.

- Handler: `lambda_function.lambda_handler`
- Runtime: Python 3.14
- Region: `us-east-2`
- Route: `POST /assessment`

## Architecture Overview

The Lambda entry point in `src/lambda_function.py` delegates directly to the
assessment handler in `src/assessment/handler.py`.

Request flow:

1. API Gateway receives `POST /assessment`.
2. Cognito authorizer validates the caller before Lambda invocation.
3. Lambda parses and validates the JSON request body.
4. Valid requests are scored by the deterministic assessment scoring module.
5. Lambda returns an API Gateway proxy response with a JSON body.

The current service has no third-party Python runtime dependencies and does not
call Bedrock, DynamoDB, S3, or other AWS data-plane services.

## Local Testing

Run the full test suite from the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Run a single test module:

```bash
PYTHONPATH=src python3 -m unittest tests.test_handler -v
```

## Lambda Deployment

Create the deployment package:

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

Create the Lambda function:

```bash
aws lambda create-function \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --runtime python3.14 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::<account-id>:role/<lambda-execution-role-name> \
  --zip-file fileb://dist/nguyen-ai-assessment-service.zip
```

Update an existing Lambda function:

```bash
aws lambda update-function-code \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --zip-file fileb://dist/nguyen-ai-assessment-service.zip
```

See `docs/deployment-guide.md` for IAM, API Gateway, Cognito authorizer, and
CORS setup.

## API Contract

### Request

`POST /assessment`

Headers:

```http
Authorization: Bearer <cognito-token>
Content-Type: application/json
```

Body fields:

- `assessmentVersion`: required string. Current supported value:
  `nguyen-ai-readiness-v1`.
- `organization`: required object.
- `respondent`: required object.
- `answers`: required object mapping question IDs to numeric answers, or a list
  of answer entries with `questionId` and numeric `value`.

Example request:

```json
{
  "assessmentVersion": "nguyen-ai-readiness-v1",
  "organization": {
    "name": "Nguyen AI"
  },
  "respondent": {
    "role": "Founder"
  },
  "answers": {
    "future.question.1": 3
  }
}
```

Equivalent list-form answers:

```json
{
  "assessmentVersion": "nguyen-ai-readiness-v1",
  "organization": {
    "name": "Nguyen AI"
  },
  "respondent": {
    "role": "Founder"
  },
  "answers": [
    {
      "questionId": "future.question.1",
      "value": 3
    }
  ]
}
```

### Successful Response

HTTP `200`

```json
{
  "requestId": "1f0e2e4f-8f25-40a3-9f35-f9fdb828c04f",
  "assessmentVersion": "nguyen-ai-readiness-v1",
  "overallScore": 0,
  "readinessLevel": {
    "id": "pending-rubric",
    "label": "Pending Official Rubric",
    "description": "Deterministic scoring is not available until the official Nguyen-AI rubric is provided."
  },
  "categoryScores": [],
  "recommendations": [],
  "modelInvoked": false,
  "persisted": false
}
```

### Validation Error Response

HTTP `400`

```json
{
  "requestId": "d40f08f7-5e70-404b-939b-0ce40349b243",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Assessment request is invalid.",
    "details": [
      {
        "field": "answers",
        "message": "Field is required.",
        "code": "REQUIRED"
      }
    ]
  },
  "modelInvoked": false,
  "persisted": false
}
```
