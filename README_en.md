# Book Management System

A simple book management system developed with Flask framework. The system provides CRUD (Create, Read, Update, Delete) operations for books and supports book cover image upload and management.

## Main Features

- Book information management (CRUD operations)
- Book cover image upload and management
- Clean and user-friendly interface
- SQLite database for data storage

## System Requirements

- Windows 10 or later
- Python 3.x (for running Python source code)
- No additional requirements for running the executable version

## Quick Start Guide

### Option 1: Running the Executable (Recommended for End Users)

1. Download the latest release package
2. Extract the package to your desired location
3. Run `BookManagementSystem.exe`
4. Open your web browser and visit `http://localhost:5000`

### Option 2: Running from Source Code (For Developers)

1. Ensure Python 3.x is installed on your system
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your web browser and visit `http://localhost:5000`

## Key Features

### Book Management
- View all books in the system
- Add new books with details
- Edit existing book information
- Delete books from the system

### Image Management
- Upload book cover images
- View book covers
- Automatic image resizing and optimization

### User Interface
- Responsive design
- Intuitive navigation
- Real-time search functionality
- Pagination support

## File Structure

- `app.py`: Main application file
- `database.py`: Database models and configurations
- `templates/`: HTML template files
- `static/`: Static resources (CSS, JavaScript, etc.)
- `uploads/`: Directory for storing uploaded book covers
- `books.db`: SQLite database file

## Important Notes

1. For Executable Version:
   - The application will automatically create necessary files and directories
   - Ensure you have write permissions in the installation directory
   - Run as administrator if you encounter permission issues

2. For Source Code Version:
   - Virtual environment is recommended
   - Database will be created automatically on first run
   - Make sure the `uploads` directory has write permissions

## Troubleshooting

1. If the application fails to start:
   - Check if port 5000 is available
   - Ensure all required files are present
   - Try running as administrator

2. If database operations fail:
   - Check file permissions
   - Ensure the application has write access to the directory

3. If image upload fails:
   - Verify the `uploads` directory exists
   - Check disk space availability
   - Ensure proper file permissions

## Support

For any issues or questions, please contact the development team or create an issue in the repository. 