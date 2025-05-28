# 🎵 Video to MP3 Converter Microservices Application

A complete microservices-based application for converting video files to MP3 format with user authentication, file processing, and email notifications.

## 🏗️ Architecture Overview

This application consists of 5 microservices:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Gateway     │────│  Authentication │────│     MySQL       │
│   (API Entry)   │    │    Service      │    │   (Users DB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   RabbitMQ      │────│   Converter     │────│    MongoDB      │
│  (Message Bus)  │    │   Service       │    │ (Files DB)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Notification   │
│   Service       │
└─────────────────┘
```

## 📁 Services

### 🚪 Gateway Service (`/gateway`)
- **Purpose**: API Gateway and entry point for all requests
- **Features**: 
  - User authentication and authorization
  - File upload handling
  - MP3 file download
  - Request routing to other services
- **Tech Stack**: Python Flask, JWT tokens
- **Port**: 8080

### 🔐 Authentication Service (`/auth`) 
- **Purpose**: User management and JWT token generation
- **Features**:
  - User registration and login
  - JWT token creation and validation
  - Password storage and validation
- **Tech Stack**: Python Flask, MySQL, JWT
- **Database**: MySQL (user table)

### 🔄 Converter Service (`/converter`)
- **Purpose**: Video to MP3 conversion processing
- **Features**:
  - Consumes video processing messages from RabbitMQ
  - Converts video files to MP3 using MoviePy
  - Stores converted files in MongoDB GridFS
  - Sends completion notifications via RabbitMQ
- **Tech Stack**: Python, MoviePy, RabbitMQ, MongoDB GridFS

### 📧 Notification Service (`/notification`)
- **Purpose**: Email notifications for completed conversions
- **Features**:
  - Consumes notification messages from RabbitMQ
  - Sends email notifications via Gmail SMTP
  - Notifies users when MP3 conversion is complete
- **Tech Stack**: Python, SMTP, RabbitMQ

### 🐰 RabbitMQ Service (`/rabbit`)
- **Purpose**: Message broker for inter-service communication
- **Features**:
  - Video processing queue
  - MP3 notification queue
  - Persistent message storage
- **Tech Stack**: RabbitMQ with management UI
- **Ports**: 5672 (AMQP), 15672 (Management UI)

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Kubernetes cluster (minikube for local development)
- kubectl configured

### 1. Local Development with Docker
```bash
# Clone the repository
git clone <your-repo-url>
cd microservices_python

# Build and run all services
docker-compose up --build
```

### 2. Kubernetes Deployment
```bash
# Start minikube
minikube start

# Deploy each service
kubectl apply -f auth/manifests/
kubectl apply -f gateway/manifests/
kubectl apply -f converter/manifests/
kubectl apply -f notification/manifests/
kubectl apply -f rabbit/manifests/

# Check deployment status
kubectl get pods
kubectl get services
```

## 📋 API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - User login (returns JWT token)

### File Operations
- `POST /upload` - Upload video file for conversion
- `GET /download?fid=<file_id>` - Download converted MP3 file

## 🔧 Configuration

### Environment Variables

Each service requires specific environment variables:

#### Gateway Service
- `AUTH_SVC_ADDRESS` - Authentication service URL
- `MONGO_HOST` - MongoDB host
- `MONGO_PORT` - MongoDB port

#### Authentication Service  
- `MYSQL_HOST` - MySQL host
- `MYSQL_USER` - MySQL username
- `MYSQL_PASSWORD` - MySQL password
- `MYSQL_DB` - MySQL database name
- `MYSQL_PORT` - MySQL port
- `JWT_SECRET_KEY` - JWT signing secret

#### Converter Service
- `MP3_QUEUE` - RabbitMQ queue for MP3 notifications
- `VIDEO_QUEUE` - RabbitMQ queue for video processing
- `MONGO_HOST` - MongoDB host
- `RABBITMQ_HOST` - RabbitMQ host

#### Notification Service
- `MP3_QUEUE` - RabbitMQ queue for MP3 notifications
- `GMAIL_ADDRESS` - Gmail sender address
- `GMAIL_PASSWORD` - Gmail app password
- `RABBITMQ_HOST` - RabbitMQ host

## 🗄️ Database Schema

### User Table (MySQL)
```sql
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);
```

### Files Storage (MongoDB GridFS)
- **videos**: Original uploaded video files
- **mp3s**: Converted MP3 files

## 🔄 Message Flow

1. User uploads video via Gateway
2. Gateway stores video in MongoDB and sends message to `video` queue
3. Converter service processes video from queue
4. Converter converts video to MP3 and stores in MongoDB
5. Converter sends completion message to `mp3` queue
6. Notification service sends email to user
7. User downloads MP3 via Gateway

## 🛠️ Development

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes in appropriate service directory
3. Update manifests if needed
4. Test locally with Docker
5. Deploy to Kubernetes for integration testing
6. Merge to main branch

### Service Dependencies
- All services depend on MongoDB and RabbitMQ
- Gateway depends on Authentication service
- Converter and Notification services are queue consumers

## 📊 Monitoring

### Health Checks
- Gateway: `http://localhost:8080/health`
- RabbitMQ Management: `http://localhost:15672`
- MongoDB: Check connection via service logs

### Logs
```bash
# View service logs in Kubernetes
kubectl logs -f deployment/gateway
kubectl logs -f deployment/converter
kubectl logs -f deployment/notification
```

## 🔒 Security

- JWT tokens for authentication
- Plain text password storage (⚠️ **Note**: Consider implementing password hashing for production)
- Environment variables for sensitive data
- Kubernetes secrets for production deployment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License. 