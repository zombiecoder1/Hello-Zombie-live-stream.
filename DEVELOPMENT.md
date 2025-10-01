# ZombieCoder Development Guide

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.10+
- Git

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd workspace

# Start all services
./start.sh

# Or start specific services
docker-compose up -d postgres redis
docker-compose up -d api-gateway
```

## 🏗️ Architecture

### Core Services
- **API Gateway**: Central routing and authentication
- **Orchestrator**: Agent coordination and task management
- **Auth Service**: User authentication and authorization

### Agents
- **Code Generation**: AI-powered code generation
- **Code Review**: Automated code review and suggestions
- **Documentation**: Auto-documentation generation
- **Testing**: Test generation and execution
- **Deployment**: DevOps automation
- **Bengali NLP**: Bengali language processing

### Frontend
- **Web Portal**: Next.js web application
- **VS Code Extension**: Editor integration
- **Mobile App**: React Native mobile app
- **Shared Components**: Reusable UI components

## 🛠️ Development

### Adding New Services
1. Create service directory in appropriate category
2. Add service configuration to docker-compose.yml
3. Update API Gateway routing
4. Add service documentation

### Testing
```bash
# Run all tests
npm test

# Run specific service tests
cd services/file-indexer
npm test
```

### Monitoring
- **Logs**: Check `monitoring/logs/`
- **Metrics**: Access Grafana dashboard
- **Health**: Check service health endpoints

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `API_GATEWAY_URL`: API Gateway endpoint
- `OLLAMA_URL`: Ollama service endpoint

### Service Configuration
Each service has its own configuration file:
- `config/database.json`: Database settings
- `config/redis.json`: Redis settings
- `config/ollama.json`: Ollama settings

## 📚 Documentation

- **API Docs**: `/docs/api-docs/`
- **User Guides**: `/docs/user-guides/`
- **Developer Guides**: `/docs/developer-guides/`
- **Architecture**: `/docs/architecture/`

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📞 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: `/docs/`
