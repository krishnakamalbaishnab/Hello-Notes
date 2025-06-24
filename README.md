# HelloNotes - Student-Focused Note-Taking Application

A modern, distraction-free note-taking web application built with FastAPI, MongoDB, and Bootstrap. Designed specifically for students to organize their academic life efficiently.

## 🚀 Features

### ✅ Core Features
- **User Authentication**: Secure JWT-based authentication with registration and login
- **Rich Note Creation**: Create notes with titles, content, tags, and markdown formatting
- **Folder Organization**: Organize notes into color-coded folders
- **To-Do Integration**: Add task lists directly within notes
- **Important Notes**: Mark crucial notes for quick access
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### 🎨 Enhanced UI/UX
- **Modern Bootstrap Design**: Clean, professional interface
- **Rich Text Editor**: Basic formatting (bold, italic, underline, links)
- **Interactive Elements**: Hover effects, smooth transitions, and animations
- **Accessibility**: Keyboard navigation and screen reader support
- **Print-Friendly**: Optimized for printing notes

### 📱 Student-Focused Features
- **Quick Stats Dashboard**: Overview of notes, folders, and progress
- **Tag System**: Categorize notes with custom tags
- **Search & Filter**: Find notes quickly (coming soon)
- **Calendar Integration**: Sync with Google Calendar (placeholder)
- **Image Upload**: Add images to notes (coming soon)

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Frontend**: Bootstrap 5 + Jinja2 Templates
- **Authentication**: JWT with bcrypt password hashing
- **Styling**: Custom CSS with dark mode support
- **Icons**: Bootstrap Icons

## 📦 Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HelloNotes
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=your_mongodb_connection_string
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_NAME=hellonotes
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8000`

## 🏗️ Project Structure

```
HelloNotes/
├── config/
│   ├── db.py          # Database configuration
│   └── settings.py    # Application settings
├── models/
│   ├── user.py        # User data models
│   ├── note.py        # Note data models
│   └── folder.py      # Folder data models
├── routes/
│   ├── auth.py        # Authentication routes
│   ├── note.py        # Note management routes
│   └── folder.py      # Folder management routes
├── templates/
│   ├── base.html      # Base template
│   ├── landing.html   # Landing page
│   ├── dashboard.html # Main dashboard
│   ├── auth/          # Authentication templates
│   ├── notes/         # Note templates
│   └── folders/       # Folder templates
├── static/
│   ├── styles.css     # Custom CSS
│   └── uploads/       # File uploads directory
├── utils/
│   └── auth.py        # Authentication utilities
├── main.py            # Main application file
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔧 Configuration

### Database Setup
The application uses MongoDB. You can use:
- **MongoDB Atlas** (cloud): Free tier available
- **Local MongoDB**: Install and run locally
- **Docker**: Use MongoDB container

### Security Settings
- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Configure proper CORS settings
- Set up rate limiting

## 🚀 Deployment

### Production Deployment
1. **Set up a production server** (AWS, DigitalOcean, Heroku, etc.)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment variables**
4. **Set up a reverse proxy** (Nginx recommended)
5. **Use a production ASGI server** (Gunicorn + Uvicorn)
6. **Set up SSL certificates**

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Input Validation**: Pydantic models for data validation
- **SQL Injection Protection**: MongoDB with parameterized queries
- **XSS Protection**: Jinja2 auto-escaping
- **CSRF Protection**: Form-based protection

## 📊 Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "username": "string",
  "hashed_password": "string",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Notes Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "title": "string",
  "content": "string",
  "folder_id": "string",
  "tags": ["string"],
  "is_important": "boolean",
  "todos": [
    {
      "id": "string",
      "text": "string",
      "completed": "boolean",
      "created_at": "datetime"
    }
  ],
  "images": ["string"],
  "links": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Folders Collection
```json
{
  "_id": "ObjectId",
  "user_id": "string",
  "name": "string",
  "description": "string",
  "color": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Test Coverage
- Unit tests for models and utilities
- Integration tests for API endpoints
- Frontend testing with Selenium (planned)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 API Documentation

Once the application is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

## 🎯 Roadmap

### Phase 2 Features
- [ ] **Advanced Search**: Full-text search with filters
- [ ] **Image Upload**: Drag-and-drop image support
- [ ] **Google Calendar Integration**: Sync events with notes
- [ ] **Export Options**: PDF, Markdown, and Word export
- [ ] **Collaboration**: Share notes with other users
- [ ] **Mobile App**: React Native mobile application

### Phase 3 Features
- [ ] **AI Integration**: Smart note suggestions
- [ ] **Voice Notes**: Speech-to-text functionality
- [ ] **Offline Support**: Progressive Web App features
- [ ] **Advanced Analytics**: Study progress tracking
- [ ] **Plugin System**: Extensible architecture

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **Bootstrap** for the responsive UI components
- **MongoDB** for the flexible database solution
- **Bootstrap Icons** for the beautiful icon set

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: support@hellonotes.com
- Documentation: [docs.hellonotes.com](https://docs.hellonotes.com)

---

**HelloNotes** - Making student life more organized, one note at a time! 📚✨ 