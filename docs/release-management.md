# Release Management

## Purpose

This document defines release governance for the Nguyen AI Assessment Service.
GitHub is the source of truth for source code, documentation, tests,
infrastructure definitions, and release history. AWS is the runtime environment
for production workloads. Release ZIP files are deployment artifacts and must be
stored outside Git.

## Repository Boundary

The repository should contain:

- Lambda source code under `src/`.
- Unit tests under `tests/`.
- Enterprise architecture, deployment, and release documentation under `docs/`.
- Dependency manifest in `requirements.txt`.
- Ignore rules and repository metadata.

The repository should not contain:

- `deployment.zip` or other local release ZIP files.
- Python cache directories.
- Local virtual environments.
- IDE configuration.
- Local `.env` files.
- Logs or coverage output.

## Build Process

The release build should start from a clean Git commit. The build operator or
CI job should verify:

1. The working tree is clean except for intentionally generated release output.
2. The target commit has passed unit tests.
3. The package is created from tracked source files.
4. The package places `lambda_function.py` and `assessment/` at the ZIP root.
5. The generated ZIP is archived to S3 before production deployment.

Recommended local validation:

```bash
git status --short
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Packaging

Create the Lambda package from the repository root:

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

`deployment.zip` may be used as a temporary local filename during manual
testing, but the canonical release artifact should use a versioned name.

Recommended release artifact name:

```text
nguyen-ai-assessment-service-<version>-<git-sha>.zip
```

Example:

```text
nguyen-ai-assessment-service-v0.2.0-b66bdc9.zip
```

## Deployment

Deploy only artifacts created from a known Git commit. For manual deployment,
update Lambda code with the approved package:

```bash
aws lambda update-function-code \
  --region us-east-2 \
  --function-name nguyen-ai-assessment-service \
  --zip-file fileb://dist/nguyen-ai-assessment-service.zip
```

After deployment, verify Lambda configuration and run a smoke test through API
Gateway with a valid Cognito token.

Production deployment records should include:

- Git commit SHA.
- Git tag.
- S3 artifact URI.
- Artifact checksum.
- AWS Lambda function name.
- AWS region.
- Deployment timestamp.
- Operator or automation identity.
- Smoke test result.

## Versioning

Use semantic versioning for service releases:

- `MAJOR`: incompatible API or response contract changes.
- `MINOR`: backward-compatible functionality, documentation, or ruleset
  additions.
- `PATCH`: backward-compatible fixes, release process changes, or operational
  corrections.

Assessment methodology versions and service release versions should be tracked
separately. A service release may contain the same assessment version, and a
future service release may support multiple assessment versions.

## Rollback Strategy

Rollback should restore a previously known-good Lambda deployment package.

Recommended rollback steps:

1. Identify the last successful release tag and S3 artifact URI.
2. Confirm the artifact checksum matches the release record.
3. Update Lambda code using the archived ZIP.
4. Verify function configuration.
5. Run the API Gateway smoke test.
6. Record the rollback in release history.

Rollback should not rebuild from source unless the archived artifact is missing
or compromised. Rebuilding can introduce environmental differences and weakens
deployment reproducibility.

## Release Artifact Storage

Release ZIP files belong in an S3 Release Archive bucket, not Git.

Recommended S3 object pattern:

```text
s3://<release-archive-bucket>/nguyen-ai-assessment-service/releases/<version>/<git-sha>/nguyen-ai-assessment-service-<version>-<git-sha>.zip
```

Each release artifact should have:

- Server-side encryption with AWS KMS.
- Bucket versioning enabled.
- Public access blocked.
- Least-privilege write access for release automation.
- Read access limited to deployment automation and release operators.
- Object metadata containing Git SHA, version, build timestamp, and checksum.

## S3 Archive Strategy

The S3 Release Archive should be treated as the deployment artifact system of
record. Recommended controls:

- Enable S3 Versioning.
- Enable default SSE-KMS encryption.
- Enable CloudTrail data events for write and delete operations.
- Use lifecycle policies for non-production artifacts.
- Retain production artifacts according to business and compliance needs.
- Prevent accidental deletion through IAM controls or object lock if required.

Recommended metadata keys:

- `service-name`
- `release-version`
- `git-sha`
- `git-tag`
- `build-timestamp`
- `artifact-sha256`

## Git Tagging Strategy

Create an annotated Git tag for each production release:

```bash
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

The tag should point to the exact commit used to create the release artifact.
The release record should link the Git tag to the S3 artifact URI.

Recommended tag naming:

```text
v<major>.<minor>.<patch>
```

For emergency fixes, use a patch version and document the rollback or hotfix
context in the release notes.

## Governance Rules

- Do not commit release ZIP files.
- Do not deploy artifacts built from uncommitted source changes.
- Do not overwrite an archived production release artifact.
- Do not reuse a version number for a different artifact.
- Do not deploy without a recorded Git SHA and checksum.
- Do not treat GitHub Releases as the production artifact store unless the
  release governance model is explicitly changed.

