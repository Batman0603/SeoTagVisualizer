import os
import logging
import time
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from seo_analyzer import SEOAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure database
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
else:
    # Fallback for development
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///seo_analyzer.db"

# Initialize database
db = SQLAlchemy(app, model_class=Base)

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
    
    start_time = time.time()
    
    try:
        analyzer = SEOAnalyzer()
        results = analyzer.analyze_url(url)
        
        if results['error']:
            # Save failed analysis to database
            save_analysis_to_db(url, None, results['error'], time.time() - start_time)
            flash(results['error'], 'error')
            return redirect(url_for('index'))
        
        # Save successful analysis to database
        processing_time = time.time() - start_time
        save_analysis_to_db(url, results, None, processing_time)
        
        return render_template('results.html', results=results, url=url)
    
    except Exception as e:
        app.logger.error(f"Error analyzing URL {url}: {str(e)}")
        save_analysis_to_db(url, None, str(e), time.time() - start_time)
        flash('An error occurred while analyzing the website. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

def save_analysis_to_db(url, results, error_message, processing_time):
    """Save analysis results to database"""
    try:
        
        # Extract domain from URL
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Create new analysis record
        analysis = SeoAnalysis(
            url=url,
            domain=domain,
            processing_time=processing_time,
            error_message=error_message
        )
        
        if results and not error_message:
            # Extract meta data
            meta_data = results.get('meta_data', {})
            analysis.title = meta_data.get('title')
            analysis.title_length = len(meta_data.get('title', ''))
            analysis.description = meta_data.get('description')
            analysis.description_length = len(meta_data.get('description', ''))
            analysis.keywords = meta_data.get('keywords')
            
            # Extract Open Graph data
            analysis.og_title = meta_data.get('og:title')
            analysis.og_description = meta_data.get('og:description')
            analysis.og_image = meta_data.get('og:image')
            analysis.og_url = meta_data.get('og:url')
            analysis.og_type = meta_data.get('og:type')
            analysis.og_site_name = meta_data.get('og:site_name')
            
            # Extract Twitter Card data
            analysis.twitter_card = meta_data.get('twitter:card')
            analysis.twitter_title = meta_data.get('twitter:title')
            analysis.twitter_description = meta_data.get('twitter:description')
            analysis.twitter_image = meta_data.get('twitter:image')
            analysis.twitter_site = meta_data.get('twitter:site')
            
            # Extract scores
            validation = results.get('validation', {})
            analysis.overall_score = validation.get('overall_score', 0)
            analysis.title_score = validation.get('title_score', 0)
            analysis.description_score = validation.get('description_score', 0)
            analysis.og_score = validation.get('og_score', 0)
            analysis.twitter_score = validation.get('twitter_score', 0)
            
            # Set validation flags
            analysis.has_title = bool(meta_data.get('title'))
            analysis.has_description = bool(meta_data.get('description'))
            analysis.has_keywords = bool(meta_data.get('keywords'))
            analysis.has_og_tags = any([
                meta_data.get('og:title'),
                meta_data.get('og:description'),
                meta_data.get('og:image')
            ])
            analysis.has_twitter_cards = any([
                meta_data.get('twitter:card'),
                meta_data.get('twitter:title'),
                meta_data.get('twitter:description')
            ])
            
            # Additional metadata
            analysis.canonical_url = meta_data.get('canonical')
            analysis.robots = meta_data.get('robots')
            analysis.viewport = meta_data.get('viewport')
            analysis.charset = meta_data.get('charset')
        
        # Save to database
        db.session.add(analysis)
        
        # Update or create domain statistics
        if not error_message:
            domain_stats = DomainStats.query.filter_by(domain=domain).first()
            if not domain_stats:
                domain_stats = DomainStats(domain=domain)
                db.session.add(domain_stats)
            
            domain_stats.update_stats(analysis)
        
        db.session.commit()
        app.logger.info(f"Saved analysis for {url} to database")
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error saving analysis to database: {str(e)}")


@app.route('/history')
def history():
    """Show analysis history"""
    try:
        
        # Get recent analyses (last 50)
        analyses = SeoAnalysis.query.order_by(
            SeoAnalysis.analysis_date.desc()
        ).limit(50).all()
        
        return render_template('history.html', analyses=analyses)
    
    except Exception as e:
        app.logger.error(f"Error fetching history: {str(e)}")
        flash('Error loading analysis history', 'error')
        return redirect(url_for('index'))


@app.route('/stats')
def stats():
    """Show domain statistics"""
    try:
        
        # Get top domains by analysis count
        top_domains = DomainStats.query.order_by(
            DomainStats.total_analyses.desc()
        ).limit(20).all()
        
        # Get overall statistics
        total_analyses = SeoAnalysis.query.count()
        avg_score = db.session.query(db.func.avg(SeoAnalysis.overall_score)).scalar() or 0
        
        return render_template('stats.html', 
                             top_domains=top_domains,
                             total_analyses=total_analyses,
                             avg_score=round(avg_score, 1))
    
    except Exception as e:
        app.logger.error(f"Error fetching stats: {str(e)}")
        flash('Error loading statistics', 'error')
        return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal error: {str(error)}")
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html'), 500

# Import and initialize models
import models
SeoAnalysis, DomainStats = models.init_models(db)

with app.app_context():
    db.create_all()
    app.logger.info("Database tables created")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
