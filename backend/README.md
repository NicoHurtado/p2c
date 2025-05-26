# Course Generator API

A FastAPI-based backend for generating AI-powered courses with external API integration.

## Features

- 🤖 AI-powered course generation using external API
- 👤 User authentication and authorization
- 📚 Course management (CRUD operations)
- 🔄 External API integration for course generation
- 🎯 Personalized learning experiences

## Project Structure

```
backend/
├── app.py                 # FastAPI application entry point
├── config.py             # Centralized configuration
├── db.py                 # Database connection and initialization
├── schemas.py            # Pydantic models for requests/responses
├── requirements.txt      # Python dependencies
├── models/              # Database models
│   ├── user.py
│   └── course.py
├── routes/              # API route handlers
│   ├── auth.py
│   └── courses.py
├── services/            # External service integrations
│   └── course.py        # External API integration
└── utils/               # Utility functions
    └── auth.py
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```env
   # Database Configuration
   MONGO_URI=mongodb://localhost:27017
   DB_NAME=course_generator

   # Authentication
   SECRET_KEY=your-super-secret-key-change-in-production
   ACCESS_TOKEN_EXPIRE_MINUTES=30

   # Server Configuration
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True

   # Frontend Configuration
   FRONTEND_URL=http://localhost:3000

   # External API Configuration
   EXTERNAL_API_URL=http://localhost:8001
   ```

## Running the Application

### Development
```bash
python app.py
```

### Production
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/token` - Login and get access token
- `GET /api/auth/me` - Get current user information

### Courses
- `POST /api/courses/generate-course` - Generate a new course using external API
- `POST /api/courses/save` - Save a generated course
- `GET /api/courses/` - Get user's courses
- `GET /api/courses/{course_id}` - Get specific course
- `DELETE /api/courses/{course_id}` - Delete a course

## Architecture

### Configuration Management
- Centralized configuration in `config.py`
- Environment variable validation
- Type-safe settings with Pydantic

### Database
- MongoDB with Beanie ODM
- Async operations
- Document-based models for users and courses

### Authentication
- JWT-based authentication
- Password hashing with bcrypt
- OAuth2 compatible token endpoint

### External API Integration
- HTTP client with proper timeout handling
- Error handling and retry logic
- Support for long-running AI generation requests

### Error Handling
- Comprehensive error handling with specific messages
- Proper HTTP status codes
- Detailed logging for debugging

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- CORS configuration
- Input validation with Pydantic
- Environment variable validation

## Development Guidelines

1. **Code Organization**: Follow the established directory structure
2. **Type Hints**: Use type hints for all functions and variables
3. **Error Handling**: Use proper HTTP exceptions and meaningful error messages
4. **Documentation**: Document all functions and classes
5. **Environment**: Use environment variables for configuration

## External API Requirements

The application requires an external API running on port 8001 with the following endpoint:

- `POST /api/v1/generate-course` - Generate course content

Expected payload:
```json
{
  "prompt": "Course topic description",
  "experience_level": "beginner|intermediate|advanced",
  "personality": "analytical|creative|practical|social",
  "learning_style": "visual|auditory|kinesthetic|interactive",
  "intensity": "short|medium|long"
}
```

## Contributing

1. Follow the existing code style
2. Update documentation
3. Use meaningful commit messages
4. Test integration with external API

## License

This project is licensed under the MIT License. 