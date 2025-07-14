import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import validators
import re
from typing import Dict, List, Any

class SEOAnalyzer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 10
        
        # SEO best practice limits
        self.title_min_length = 30
        self.title_max_length = 60
        self.description_min_length = 120
        self.description_max_length = 160

    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze a URL for SEO meta tags and best practices"""
        
        # Validate URL format
        if not validators.url(url):
            return {'error': 'Invalid URL format. Please enter a valid URL.'}
        
        try:
            # Fetch the webpage
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract meta tags
            meta_data = self._extract_meta_tags(soup)
            
            # Validate against best practices
            validation_results = self._validate_seo_tags(meta_data)
            
            # Generate previews
            previews = self._generate_previews(meta_data, url)
            
            return {
                'error': None,
                'meta_data': meta_data,
                'validation': validation_results,
                'previews': previews,
                'url': url
            }
            
        except requests.exceptions.Timeout:
            return {'error': 'Request timed out. The website took too long to respond.'}
        except requests.exceptions.ConnectionError:
            return {'error': 'Could not connect to the website. Please check the URL and try again.'}
        except requests.exceptions.HTTPError as e:
            return {'error': f'HTTP error {e.response.status_code}: {e.response.reason}'}
        except Exception as e:
            return {'error': f'An unexpected error occurred: {str(e)}'}

    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract all relevant SEO meta tags from the HTML"""
        
        meta_data = {
            'title': '',
            'description': '',
            'keywords': '',
            'canonical': '',
            'robots': '',
            'viewport': '',
            'charset': '',
            'og_title': '',
            'og_description': '',
            'og_image': '',
            'og_url': '',
            'og_type': '',
            'og_site_name': '',
            'twitter_card': '',
            'twitter_title': '',
            'twitter_description': '',
            'twitter_image': '',
            'twitter_site': '',
            'h1_tags': [],
            'h2_tags': [],
            'image_alt_missing': 0,
            'total_images': 0
        }
        
        # Title tag
        title_tag = soup.find('title')
        if title_tag:
            meta_data['title'] = title_tag.get_text().strip()
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name', '').lower()
            property_attr = tag.get('property', '').lower()
            content = tag.get('content', '').strip()
            
            # Standard meta tags
            if name == 'description':
                meta_data['description'] = content
            elif name == 'keywords':
                meta_data['keywords'] = content
            elif name == 'robots':
                meta_data['robots'] = content
            elif name == 'viewport':
                meta_data['viewport'] = content
            
            # Open Graph tags
            elif property_attr == 'og:title':
                meta_data['og_title'] = content
            elif property_attr == 'og:description':
                meta_data['og_description'] = content
            elif property_attr == 'og:image':
                meta_data['og_image'] = content
            elif property_attr == 'og:url':
                meta_data['og_url'] = content
            elif property_attr == 'og:type':
                meta_data['og_type'] = content
            elif property_attr == 'og:site_name':
                meta_data['og_site_name'] = content
            
            # Twitter Card tags
            elif name == 'twitter:card':
                meta_data['twitter_card'] = content
            elif name == 'twitter:title':
                meta_data['twitter_title'] = content
            elif name == 'twitter:description':
                meta_data['twitter_description'] = content
            elif name == 'twitter:image':
                meta_data['twitter_image'] = content
            elif name == 'twitter:site':
                meta_data['twitter_site'] = content
            
            # Charset
            elif tag.get('charset'):
                meta_data['charset'] = tag.get('charset')
        
        # Canonical URL
        canonical_tag = soup.find('link', rel='canonical')
        if canonical_tag:
            meta_data['canonical'] = canonical_tag.get('href', '')
        
        # H1 and H2 tags
        meta_data['h1_tags'] = [h1.get_text().strip() for h1 in soup.find_all('h1')]
        meta_data['h2_tags'] = [h2.get_text().strip() for h2 in soup.find_all('h2')]
        
        # Image alt attributes
        images = soup.find_all('img')
        meta_data['total_images'] = len(images)
        meta_data['image_alt_missing'] = len([img for img in images if not img.get('alt')])
        
        return meta_data

    def _validate_seo_tags(self, meta_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate meta tags against SEO best practices"""
        
        validation = {
            'title': {'status': 'success', 'messages': []},
            'description': {'status': 'success', 'messages': []},
            'og_tags': {'status': 'success', 'messages': []},
            'twitter_tags': {'status': 'success', 'messages': []},
            'technical': {'status': 'success', 'messages': []},
            'content': {'status': 'success', 'messages': []},
            'overall_score': 100
        }
        
        score_deduction = 0
        
        # Title validation
        title = meta_data['title']
        if not title:
            validation['title']['status'] = 'error'
            validation['title']['messages'].append('Missing title tag')
            score_deduction += 15
        else:
            if len(title) < self.title_min_length:
                validation['title']['status'] = 'warning'
                validation['title']['messages'].append(f'Title too short ({len(title)} chars). Recommended: {self.title_min_length}-{self.title_max_length} characters')
                score_deduction += 5
            elif len(title) > self.title_max_length:
                validation['title']['status'] = 'warning'
                validation['title']['messages'].append(f'Title too long ({len(title)} chars). Recommended: {self.title_min_length}-{self.title_max_length} characters')
                score_deduction += 5
            else:
                validation['title']['messages'].append('Title length is optimal')
        
        # Description validation
        description = meta_data['description']
        if not description:
            validation['description']['status'] = 'error'
            validation['description']['messages'].append('Missing meta description')
            score_deduction += 15
        else:
            if len(description) < self.description_min_length:
                validation['description']['status'] = 'warning'
                validation['description']['messages'].append(f'Description too short ({len(description)} chars). Recommended: {self.description_min_length}-{self.description_max_length} characters')
                score_deduction += 5
            elif len(description) > self.description_max_length:
                validation['description']['status'] = 'warning'
                validation['description']['messages'].append(f'Description too long ({len(description)} chars). Recommended: {self.description_min_length}-{self.description_max_length} characters')
                score_deduction += 5
            else:
                validation['description']['messages'].append('Description length is optimal')
        
        # Open Graph validation
        og_missing = []
        if not meta_data['og_title']:
            og_missing.append('og:title')
        if not meta_data['og_description']:
            og_missing.append('og:description')
        if not meta_data['og_image']:
            og_missing.append('og:image')
        
        if og_missing:
            validation['og_tags']['status'] = 'warning'
            validation['og_tags']['messages'].append(f'Missing Open Graph tags: {", ".join(og_missing)}')
            score_deduction += len(og_missing) * 3
        else:
            validation['og_tags']['messages'].append('All essential Open Graph tags present')
        
        # Twitter Card validation
        if not meta_data['twitter_card']:
            validation['twitter_tags']['status'] = 'warning'
            validation['twitter_tags']['messages'].append('Missing Twitter Card type')
            score_deduction += 5
        
        if meta_data['twitter_card'] and not meta_data['twitter_image']:
            validation['twitter_tags']['status'] = 'warning'
            validation['twitter_tags']['messages'].append('Twitter Card specified but missing image')
            score_deduction += 3
        
        if validation['twitter_tags']['status'] == 'success':
            validation['twitter_tags']['messages'].append('Twitter Card tags are properly configured')
        
        # Technical validation
        if not meta_data['canonical']:
            validation['technical']['status'] = 'warning'
            validation['technical']['messages'].append('Missing canonical URL')
            score_deduction += 5
        
        if not meta_data['viewport']:
            validation['technical']['status'] = 'warning'
            validation['technical']['messages'].append('Missing viewport meta tag')
            score_deduction += 5
        
        if validation['technical']['status'] == 'success':
            validation['technical']['messages'].append('Technical SEO tags are properly configured')
        
        # Content validation
        if not meta_data['h1_tags']:
            validation['content']['status'] = 'warning'
            validation['content']['messages'].append('No H1 tags found')
            score_deduction += 10
        elif len(meta_data['h1_tags']) > 1:
            validation['content']['status'] = 'warning'
            validation['content']['messages'].append(f'Multiple H1 tags found ({len(meta_data["h1_tags"])}). Use only one H1 per page')
            score_deduction += 5
        
        if meta_data['image_alt_missing'] > 0:
            validation['content']['status'] = 'warning'
            validation['content']['messages'].append(f'{meta_data["image_alt_missing"]} out of {meta_data["total_images"]} images missing alt attributes')
            score_deduction += min(meta_data['image_alt_missing'] * 2, 10)
        
        if validation['content']['status'] == 'success':
            validation['content']['messages'].append('Content structure is well optimized')
        
        # Calculate overall score
        validation['overall_score'] = max(0, 100 - score_deduction)
        
        return validation

    def _generate_previews(self, meta_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Generate preview data for different platforms"""
        
        # Get domain name for fallbacks
        domain = urlparse(url).netloc
        
        previews = {
            'google': {
                'title': meta_data['title'] or 'Untitled Page',
                'url': url,
                'description': meta_data['description'] or 'No description available'
            },
            'facebook': {
                'title': meta_data['og_title'] or meta_data['title'] or 'Untitled Page',
                'description': meta_data['og_description'] or meta_data['description'] or 'No description available',
                'image': meta_data['og_image'] or '',
                'site_name': meta_data['og_site_name'] or domain,
                'url': meta_data['og_url'] or url
            },
            'twitter': {
                'title': meta_data['twitter_title'] or meta_data['og_title'] or meta_data['title'] or 'Untitled Page',
                'description': meta_data['twitter_description'] or meta_data['og_description'] or meta_data['description'] or 'No description available',
                'image': meta_data['twitter_image'] or meta_data['og_image'] or '',
                'card_type': meta_data['twitter_card'] or 'summary',
                'site': meta_data['twitter_site'] or domain
            },
            'linkedin': {
                'title': meta_data['og_title'] or meta_data['title'] or 'Untitled Page',
                'description': meta_data['og_description'] or meta_data['description'] or 'No description available',
                'image': meta_data['og_image'] or '',
                'site_name': meta_data['og_site_name'] or domain
            }
        }
        
        # Truncate for display limits
        previews['google']['title'] = self._truncate_text(previews['google']['title'], 60)
        previews['google']['description'] = self._truncate_text(previews['google']['description'], 160)
        
        previews['facebook']['title'] = self._truncate_text(previews['facebook']['title'], 100)
        previews['facebook']['description'] = self._truncate_text(previews['facebook']['description'], 300)
        
        previews['twitter']['title'] = self._truncate_text(previews['twitter']['title'], 70)
        previews['twitter']['description'] = self._truncate_text(previews['twitter']['description'], 200)
        
        previews['linkedin']['title'] = self._truncate_text(previews['linkedin']['title'], 100)
        previews['linkedin']['description'] = self._truncate_text(previews['linkedin']['description'], 300)
        
        return previews

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + '...'
