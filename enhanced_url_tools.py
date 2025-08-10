import requests
from bs4 import BeautifulSoup
import qrcode
import io
import base64
from urllib.parse import urlparse, urljoin
import validators
import hashlib
from typing import Dict, List, Any
from url_storage import URLStorage
import json

class EnhancedURLTools:
    def __init__(self):
        self.storage = URLStorage()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Known suspicious domains for basic safety checking
        self.suspicious_domains = [
            'malware-site.com',
            'phishing-example.org',
            'suspicious-domain.net'
        ]
    
    def validate_url(self, url: str) -> Dict[str, Any]:
        """Validate if a URL is properly formatted and reachable"""
        try:
            # First, basic format validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if not validators.url(url):
                return {
                    'is_valid': False,
                    'is_reachable': False,
                    'error': 'Invalid URL format',
                    'url': url
                }
            
            # Check if URL is reachable
            try:
                response = self.session.head(url, timeout=10, allow_redirects=True)
                is_reachable = response.status_code < 400
                status_code = response.status_code
                final_url = response.url
            except Exception as e:
                is_reachable = False
                status_code = None
                final_url = url
            
            return {
                'is_valid': True,
                'is_reachable': is_reachable,
                'status_code': status_code,
                'original_url': url,
                'final_url': final_url,
                'redirected': url != final_url
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'is_reachable': False,
                'error': str(e),
                'url': url
            }
    
    def get_url_metadata(self, url: str) -> Dict[str, Any]:
        """Extract metadata from URL including title, description, and other info"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = ""
            title_tag = soup.find('title')
            og_title = soup.find('meta', property='og:title')
            twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
            
            if og_title and og_title.get('content'):
                title = og_title.get('content').strip()
            elif twitter_title and twitter_title.get('content'):
                title = twitter_title.get('content').strip()
            elif title_tag:
                title = title_tag.get_text().strip()
            
            # Extract description
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            og_desc = soup.find('meta', property='og:description')
            twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
            
            if og_desc and og_desc.get('content'):
                description = og_desc.get('content').strip()
            elif twitter_desc and twitter_desc.get('content'):
                description = twitter_desc.get('content').strip()
            elif meta_desc and meta_desc.get('content'):
                description = meta_desc.get('content').strip()
            
            # Extract favicon
            favicon_url = ""
            favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
            if favicon and favicon.get('href'):
                favicon_url = urljoin(url, favicon.get('href'))
            
            # Extract image
            image_url = ""
            og_image = soup.find('meta', property='og:image')
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            
            if og_image and og_image.get('content'):
                image_url = urljoin(url, og_image.get('content'))
            elif twitter_image and twitter_image.get('content'):
                image_url = urljoin(url, twitter_image.get('content'))
            
            parsed_url = urlparse(url)
            
            return {
                'title': title,
                'description': description,
                'domain': parsed_url.netloc,
                'is_secure': url.startswith('https://'),
                'favicon_url': favicon_url,
                'image_url': image_url,
                'content_length': len(response.content),
                'content_type': response.headers.get('content-type', ''),
                'status_code': response.status_code,
                'url': url
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'url': url,
                'title': '',
                'description': '',
                'domain': urlparse(url).netloc if url else ''
            }
    
    def generate_qr_code(self, url: str, size: int = 10) -> str:
        """Generate QR code for URL and return as base64 string"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                'qr_code_base64': qr_base64,
                'url': url,
                'format': 'PNG',
                'size': f"{img.size[0]}x{img.size[1]}"
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'url': url
            }
    
    def check_url_safety(self, url: str) -> Dict[str, Any]:
        """Check URL safety using basic domain filtering"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            warnings = []
            is_safe = True
            
            # Check against known suspicious domains
            for suspicious in self.suspicious_domains:
                if suspicious in domain:
                    warnings.append(f"Domain '{domain}' matches suspicious pattern")
                    is_safe = False
            
            # Check for suspicious URL patterns
            if len(url) > 200:
                warnings.append("URL is unusually long")
            
            if url.count('/') > 10:
                warnings.append("URL has suspicious number of path segments")
            
            # Check for suspicious parameters
            suspicious_params = ['redirect', 'goto', 'url', 'link', 'forward']
            query_params = parsed_url.query.lower()
            for param in suspicious_params:
                if param in query_params:
                    warnings.append(f"URL contains potentially suspicious parameter: {param}")
            
            # Check if HTTPS
            if not url.startswith('https://'):
                warnings.append("URL is not using secure HTTPS protocol")
            
            return {
                'is_safe': is_safe and len(warnings) <= 1,  # Allow one minor warning
                'warnings': warnings,
                'domain': domain,
                'url': url,
                'risk_level': 'low' if len(warnings) <= 1 else 'medium' if len(warnings) <= 3 else 'high'
            }
            
        except Exception as e:
            return {
                'is_safe': False,
                'error': str(e),
                'url': url,
                'warnings': ['Failed to analyze URL safety']
            }
    
    def expand_url(self, shortened_url: str) -> Dict[str, Any]:
        """Expand a shortened URL to see its final destination"""
        try:
            response = self.session.head(shortened_url, allow_redirects=True, timeout=10)
            final_url = response.url
            
            redirect_chain = []
            if hasattr(response, 'history'):
                redirect_chain = [resp.url for resp in response.history]
            
            return {
                'original_shortened': shortened_url,
                'final_url': final_url,
                'redirect_chain': redirect_chain,
                'redirect_count': len(redirect_chain),
                'status_code': response.status_code,
                'is_safe_redirect': response.status_code < 400
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'original_shortened': shortened_url,
                'final_url': None
            } 