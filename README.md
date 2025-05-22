# Prompt2Course

Prompt2Course is an AI-powered tool that generates comprehensive, structured courses on any topic of your choice. The application uses OpenAI's API to create detailed learning paths, modules, and resources for learners of all levels.

## Features

- Generate custom courses on any topic
- Specify experience level and time availability
- Save and manage multiple courses
- Subscription tiers with different course limits
- User authentication and account management

## Project Structure

The project follows a modular architecture:

```
prompt2course/
├─ backend/               # FastAPI backend
│  ├─ controllers/        # Business logic controllers
│  ├─ models/             # Data models
│  ├─ routes/             # API routes/endpoints
│  ├─ services/           # External services like OpenAI
│  ├─ middlewares/        # Request/response middleware
│  ├─ utils/              # Utility functions
│  ├─ tests/              # Test files
│  ├─ app.py              # Main application entry point
│  └─ requirements.txt    # Python dependencies
├─ frontend/              # React frontend
│  ├─ public/             # Static public assets
│  ├─ src/                # React source code
│  ├─ package.json        # Node.js dependencies
│  └─ Dockerfile          # Frontend Docker configuration
├─ docker-compose.yml     # Docker Compose configuration
└─ .gitignore             # Git ignore file
```

## Environment Setup

### Backend Environment Variables (.env file)

Create a `.env` file in the backend directory with the following variables:

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
MONGODB_URI=mongodb://mongo:27017/prompt2course
# For local development, use: mongodb://localhost:27017/prompt2course

# Server Configuration
PORT=8000
HOST=0.0.0.0
DEBUG=True

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend URL for CORS
FRONTEND_URL=http://localhost:3000
```

## Installation and Setup

### Using Docker (Recommended)

1. Make sure Docker and Docker Compose are installed on your system
2. Create the `.env` file in the backend directory as described above
3. Run the following command:

```bash
docker-compose up --build
```

This will start the frontend, backend, and MongoDB containers.

### Manual Installation

#### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create the `.env` file as described above

5. Run the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

#### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install the required packages:

```bash
npm install
```

3. Run the development server:

```bash
npm start
```

The frontend will be available at http://localhost:3000

## API Documentation

Once the backend is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

### Backend Tests

Run the tests with pytest:

```bash
cd backend
pytest
```

## Deployment

### Production Considerations

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Use a production-grade web server like Gunicorn
3. Set specific CORS origins instead of allowing all origins
4. Use a proper MongoDB instance with authentication
5. Ensure your OpenAI API key has sufficient quota for production usage

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License. 