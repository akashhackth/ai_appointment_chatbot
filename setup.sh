#!/bin/bash

# AI Appointment Chatbot - Quick Setup Script

set -e

echo "================================================"
echo "AI Appointment Chatbot - Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env and add your OPENAI_API_KEY${NC}"
    echo ""
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
    echo ""
fi

# Start services
echo "Starting services with Docker Compose..."
echo ""

docker-compose up -d

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Services:"
echo "  - Frontend:   http://localhost:3000"
echo "  - Backend:    http://localhost:4000"
echo "  - AI Service: http://localhost:8000"
echo "  - Database:   localhost:5432"
echo ""
echo "Demo credentials:"
echo "  Email:    john.doe@example.com"
echo "  Password: password123"
echo ""
echo "Useful commands:"
echo "  View logs:     docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart:       docker-compose restart"
echo ""
echo -e "${GREEN}✓ All services are starting...${NC}"
echo "Wait a few moments for all services to be ready."
