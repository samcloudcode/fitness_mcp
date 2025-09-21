# Deploy FastAPI to AWS Lambda

Deploy this FastAPI application to AWS Lambda with proper configuration and infrastructure setup.

## Pre-deployment Checklist

1. **Infrastructure Verification**
   - AWS infrastructure setup completed (Infrastructure Team)
   - Lambda function created in target region
   - ECR repository available for container images

2. **Code Requirements**
   - FastAPI application structure validated
   - All dependencies specified in requirements.txt or pyproject.toml
   - Application tested locally

## Code Modifications

### 1. Lambda Handler Setup

**Install Required Package**
```bash
uv add mangum
```

**Configure Entry Point (main.py)**
```python
from mangum import Mangum

# Your existing FastAPI app
app = FastAPI(...)

# Add Lambda handler
handler = Mangum(app)
```

### 2. FastAPI Configuration for Lambda

**Update FastAPI Initialization**
```python
APP_NAME = 'your-repo-name'  # Must match GitHub repository name

app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    docs_url=f'/{APP_NAME}/docs',
    redoc_url=None,
    openapi_url=f'/{APP_NAME}/openapi.json'
)
```

### 3. Router Prefix Updates

**Update All Router Files**
```python
# Change from: APIRouter(prefix="/")
# To:
router = APIRouter(prefix="/your-app-name")
```

**Update Main Router Inclusion**
```python
app.include_router(router1.router, prefix=f"/{APP_NAME}")
```

### 4. File Path Configuration

**Update All File I/O Paths to /tmp**
```python
# Examples:
TEMP_DIR = "/tmp/uploads"
LOG_FILE = "/tmp/app.log"
```

## Infrastructure Configuration

### 1. Create Dockerfile.lambda

```dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY ./ ./

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD [ "src.main.handler" ]
```

**Critical**: The CMD path must match your handler location (e.g., `src.main.handler` for handler in src/main.py)

### 2. GitHub Workflow Configuration

Create `.github/workflows/build-deploy-lambda.yml`:

```yaml
name: Deploy to Lambda

on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning'
      image_tag:
        description: 'Image Tag'
        required: false
        default: 'latest'
        type: string
      environment:
        type: environment
        description: 'Environment to deploy'
        required: true
        default: DEV
      aws_deploy_region:
        type: choice
        description: 'AWS Region to deploy'
        required: true
        default: 'ap-east-1'
        options:
        - ap-east-1
        - ap-southeast-1

jobs:
  build:
    uses: pamam-apps/gh-workflows/.github/workflows/simple-build-python-container-lambda.yml@main
    secrets: inherit
    with:
      image_tag: ${{ inputs.image_tag }}
      environment: ${{ inputs.environment}}

  deploy:
    uses: pamam-apps/gh-workflows/.github/workflows/deploy-lambda-python-container.yml@main
    secrets: inherit
    needs: build
    with:
      image_tag: latest
      aws_deploy_region: ${{ inputs.aws_deploy_region}}
      environment: ${{ inputs.environment}}
```

## Environment Setup

### Configure GitHub Environment

**Create Environment**
```bash
gh api repos/OWNER/REPO-NAME/environments/DEV -X PUT
```

**Set Secrets**
```bash
# AWS credentials (obtain from Infrastructure Team)
gh secret set AWS_ACCESS_KEY_ID --env DEV --body "YOUR_ACCESS_KEY"
gh secret set AWS_SECRET_ACCESS_KEY --env DEV --body "YOUR_SECRET_KEY"
```

**Set Variables**
```bash
# AWS Account ID
gh variable set AWS_ACCOUNT --env DEV --body "442042504661"

# Environment configuration from .env
gh variable set ENV_VARS --env DEV --body "DATABASE_URL=postgresql://...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_RESEARCH_BUCKET=...
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
GOOGLE_API_KEY=...
LOGFIRE_TOKEN=...
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=False"
```

## Deployment Process

### Initial Deployment

1. **Request Infrastructure Setup**
   - Contact Infrastructure Team for ECR repository creation
   - Provide repository name and AWS region

2. **Run GitHub Action**
   - Navigate to Actions → Deploy to Lambda
   - Click "Run workflow"
   - Select environment and region

3. **Handle First Run**
   - Expected: Deploy step fails with Error 254
   - Action: Request Lambda function creation from Infrastructure Team
   - Resolution: Rerun deploy step after function creation

### Validation Gates

```bash
# Pre-deployment checks
ruff check --fix
mypy .
uv run pytest tests/ -v

# Post-deployment verification
curl https://your-api-gateway-url/your-app-name/docs
```

## Troubleshooting

### Common Issues

1. **Handler Not Found**
   - Verify CMD path in Dockerfile.lambda matches actual file structure
   - Ensure handler = Mangum(app) is in the specified file

2. **Missing Prefixes**
   - Check all routers have correct prefix
   - Verify APP_NAME consistency across configuration

3. **File I/O Errors**
   - Ensure all file operations use /tmp directory
   - Check write permissions in Lambda environment

## Success Criteria

- [ ] Lambda handler configured
- [ ] All routes accessible with correct prefixes
- [ ] Swagger UI available at /{APP_NAME}/docs
- [ ] Environment variables properly set
- [ ] Deployment workflow succeeds