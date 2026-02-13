# Deployment Guide

This guide covers deploying the AI Appointment Chatbot to various cloud platforms.

## Prerequisites

- Docker and Docker Compose installed
- Git repository with your code
- OpenAI API key
- Cloud provider account (AWS, GCP, Azure, or similar)

---

## Option 1: Docker Compose (Simple)

Best for: Small-scale deployments, testing, single-server setups

### Steps

1. **Clone repository on server:**
```bash
git clone <your-repo-url>
cd ai-appointment-chatbot
```

2. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Edit with your production values
```

3. **Start services:**
```bash
docker-compose up -d
```

4. **Set up reverse proxy (Nginx):**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:4000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable HTTPS with Let's Encrypt:**
```bash
sudo certbot --nginx -d your-domain.com
```

---

## Option 2: AWS Deployment

### Architecture
- **Frontend**: S3 + CloudFront or ECS
- **Backend**: ECS Fargate
- **AI Service**: ECS Fargate
- **Database**: RDS PostgreSQL
- **Load Balancer**: ALB

### Steps

#### 1. Database (RDS)
```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier ai-chatbot-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 20
```

#### 2. Build and Push Docker Images
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t ai-chatbot-backend .
docker tag ai-chatbot-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest

# Build and push AI service
cd ../ai-service
docker build -t ai-chatbot-ai .
docker tag ai-chatbot-ai:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-ai:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-ai:latest
```

#### 3. ECS Task Definitions
Create task definitions for backend and AI service in ECS console or using AWS CLI.

#### 4. Frontend (S3 + CloudFront)
```bash
cd frontend
npm run build
aws s3 sync out/ s3://your-bucket-name

# Create CloudFront distribution pointing to S3 bucket
```

---

## Option 3: Google Cloud Platform

### Architecture
- **Frontend**: Cloud Run
- **Backend**: Cloud Run
- **AI Service**: Cloud Run
- **Database**: Cloud SQL (PostgreSQL)

### Steps

#### 1. Create Cloud SQL Instance
```bash
gcloud sql instances create ai-chatbot-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=us-central1
```

#### 2. Deploy Services to Cloud Run
```bash
# Backend
cd backend
gcloud run deploy ai-chatbot-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# AI Service
cd ../ai-service
gcloud run deploy ai-chatbot-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Frontend
cd ../frontend
gcloud run deploy ai-chatbot-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 4: Azure

### Architecture
- **Frontend**: Azure Static Web Apps
- **Backend**: Azure Container Apps
- **AI Service**: Azure Container Apps
- **Database**: Azure Database for PostgreSQL

### Steps

#### 1. Create PostgreSQL Database
```bash
az postgres flexible-server create \
  --resource-group myResourceGroup \
  --name ai-chatbot-db \
  --location eastus \
  --admin-user admin \
  --admin-password <password>
```

#### 2. Deploy Container Apps
```bash
# Backend
az containerapp create \
  --name ai-chatbot-backend \
  --resource-group myResourceGroup \
  --image <registry>/ai-chatbot-backend:latest \
  --environment myEnvironment

# AI Service
az containerapp create \
  --name ai-chatbot-ai \
  --resource-group myResourceGroup \
  --image <registry>/ai-chatbot-ai:latest \
  --environment myEnvironment
```

---

## Environment Variables for Production

### Backend
```env
NODE_ENV=production
PORT=4000
DATABASE_URL=<production-database-url>
JWT_SECRET=<secure-random-string>
AI_SERVICE_URL=<ai-service-url>
FRONTEND_URL=<frontend-url>
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=100
```

### AI Service
```env
OPENAI_API_KEY=<your-openai-key>
DATABASE_URL=<production-database-url>
```

### Frontend
```env
NEXT_PUBLIC_API_URL=<backend-api-url>
```

---

## Database Migration

Run database migrations on production:

```bash
# Connect to production database
psql <production-database-url>

# Run schema
\i database/schema.sql

# Optionally run seed data (for demo)
\i database/seed_data.sql
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong JWT secret
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Enable database encryption
- [ ] Use environment-specific API keys
- [ ] Set up monitoring and logging
- [ ] Enable rate limiting
- [ ] Use secure headers (Helmet.js)
- [ ] Regular security updates

---

## Monitoring

### Health Check Endpoints
- Backend: `GET /health`
- AI Service: `GET /health`

### Recommended Tools
- **Logging**: CloudWatch, Stackdriver, Azure Monitor
- **Monitoring**: Prometheus + Grafana
- **Error Tracking**: Sentry
- **Uptime Monitoring**: UptimeRobot, Pingdom

---

## Scaling Considerations

### Horizontal Scaling
- Backend and AI service are stateless (easy to scale)
- Use load balancers
- Database connection pooling

### Caching
- Redis for session storage
- Cache frequently accessed data
- CDN for static assets

### Database Optimization
- Connection pooling
- Read replicas for heavy read operations
- Proper indexing (already in schema)

---

## Backup Strategy

### Database Backups
```bash
# Daily automated backups
pg_dump <database-url> > backup_$(date +%Y%m%d).sql

# Restore from backup
psql <database-url> < backup_20240315.sql
```

### Application Data
- Use cloud provider's backup solutions
- Regular snapshot of database
- Version control for code

---

## CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker images
        run: |
          docker build -t backend ./backend
          docker push <registry>/backend:latest
      
      - name: Deploy to production
        run: |
          # Deployment commands
```

---

## Cost Optimization

- Use auto-scaling to match demand
- Choose appropriate instance sizes
- Use spot/preemptible instances where possible
- Set up billing alerts
- Monitor resource usage
- Optimize database queries
