# SEO Meta Tag Analyzer

## Overview

This is a Flask-based web application that analyzes websites for SEO meta tags and provides visual previews of how the content would appear on Google search results and social media platforms. The application extracts meta information from web pages and validates it against SEO best practices, providing users with actionable insights and an overall SEO score.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple monolithic Flask architecture with a clear separation of concerns:

- **Frontend**: HTML templates with Bootstrap for responsive UI
- **Backend**: Flask web framework with modular components
- **Web Scraping**: BeautifulSoup for HTML parsing and requests for HTTP operations
- **Validation**: Custom SEO validation logic based on industry best practices

## Key Components

### 1. Flask Application (`app.py`)
- **Purpose**: Main application entry point and route definitions
- **Routes**: 
  - `/` - Main page with URL input form
  - `/analyze` - POST endpoint for SEO analysis
- **Features**: Error handling, flash messaging, and proxy middleware support

### 2. SEO Analyzer (`seo_analyzer.py`)
- **Purpose**: Core SEO analysis functionality
- **Capabilities**: 
  - URL validation using the `validators` library
  - Web scraping with proper headers and timeout handling
  - Meta tag extraction and validation
  - SEO scoring based on best practices
- **Validation Rules**:
  - Title length: 30-60 characters
  - Description length: 120-160 characters

### 3. Frontend Templates
- **`index.html`**: Clean, responsive input form with Bootstrap dark theme
- **`results.html`**: Comprehensive results display with validation feedback and previews
- **Design**: Uses Font Awesome icons and Bootstrap components for professional appearance

### 4. Static Assets
- **CSS**: Custom styling for Google and social media previews
- **JavaScript**: Form validation, example URLs, and interactive features

## Data Flow

1. **User Input**: User enters a URL on the main page
2. **URL Processing**: Flask validates and normalizes the URL (adds HTTPS if missing)
3. **Web Scraping**: SEOAnalyzer fetches the webpage with proper headers
4. **HTML Parsing**: BeautifulSoup extracts meta tags and content
5. **Validation**: Custom logic evaluates SEO compliance and generates scores
6. **Preview Generation**: Creates visual representations for search engines and social media
7. **Results Display**: Comprehensive results page with recommendations

## External Dependencies

### Python Libraries
- **Flask**: Web framework for routing and templating
- **BeautifulSoup4**: HTML parsing and meta tag extraction
- **requests**: HTTP client for fetching web pages
- **validators**: URL validation
- **werkzeug**: WSGI utilities and middleware

### Frontend Dependencies
- **Bootstrap**: CSS framework with dark theme support
- **Font Awesome**: Icon library for enhanced UI
- **CDN-hosted**: All frontend dependencies loaded from CDNs

## Deployment Strategy

### Environment Configuration
- **Session Secret**: Configurable via `SESSION_SECRET` environment variable
- **Development Mode**: Fallback secret key for development
- **Production Ready**: ProxyFix middleware for reverse proxy deployment

### Platform Compatibility
- **Replit**: Optimized for Replit deployment with proper WSGI configuration
- **General Hosting**: Compatible with any Flask-supporting platform
- **Static Files**: Served through Flask's static file handling

### Performance Considerations
- **Request Timeout**: 10-second timeout for external URL fetching
- **User Agent**: Proper browser user agent to avoid blocking
- **Error Handling**: Comprehensive exception handling for robust operation

### Security Features
- **Input Validation**: URL format validation before processing
- **Secure Headers**: Proper User-Agent headers for legitimate scraping
- **Error Sanitization**: Safe error message display without exposing internals