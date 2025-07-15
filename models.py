from datetime import datetime


# Models will be created after db is initialized
SeoAnalysis = None
DomainStats = None


def init_models(db):
    """Initialize models with database instance"""
    global SeoAnalysis, DomainStats
    
    class SeoAnalysis(db.Model):
        """Store SEO analysis results for websites"""
        __tablename__ = 'seo_analyses'
        
        id = db.Column(db.Integer, primary_key=True)
        url = db.Column(db.String(2048), nullable=False, index=True)
        domain = db.Column(db.String(255), nullable=False, index=True)
        
        # Meta tag data
        title = db.Column(db.Text)
        title_length = db.Column(db.Integer)
        description = db.Column(db.Text)
        description_length = db.Column(db.Integer)
        keywords = db.Column(db.Text)
        
        # Open Graph data
        og_title = db.Column(db.Text)
        og_description = db.Column(db.Text)
        og_image = db.Column(db.String(2048))
        og_url = db.Column(db.String(2048))
        og_type = db.Column(db.String(100))
        og_site_name = db.Column(db.String(255))
        
        # Twitter Card data
        twitter_card = db.Column(db.String(100))
        twitter_title = db.Column(db.Text)
        twitter_description = db.Column(db.Text)
        twitter_image = db.Column(db.String(2048))
        twitter_site = db.Column(db.String(255))
        
        # SEO scores and validation
        overall_score = db.Column(db.Integer, default=0)
        title_score = db.Column(db.Integer, default=0)
        description_score = db.Column(db.Integer, default=0)
        og_score = db.Column(db.Integer, default=0)
        twitter_score = db.Column(db.Integer, default=0)
        
        # Validation flags
        has_title = db.Column(db.Boolean, default=False)
        has_description = db.Column(db.Boolean, default=False)
        has_keywords = db.Column(db.Boolean, default=False)
        has_og_tags = db.Column(db.Boolean, default=False)
        has_twitter_cards = db.Column(db.Boolean, default=False)
        
        # Analysis metadata
        analysis_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        processing_time = db.Column(db.Float)  # Time taken to analyze in seconds
        error_message = db.Column(db.Text)  # Store any errors encountered
        
        # Additional metadata
        canonical_url = db.Column(db.String(2048))
        robots = db.Column(db.String(255))
        viewport = db.Column(db.String(255))
        charset = db.Column(db.String(50))
        
        def __repr__(self):
            return f'<SeoAnalysis {self.url}>'
        
        def to_dict(self):
            """Convert analysis to dictionary for JSON serialization"""
            return {
                'id': self.id,
                'url': self.url,
                'domain': self.domain,
                'title': self.title,
                'description': self.description,
                'overall_score': self.overall_score,
                'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
                'has_title': self.has_title,
                'has_description': self.has_description,
                'has_og_tags': self.has_og_tags,
                'has_twitter_cards': self.has_twitter_cards
            }

    class DomainStats(db.Model):
        """Store aggregated statistics for domains"""
        __tablename__ = 'domain_stats'
        
        id = db.Column(db.Integer, primary_key=True)
        domain = db.Column(db.String(255), unique=True, nullable=False, index=True)
        
        # Analysis counts
        total_analyses = db.Column(db.Integer, default=0)
        last_analysis = db.Column(db.DateTime)
        
        # Average scores
        avg_overall_score = db.Column(db.Float, default=0.0)
        avg_title_score = db.Column(db.Float, default=0.0)
        avg_description_score = db.Column(db.Float, default=0.0)
        avg_og_score = db.Column(db.Float, default=0.0)
        avg_twitter_score = db.Column(db.Float, default=0.0)
        
        # Best and worst scores
        best_score = db.Column(db.Integer, default=0)
        worst_score = db.Column(db.Integer, default=100)
        
        created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
        updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def __repr__(self):
            return f'<DomainStats {self.domain}>'
        
        def update_stats(self, new_analysis):
            """Update domain statistics with new analysis"""
            self.total_analyses += 1
            self.last_analysis = datetime.utcnow()
            
            # Update averages (simple running average)
            total = self.total_analyses
            self.avg_overall_score = ((self.avg_overall_score * (total - 1)) + new_analysis.overall_score) / total
            self.avg_title_score = ((self.avg_title_score * (total - 1)) + new_analysis.title_score) / total
            self.avg_description_score = ((self.avg_description_score * (total - 1)) + new_analysis.description_score) / total
            self.avg_og_score = ((self.avg_og_score * (total - 1)) + new_analysis.og_score) / total
            self.avg_twitter_score = ((self.avg_twitter_score * (total - 1)) + new_analysis.twitter_score) / total
            
            # Update best/worst scores
            if new_analysis.overall_score > self.best_score:
                self.best_score = new_analysis.overall_score
            if new_analysis.overall_score < self.worst_score:
                self.worst_score = new_analysis.overall_score
    
    # Set global variables
    globals()['SeoAnalysis'] = SeoAnalysis
    globals()['DomainStats'] = DomainStats
    
    return SeoAnalysis, DomainStats