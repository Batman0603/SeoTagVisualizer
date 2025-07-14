import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from seo_analyzer import SEOAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    """Main page with URL input form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze the submitted URL for SEO"""
    url = request.form.get('url', '').strip()
    
    if not url:
        flash('Please enter a URL to analyze', 'error')
        return redirect(url_for('index'))
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        analyzer = SEOAnalyzer()
        results = analyzer.analyze_url(url)
        
        if results['error']:
            flash(results['error'], 'error')
            return redirect(url_for('index'))
        
        return render_template('results.html', results=results, url=url)
    
    except Exception as e:
        app.logger.error(f"Error analyzing URL {url}: {str(e)}")
        flash('An error occurred while analyzing the website. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal error: {str(error)}")
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
