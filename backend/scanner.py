# # # #scanner.py - World-class cookie scanner using Playwright with enhanced features

# # # import asyncio
# # # import time
# # # import logging
# # # from typing import List, Dict, Optional, Set
# # # from urllib.parse import urljoin, urlparse
# # # from playwright.async_api import async_playwright, Browser, BrowserContext, Page
# # # import json
# # # import hashlib
# # # import tldextract

# # # # Configure logging
# # # logging.basicConfig(level=logging.INFO)
# # # logger = logging.getLogger(__name__)

# # # class PlaywrightScanner:
# # #     """
# # #     World-class cookie scanner designed to compete with CookieYes and Termly
# # #     """
    
# # #     # Fixed configuration for consistency across Docker/Linux environments
# # #     FIXED_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# # #     VIEWPORT = {'width': 1920, 'height': 1080}
# # #     TIMEZONE = 'IST'
    
    
# # #     def __init__(self):
# # #         self.browser: Optional[Browser] = None
# # #         self.playwright: Optional[async_playwright] = None
# # #         self.contexts: List[BrowserContext] = []
        
# # #     async def initialize(self, headless: bool = True):
# # #         """Initialize browser with locked configuration for consistency"""
# # #         logger.info("🔧 Initializing world-class cookie scanner...")
        
# # #         self.playwright = await async_playwright().start()
        
# # #         # Launch with locked configuration for Docker consistency
# # #         self.browser = await self.playwright.chromium.launch(
# # #             headless=headless,
# # #             args=[
# # #                 '--no-sandbox',
# # #                 '--disable-setuid-sandbox', 
# # #                 '--disable-dev-shm-usage',
# # #                 '--disable-web-security',
# # #                 '--disable-features=VizDisplayCompositor',
# # #                 '--disable-background-timer-throttling',
# # #                 '--disable-backgrounding-occluded-windows',
# # #                 '--disable-renderer-backgrounding',
# # #                 '--lang=en-US'
# # #             ]
# # #         )
# # #         logger.info("✅ Browser initialized successfully")

# # #     async def close(self):
# # #         """Gracefully close all contexts and browser"""
# # #         logger.info("🔚 Closing scanner...")
        
# # #         # Close all contexts
# # #         for context in self.contexts:
# # #             try:
# # #                 await context.close()
# # #             except Exception as e:
# # #                 logger.warning(f"⚠️ Error closing context: {e}")
        
# # #         if self.browser:
# # #             await self.browser.close()
# # #         if self.playwright:
# # #             await self.playwright.stop()
        
# # #         logger.info("✅ Scanner closed successfully")

# # #     async def create_consistent_context(self) -> BrowserContext:
# # #         """Create browser context with locked settings for consistency"""
# # #         context = await self.browser.new_context(
# # #             user_agent=self.FIXED_USER_AGENT,
# # #             viewport=self.VIEWPORT,
# # #             timezone_id=self.TIMEZONE,
# # #             permissions=['geolocation', 'notifications'],
# # #             extra_http_headers={
# # #                 'Accept-Language': 'en-US,en;q=0.9',
# # #                 'Accept-Encoding': 'gzip, deflate, br',
# # #                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# # #                 'DNT': '1'
# # #             },
# # #             ignore_https_errors=True
# # #         )
        
# # #         self.contexts.append(context)
# # #         return context

# # #     async def scan_url(self, url: str, options: Dict = None) -> Dict:
# # #         """
# # #         World-class URL scanning with comprehensive cookie detection
# # #         """
# # #         if not options:
# # #             options = {}
            
# # #         # Enhanced default options
# # #         scan_options = {
# # #             'wait_seconds': options.get('wait_seconds', 20),  # Increased wait time
# # #             'max_pages': options.get('max_pages', 300),         # Multi-page scanning
# # #             'deep_scroll': options.get('deep_scroll', True),   # Enhanced scrolling
# # #             'banner_timeout': options.get('banner_timeout', 10), # More banner wait time
# # #             'retry_banner_clicks': options.get('retry_banner_clicks', 3), # Banner click retries
# # #             'collect_network_cookies': options.get('collect_network_cookies', True),
# # #             'wait_for_dynamic_content': options.get('wait_for_dynamic_content', True),
# # #             'simulate_login': options.get('simulate_login', False),
# # #             'simulate_ecommerce': options.get('simulate_ecommerce', False)
# # #         }
        
# # #         logger.info(f"🚀 Starting world-class scan of: {url}")
# # #         start_time = time.time()
        
# # #         context = await self.create_consistent_context()
# # #         page = await context.new_page()
        
# # #         # Comprehensive data collection
# # #         all_cookies = []
# # #         network_cookies = []
# # #         xhr_cookies = []
# # #         consent_interactions = []
# # #         page_urls = [url]
# # #         all_local_storage, all_session_storage = {}, {}
        
# # #         try:
# # #             # Set up comprehensive network monitoring
# # #             await self._setup_network_monitoring(page, network_cookies, xhr_cookies)
            
# # #             # Main page scan
# # #             main_results = await self._scan_single_page(
# # #                 page, url, scan_options, consent_interactions
# # #             )
# # #             all_cookies.extend(main_results['cookies'])
# # #             all_local_storage.update(main_results.get('local_storage', {}))
# # #             all_session_storage.update(main_results.get('session_storage', {}))
            
# # #             # Multi-page discovery and scanning
# # #             if scan_options['max_pages'] > 1:
# # #                 discovered_urls = await self._discover_important_pages(page, url)
# # #                 additional_urls = discovered_urls[:scan_options['max_pages'] - 1]
                
# # #                 for additional_url in additional_urls:
# # #                     logger.info(f"📄 Scanning additional page: {additional_url}")
# # #                     try:
# # #                         additional_results = await self._scan_single_page(
# # #                             page, additional_url, scan_options, consent_interactions
# # #                         )
# # #                         all_cookies.extend(additional_results['cookies'])
# # #                         all_local_storage.update(additional_results.get('local_storage', {}))
# # #                         all_session_storage.update(additional_results.get('session_storage', {}))
# # #                         page_urls.append(additional_url)
                        
# # #                         # Brief pause between pages
# # #                         await asyncio.sleep(2)
# # #                     except Exception as e:
# # #                         logger.warning(f"⚠️ Failed to scan {additional_url}: {e}")
            
# # #             # User Journey Simulations
# # #             if scan_options['simulate_login'] : 
# # #                 await self._simulate_login(page)
# # #             if scan_options['simulate_ecommerce'] : 
# # #                 await self._simulate_ecommerce(page)
            
# # #             # Collect final cookies from context
# # #             final_browser_cookies = await context.cookies()
            
# # #             # Enhanced cookie aggregation and deduplication
# # #             deduplicated_cookies = self._deduplicate_cookies(
# # #                 all_cookies + final_browser_cookies
# # #             )
            
# # #             # Standardize cookie data format
# # #             standardized_cookies = self._standardize_cookies(
# # #                 deduplicated_cookies, url
# # #             )
            
# # #             scan_duration = time.time() - start_time
            
# # #             results = {
# # #                 'browser_cookies': standardized_cookies,
# # #                 'network_cookies': network_cookies,
# # #                 'xhr_cookies': xhr_cookies,
# # #                 'js_cookies': main_results.get('js_cookies', ''),
# # #                 'visited_urls': page_urls,
# # #                 'consent_interactions': consent_interactions,
# # #                 'local_storage': all_local_storage,
# # #                 'session_storage': all_session_storage,
# # #                 'scan_metadata': {
# # #                     'duration_seconds': round(scan_duration, 2),
# # #                     'pages_scanned': len(page_urls),
# # #                     'total_cookies_found': len(standardized_cookies),
# # #                     'user_agent': self.FIXED_USER_AGENT,
# # #                     'viewport': f"{self.VIEWPORT['width']}x{self.VIEWPORT['height']}",
# # #                     'scan_timestamp': time.time()
# # #                 }
# # #             }
            
# # #             logger.info(f"✅ Scan completed: {len(standardized_cookies)} cookies found in {scan_duration:.2f}s")
# # #             return results
            
# # #         except Exception as e:
# # #             logger.error(f"❌ Scan failed: {e}")
# # #             raise
# # #         finally:
# # #             await context.close()
# # #             if context in self.contexts:
# # #                 self.contexts.remove(context)

# # #     async def _setup_network_monitoring(self, page: Page, network_cookies: List, xhr_cookies: List):
# # #         """Set up comprehensive network request monitoring"""
        
# # #         async def handle_response(response):
# # #             try:
# # #                 headers = await response.all_headers()
# # #                 set_cookie_header = headers.get('set-cookie')
                
# # #                 if set_cookie_header:
# # #                     network_cookies.append({
# # #                         'url': response.url,
# # #                         'set_cookie_header': set_cookie_header,
# # #                         'status': response.status,
# # #                         'timestamp': time.time()
# # #                     })
                    
# # #                 # Track XHR/Fetch requests specifically
# # #                 if response.request.resource_type in ['xhr', 'fetch']:
# # #                     if set_cookie_header:
# # #                         xhr_cookies.append({
# # #                             'url': response.url,
# # #                             'method': response.request.method,
# # #                             'set_cookie_header': set_cookie_header,
# # #                             'timestamp': time.time()
# # #                         })
                        
# # #             except Exception as e:
# # #                 logger.debug(f"Network monitoring error: {e}")

# # #         page.on('response', handle_response)

# # #     async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
# # #         """Enhanced single page scanning with comprehensive cookie detection"""
        
# # #         logger.info(f"📊 Scanning page: {url}")
        
# # #         # Navigate with enhanced wait conditions
# # #         await page.goto(
# # #             url, 
# # #             wait_until='domcontentloaded',
# # #             timeout=90000
# # #         )
        
# # #         # Wait for initial dynamic content
# # #         if options['wait_for_dynamic_content']:
# # #             await self._wait_for_dynamic_content(page)
        
# # #         # Collect initial cookies
# # #         initial_cookies = await page.context.cookies()
        
# # #         # Enhanced scrolling to trigger lazy-loaded content
# # #         if options['deep_scroll']:
# # #             await self._enhanced_auto_scroll(page)
        
# # #         # Advanced banner detection and interaction
# # #         banner_success = await self._advanced_consent_handling(
# # #             page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
# # #         )
        
# # #         # Post-consent wait for cookie loading
# # #         if banner_success:
# # #             logger.info("🍪 Waiting for post-consent cookies to load...")
# # #             await asyncio.sleep(options['wait_seconds'])
            
# # #             # Additional dynamic content check after consent
# # #             if options['wait_for_dynamic_content']:
# # #                 await self._wait_for_dynamic_content(page)
# # #         else:
# # #             # Standard wait even without banner interaction
# # #             await asyncio.sleep(options['wait_seconds'])
        
# # #         # Collect final cookies
# # #         final_cookies = await page.context.cookies()
        
# # #         # Get JavaScript-accessible cookies
# # #         try:
# # #             js_cookies = await page.evaluate("document.cookie")
# # #         except Exception as e:
# # #             logger.warning(f"Could not get JS cookies: {e}")
# # #             js_cookies = ""
        
# # #         # --- NEW: Scrape local and session storage ---
# # #         local_storage = await page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))")
# # #         session_storage = await page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))")
        
# # #         return {
# # #             'cookies': final_cookies,
# # #             'js_cookies': js_cookies,
# # #             'initial_cookie_count': len(initial_cookies),
# # #             'local_storage': local_storage,
# # #             'session_storage': session_storage,
# # #             'final_cookie_count': len(final_cookies)
# # #         }

# # #     async def _wait_for_dynamic_content(self, page: Page):
# # #         """Wait for dynamic content to load (XHR, scripts, etc.)"""
# # #         try:
# # #             # Wait for network to be mostly idle
# # #             await page.wait_for_load_state('networkidle', timeout=20000)
            
# # #             # Additional wait for any remaining async operations
# # #             await page.wait_for_timeout(2000)
            
# # #         except Exception as e:
# # #             logger.debug(f"Dynamic content wait completed with: {e}")
            
# # #     async def _simulate_login(self, page: Page):
# # #         logger.info("🤖 Simulating user login...")
# # #         try:
# # #             # (Code for login simulation)
# # #             pass
# # #         except Exception as e:
# # #             logger.warning(f"⚠️ Login simulation failed: {e}")
            
# # #     async def _simulate_ecommerce(self, page: Page):
# # #         logger.info("🛒 Simulating e-commerce actions...")
# # #         try:
# # #             # (Code for e-commerce simulation)
# # #             pass
# # #         except Exception as e:
# # #             logger.warning(f"⚠️ E-commerce simulation failed: {e}")

# # #     async def _enhanced_auto_scroll(self, page: Page):
# # #         """Enhanced auto-scrolling to trigger all lazy-loaded content"""
        
# # #         logger.debug("🔄 Enhanced auto-scrolling...")
        
# # #         await page.evaluate("""
# # #         async () => {
# # #             const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            
# # #             // Comprehensive scrolling strategy
# # #             const totalHeight = document.body.scrollHeight;
# # #             const viewportHeight = window.innerHeight;
# # #             const scrollStep = Math.max(100, viewportHeight / 4);
            
# # #             // Scroll down in steps
# # #             for (let y = 0; y < totalHeight; y += scrollStep) {
# # #                 window.scrollTo(0, y);
# # #                 await sleep(200);
# # #             }
            
# # #             // Scroll back up to trigger any reverse-lazy loading
# # #             for (let y = totalHeight; y > 0; y -= scrollStep) {
# # #                 window.scrollTo(0, y);
# # #                 await sleep(100);
# # #             }
            
# # #             // Final scroll to bottom
# # #             window.scrollTo(0, document.body.scrollHeight);
# # #             await sleep(500);
            
# # #             // Scroll to top
# # #             window.scrollTo(0, 0);
# # #             await sleep(500);
# # #         }
# # #         """)

# # #     async def _advanced_consent_handling(self, page: Page, timeout: int, retries: int, consent_interactions: List) -> bool:
# # #         """
# # #         World-class consent banner detection and handling
# # #         """
# # #         logger.info("🎯 Advanced consent banner detection...")
        
# # #         # Comprehensive selector list for consent banners
# # #         consent_selectors = [
# # #             # Generic accept buttons
# # #             'button:has-text("Accept")', 'button:has-text("Accept All")',
# # #             'button:has-text("Accept all")', 'button:has-text("I Accept")',
# # #             'button:has-text("Allow All")', 'button:has-text("Allow all")',
# # #             'button:has-text("Agree")', 'button:has-text("I Agree")',
# # #             'button:has-text("OK")', 'button:has-text("Got it")',
# # #             'button:has-text("Continue")', 'button:has-text("Proceed")',
            
# # #             # Attribute-based selectors
# # #             '[data-testid*="accept"]', '[data-cy*="accept"]', 
# # #             '[id*="accept"]', '[class*="accept"]',
# # #             '[data-testid*="consent"]', '[data-cy*="consent"]',
# # #             '[id*="consent"]', '[class*="consent"]',
# # #             '[data-testid*="cookie"]', '[data-cy*="cookie"]',
# # #             '[id*="cookie"]', '[class*="cookie"]',
            
# # #             # Common consent management platforms
# # #             '[data-callback="acceptAllCallback"]',
# # #             '[data-cli-action="accept"]',
# # #             '[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
# # #             '[class*="ot-pc-refuse-all-handler"]',
# # #             '[class*="optanon-allow-all"]',
# # #             '[id*="truste-consent-button"]',
            
# # #             # OneTrust specific
# # #             '#onetrust-accept-btn-handler',
# # #             '[class*="accept-cookies-btn"]',
# # #             '[class*="cookie-accept"]',
            
# # #             # CookieBot specific  
# # #             '[id*="CybotCookiebotDialog"]',
            
# # #             # Cookieyes specific
# # #             '[data-cli-action="accept_all"]',
            
# # #             # Modal and overlay patterns
# # #             '[role="dialog"] button:has-text("Accept")',
# # #             '[role="banner"] button:has-text("Accept")',
# # #             '.cookie-banner button:has-text("Accept")',
# # #             '.consent-banner button:has-text("Accept")',
            
# # #             # Language variations
# # #             'button:has-text("Accepter")',  # French
# # #             'button:has-text("Aceptar")',   # Spanish
# # #             'button:has-text("Akzeptieren")', # German
# # #             'button:has-text("Accettare")', # Italian
# # #             'button:has-text("Aceitar")',   # Portuguese
# # #         ]
        
# # #         # Check for iframes that might contain consent forms
# # #         iframe_selectors = [
# # #             'iframe[src*="consent"]',
# # #             'iframe[src*="cookie"]',
# # #             'iframe[id*="consent"]',
# # #             'iframe[id*="cookie"]',
# # #             'iframe[name*="consent"]',
# # #             'iframe[name*="cookie"]'
# # #         ]
        
# # #         success = False
        
# # #         for attempt in range(retries):
# # #             logger.debug(f"🎯 Consent detection attempt {attempt + 1}/{retries}")
            
# # #             try:
# # #                 # First check main page
# # #                 for selector in consent_selectors:
# # #                     try:
# # #                         element = page.locator(selector).first
# # #                         if await element.is_visible(timeout=2000):
# # #                             logger.info(f"✅ Found consent button: {selector}")
                            
# # #                             # Record the interaction
# # #                             consent_interactions.append({
# # #                                 'selector': selector,
# # #                                 'attempt': attempt + 1,
# # #                                 'timestamp': time.time(),
# # #                                 'type': 'main_page'
# # #                             })
                            
# # #                             await element.click(timeout=5000)
# # #                             await page.wait_for_timeout(2000)  # Wait for response
# # #                             success = True
# # #                             break
                            
# # #                     except Exception:
# # #                         continue
                
# # #                 if success:
# # #                     break
                
# # #                 # Check iframes for consent forms
# # #                 for iframe_selector in iframe_selectors:
# # #                     try:
# # #                         iframe = page.locator(iframe_selector).first
# # #                         if await iframe.is_visible(timeout=1000):
# # #                             frame = await iframe.content_frame()
# # #                             if frame:
# # #                                 for selector in consent_selectors[:10]:  # Try top selectors in iframe
# # #                                     try:
# # #                                         element = frame.locator(selector).first
# # #                                         if await element.is_visible(timeout=1000):
# # #                                             logger.info(f"✅ Found consent button in iframe: {selector}")
                                            
# # #                                             consent_interactions.append({
# # #                                                 'selector': selector,
# # #                                                 'attempt': attempt + 1,
# # #                                                 'timestamp': time.time(),
# # #                                                 'type': 'iframe',
# # #                                                 'iframe_selector': iframe_selector
# # #                                             })
                                            
# # #                                             await element.click(timeout=5000)
# # #                                             await page.wait_for_timeout(2000)
# # #                                             success = True
# # #                                             break
# # #                                     except Exception:
# # #                                         continue
                                        
# # #                         if success:
# # #                             break
                            
# # #                     except Exception:
# # #                         continue
                
# # #                 if success:
# # #                     break
                    
# # #                 # Wait before next attempt
# # #                 if attempt < retries - 1:
# # #                     await asyncio.sleep(2)
                    
# # #             except Exception as e:
# # #                 logger.debug(f"Consent attempt {attempt + 1} error: {e}")
        
# # #         if success:
# # #             logger.info("🎉 Successfully interacted with consent banner")
# # #         else:
# # #             logger.info("ℹ️ No consent banner found or interaction failed")
            
# # #         return success

# # #     async def _discover_important_pages(self, page: Page, base_url: str) -> List[str]:
# # #         """Discover important pages to scan for additional cookies"""
        
# # #         logger.debug("🔍 Discovering important pages...")
        
# # #         try:
# # #             important_links = await page.evaluate("""
# # #             () => {
# # #                 const links = Array.from(document.querySelectorAll('a[href]'));
# # #                 const important_patterns = [
# # #                     /privacy/i, /cookie/i, /terms/i, /legal/i, /policy/i,
# # #                     /contact/i, /about/i, /login/i, /register/i, /account/i,
# # #                     /settings/i, /preferences/i, /profile/i
# # #                 ];
                
# # #                 const found_links = [];
# # #                 const base_domain = window.location.hostname;
                
# # #                 for (const link of links) {
# # #                     const href = link.getAttribute('href');
# # #                     if (!href) continue;
                    
# # #                     let full_url;
# # #                     try {
# # #                         full_url = new URL(href, window.location.origin);
# # #                     } catch {
# # #                         continue;
# # #                     }
                    
# # #                     // Only internal links
# # #                     if (full_url.hostname !== base_domain) continue;
                    
# # #                     // Check against important patterns
# # #                     const path = full_url.pathname.toLowerCase();
# # #                     const text = (link.textContent || '').toLowerCase();
                    
# # #                     for (const pattern of important_patterns) {
# # #                         if (pattern.test(path) || pattern.test(text)) {
# # #                             found_links.push(full_url.href);
# # #                             break;
# # #                         }
# # #                     }
# # #                 }
                
# # #                 // Remove duplicates and limit
# # #                 return [...new Set(found_links)].slice(0, 5);
# # #             }
# # #             """)
            
# # #             parsed_base = urlparse(base_url)
# # #             filtered_links = []
            
# # #             for link in important_links:
# # #                 parsed_link = urlparse(link)
# # #                 if parsed_link.netloc == parsed_base.netloc:
# # #                     filtered_links.append(link)
            
# # #             logger.debug(f"📋 Found {len(filtered_links)} important pages to scan")
# # #             return filtered_links
            
# # #         except Exception as e:
# # #             logger.debug(f"Page discovery error: {e}")
# # #             return []

# # #     def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
# # #         """Remove duplicate cookies based on name and domain"""
        
# # #         seen = set()
# # #         deduplicated = []
        
# # #         for cookie in cookies:
# # #             # Create unique identifier
# # #             identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}"
            
# # #             if identifier not in seen:
# # #                 seen.add(identifier)
# # #                 deduplicated.append(cookie)
        
# # #         logger.debug(f"🔄 Deduplicated {len(cookies)} → {len(deduplicated)} cookies")
# # #         return deduplicated

# # #     def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
# # #         """Standardize cookie data format for consistency"""
        
# # #         standardized = []
# # #         base_domain = self._get_base_domain(base_url)
        
# # #         for cookie in cookies:
# # #             try:
# # #                 cookie_domain = cookie.get('domain', '').lstrip('.')
# # #                 if not cookie_domain:
# # #                     cookie_domain = base_domain
                
# # #                 standardized_cookie = {
# # #                     'name': cookie.get('name', ''),
# # #                     'value': cookie.get('value', ''),
# # #                     'domain': cookie_domain,
# # #                     'path': cookie.get('path', '/'),
# # #                     'expires': cookie.get('expires', -1),
# # #                     'httpOnly': cookie.get('httpOnly', False),
# # #                     'secure': cookie.get('secure', False),
# # #                     'sameSite': cookie.get('sameSite', 'Lax'),
# # #                     'is_third_party': cookie_domain != base_domain,
# # #                     'base_domain': self._get_base_domain(cookie_domain),
# # #                     'size': len(cookie.get('value', '')),
# # #                     'timestamp': time.time()
# # #                 }
                
# # #                 standardized.append(standardized_cookie)
                
# # #             except Exception as e:
# # #                 logger.debug(f"Cookie standardization error: {e}")
# # #                 continue
        
# # #         return standardized

# # #     def _get_base_domain(self, url_or_domain: str) -> str:
# # #         """
# # #         Accurately extract the base domain (e.g., google.com) from a URL 
# # #         or domain string using tldextract.
# # #         """
# # #         try:
# # #             extracted = tldextract.extract(url_or_domain,cache_dir="/tmp")
# # #             # Combine the domain and suffix (e.g., 'google' + '.' + 'co.uk')
# # #             if extracted.domain and extracted.suffix:
# # #                 return f"{extracted.domain}.{extracted.suffix}"
# # #             # Fallback for cases where it might just be a domain without a known suffix (like 'localhost')
# # #             return extracted.domain or url_or_domain
# # #         except Exception:
# # #             return url_or_domain


# # # #scanner.py - World-class cookie scanner using Playwright with enhanced features

# # # import asyncio
# # # import time
# # # import logging
# # # from typing import List, Dict, Optional, Set
# # # from urllib.parse import urljoin, urlparse
# # # from playwright.async_api import async_playwright, Browser, BrowserContext, Page
# # # import json
# # # import hashlib
# # # import tldextract

# # # # (Logging configuration as before)
# # # logger = logging.getLogger(__name__)

# # # class PlaywrightScanner:
# # #     # (FIXED_USER_AGENT, VIEWPORT, TIMEZONE as before)
# # #     FIXED_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# # #     VIEWPORT = {'width': 1920, 'height': 1080}
# # #     TIMEZONE = 'IST'
    
# # #     def __init__(self):
# # #         self.browser: Optional[Browser] = None
# # #         self.playwright: Optional[async_playwright] = None
# # #         self.contexts: List[BrowserContext] = []
        
# # #     async def initialize(self, headless: bool = True):
# # #         # (Same initialize logic as before)
# # #         logger.info("🔧 Initializing world-class cookie scanner...")
# # #         self.playwright = await async_playwright().start()
# # #         self.browser = await self.playwright.chromium.launch(
# # #             headless=headless,
# # #             args=[
# # #                 '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
# # #                 '--disable-web-security', '--disable-features=VizDisplayCompositor',
# # #                 '--disable-background-timer-throttling', '--disable-backgrounding-occluded-windows',
# # #                 '--disable-renderer-backgrounding', '--lang=en-US'
# # #             ]
# # #         )
# # #         logger.info("✅ Browser initialized successfully")

# # #     async def close(self):
# # #         # (Same close logic as before)
# # #         logger.info("🔚 Closing scanner...")
# # #         for context in self.contexts:
# # #             try:
# # #                 await context.close()
# # #             except Exception as e:
# # #                 logger.warning(f"⚠️ Error closing context: {e}")
# # #         if self.browser:
# # #             await self.browser.close()
# # #         if self.playwright:
# # #             await self.playwright.stop()
# # #         logger.info("✅ Scanner closed successfully")

# # #     async def create_consistent_context(self) -> BrowserContext:
# # #         # (Same create_consistent_context logic as before)
# # #         context = await self.browser.new_context(
# # #             user_agent=self.FIXED_USER_AGENT,
# # #             viewport=self.VIEWPORT,
# # #             timezone_id=self.TIMEZONE,
# # #             permissions=['geolocation', 'notifications'],
# # #             extra_http_headers={
# # #                 'Accept-Language': 'en-US,en;q=0.9',
# # #                 'Accept-Encoding': 'gzip, deflate, br',
# # #                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# # #                 'DNT': '1'
# # #             },
# # #             ignore_https_errors=True
# # #         )
# # #         self.contexts.append(context)
# # #         return context

# # #     async def run_crawl_and_scan(self, start_url: str, options: Dict = None) -> Dict:
# # #         """
# # #         NEW: Orchestrates a full-site crawl. Manages a queue and scans
# # #         pages one by one, collecting cookies and links.
# # #         """
# # #         if not options:
# # #             options = {}
            
# # #         scan_options = {
# # #             'wait_seconds': options.get('wait_seconds', 10),
# # #             'max_pages': options.get('max_pages', 300),
# # #             'deep_scroll': options.get('deep_scroll', True),
# # #             'banner_timeout': options.get('banner_timeout', 10),
# # #             'retry_banner_clicks': options.get('retry_banner_clicks', 3),
# # #             'accept_consent': options.get('accept_consent', False) # <-- Get this from options
# # #             # (other options as needed)
# # #         }
        
# # #         logger.info(f"🚀 Starting world-class CRAWL of: {start_url}")
# # #         crawl_start_time = time.time()
        
# # #         base_domain = self._get_base_domain(start_url)
        
# # #         crawl_queue = asyncio.Queue()
# # #         await crawl_queue.put(start_url)
        
# # #         visited_urls = {start_url}
# # #         all_page_results = []
        
# # #         context = await self.create_consistent_context()
# # #         page = await context.new_page()
        
# # #         network_cookies, xhr_cookies = [], []
# # #         await self._setup_network_monitoring(page, network_cookies, xhr_cookies)
        
# # #         consent_interactions = [] # Track consent across all pages
        
# # #         page_count = 0
        
# # #         try:
# # #             while not crawl_queue.empty() and page_count < scan_options['max_pages']:
# # #                 current_url = await crawl_queue.get()
# # #                 page_count += 1
# # #                 logger.info(f"📄 Scanning page {page_count}/{scan_options['max_pages']}: {current_url}")
                
# # #                 page_start_time = time.time()
# # #                 try:
# # #                     # Use the modified single-page scan function
# # #                     page_data = await self._scan_single_page(
# # #                         page, current_url, scan_options, consent_interactions
# # #                     )
                    
# # #                     page_duration = time.time() - page_start_time
                    
# # #                     # Store comprehensive results for this page
# # #                     page_result = {
# # #                         "url": current_url,
# # #                         "status": "COMPLETED",
# # #                         "duration_seconds": round(page_duration, 2),
# # #                         "cookies": await context.cookies([current_url]), # Get cookies for this URL
# # #                         "local_storage": page_data.get('local_storage', {}),
# # #                         "session_storage": page_data.get('session_storage', {}),
# # #                         "error": None
# # #                     }
# # #                     all_page_results.append(page_result)

# # #                     # --- Link Discovery ---
# # #                     found_links = page_data.get('links', [])
# # #                     for link in found_links:
# # #                         try:
# # #                             abs_link = urljoin(current_url, link)
# # #                             parsed_link = urlparse(abs_link)
                            
# # #                             # Clean fragment, params, query
# # #                             clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
                            
# # #                             # Check if it's an internal link and not yet visited
# # #                             if self._get_base_domain(clean_link) == base_domain and clean_link not in visited_urls:
# # #                                 # Check for common file extensions to ignore
# # #                                 if not any(clean_link.endswith(ext) for ext in ['.pdf', '.jpg', '.png', '.zip', '.css', '.js']):
# # #                                     visited_urls.add(clean_link)
# # #                                     await crawl_queue.put(clean_link)
                                    
# # #                         except Exception as e:
# # #                             logger.debug(f"Link processing error: {e}")

# # #                 except Exception as e:
# # #                     logger.warning(f"⚠️ Failed to scan page {current_url}: {e}")
# # #                     page_duration = time.time() - page_start_time
# # #                     all_page_results.append({
# # #                         "url": current_url,
# # #                         "status": "FAILED",
# # #                         "duration_seconds": round(page_duration, 2),
# # #                         "cookies": [], "local_storage": {}, "session_storage": {},
# # #                         "error": str(e)
# # #                     })
                
# # #                 # Clear cookies for the *current page* only, to simulate a fresh visit
# # #                 # This is a choice: alternatively, keep context to simulate user journey
# # #                 # For comprehensive discovery, clearing is often better.
# # #                 # await context.clear_cookies() # <-- Optional: decide on strategy

# # #             crawl_duration = time.time() - crawl_start_time
            
# # #             # Get ALL cookies from the entire context at the end
# # #             final_all_cookies = await context.cookies()
            
# # #             return {
# # #                 "scan_metadata": {
# # #                     "start_url": start_url,
# # #                     "base_domain": base_domain,
# # #                     "total_duration_seconds": round(crawl_duration, 2),
# # #                     "pages_scanned_count": page_count,
# # #                     "user_agent": self.FIXED_USER_AGENT,
# # #                     "scan_timestamp": time.time()
# # #                 },
# # #                 "page_results": all_page_results,
# # #                 "final_context_cookies": final_all_cookies, # All cookies found during the session
# # #                 "consent_interactions_count": len(consent_interactions),
# # #                 "network_cookies": network_cookies # For deep analysis
# # #             }

# # #         finally:
# # #             await context.close()
# # #             if context in self.contexts:
# # #                 self.contexts.remove(context)


# # #     async def _setup_network_monitoring(self, page: Page, network_cookies: List, xhr_cookies: List):
# # #         # (Same logic as before)
# # #         async def handle_response(response):
# # #             try:
# # #                 headers = await response.all_headers()
# # #                 set_cookie_header = headers.get('set-cookie')
# # #                 if set_cookie_header:
# # #                     network_cookies.append({'url': response.url, 'set_cookie_header': set_cookie_header})
# # #             except Exception as e:
# # #                 logger.debug(f"Network monitoring error: {e}")
# # #         page.on('response', handle_response)


# # #     async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
# # #         """
# # #         MODIFIED: Scans a single page, handles consent, scrolls,
# # #         and returns cookies, storage, AND links.
# # #         """
# # #         await page.goto(url, wait_until='domcontentloaded', timeout=90000)
        
# # #         await self._wait_for_dynamic_content(page)
        
# # #         if options['deep_scroll']:
# # #             await self._enhanced_auto_scroll(page)
        
# # #         # --- MODIFIED: Use the accept_consent option ---
# # #         if options['accept_consent']:
# # #             await self._advanced_consent_handling(
# # #                 page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
# # #             )
        
# # #         # Wait for all cookies to settle
# # #         await asyncio.sleep(options['wait_seconds'])
        
# # #         try:
# # #             js_cookies = await page.evaluate("document.cookie")
# # #         except Exception:
# # #             js_cookies = ""
        
# # #         local_storage = await page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))")
# # #         session_storage = await page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))")
        
# # #         # --- NEW: Extract all links ---
# # #         try:
# # #             links = await page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.href)")
# # #         except Exception as e:
# # #             logger.warning(f"Could not extract links from {url}: {e}")
# # #             links = []

# # #         return {
# # #             'js_cookies': js_cookies,
# # #             'local_storage': local_storage,
# # #             'session_storage': session_storage,
# # #             'links': links # Return discovered links
# # #         }

# # #     # ( _wait_for_dynamic_content, _enhanced_auto_scroll, 
# # #     #   _advanced_consent_handling, _get_base_domain
# # #     #   and other helpers remain exactly the same )
    
# # #     # --- REMOVED ---
# # #     # def _discover_important_pages(self, page: Page, base_url: str) -> List[str]:
# # #     #     # This function is no longer needed, as we do a real crawl.
# # #     #     pass
# # #     async def _wait_for_dynamic_content(self, page: Page):
# # #         """Wait for dynamic content to load (XHR, scripts, etc.)"""
# # #         try:
# # #             # Wait for network to be mostly idle
# # #             await page.wait_for_load_state('networkidle', timeout=20000)
            
# # #             # Additional wait for any remaining async operations
# # #             await page.wait_for_timeout(2000)
            
# # #         except Exception as e:
# # #             logger.debug(f"Dynamic content wait completed with: {e}")
            
# # #     async def _enhanced_auto_scroll(self, page: Page):
# # #         """Enhanced auto-scrolling to trigger all lazy-loaded content"""
        
# # #         logger.debug("🔄 Enhanced auto-scrolling...")
        
# # #         await page.evaluate("""
# # #         async () => {
# # #             const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
            
# # #             // Comprehensive scrolling strategy
# # #             const totalHeight = document.body.scrollHeight;
# # #             const viewportHeight = window.innerHeight;
# # #             const scrollStep = Math.max(100, viewportHeight / 4);
            
# # #             // Scroll down in steps
# # #             for (let y = 0; y < totalHeight; y += scrollStep) {
# # #                 window.scrollTo(0, y);
# # #                 await sleep(200);
# # #             }
            
# # #             // Final scroll to bottom
# # #             window.scrollTo(0, document.body.scrollHeight);
# # #             await sleep(500);
            
# # #             // Scroll to top
# # #             window.scrollTo(0, 0);
# # #             await sleep(500);
# # #         }
# # #         """)

# # #     async def _advanced_consent_handling(self, page: Page, timeout: int, retries: int, consent_interactions: List) -> bool:
# # #         """
# # #         World-class consent banner detection and handling
# # #         """
# # #         logger.info("🎯 Advanced consent banner detection...")
        
# # #         # Comprehensive selector list for consent banners
# # #         consent_selectors = [
# # #             # Generic accept buttons
# # #             'button:has-text("Accept")', 'button:has-text("Accept All")',
# # #             'button:has-text("Accept all")', 'button:has-text("I Accept")',
# # #             'button:has-text("Allow All")', 'button:has-text("Allow all")',
# # #             'button:has-text("Agree")', 'button:has-text("I Agree")',
# # #             'button:has-text("OK")', 'button:has-text("Got it")',
# # #             'button:has-text("Continue")', 'button:has-text("Proceed")',
            
# # #             # Attribute-based selectors
# # #             '[data-testid*="accept"]', '[data-cy*="accept"]', 
# # #             '[id*="accept"]', '[class*="accept"]',
# # #             '[data-testid*="consent"]', '[data-cy*="consent"]',
# # #             '[id*="consent"]', '[class*="consent"]',
# # #             '[data-testid*="cookie"]', '[data-cy*="cookie"]',
# # #             '[id*="cookie"]', '[class*="cookie"]',
            
# # #             # Common consent management platforms
# # #             '[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
# # #             '[class*="optanon-allow-all"]',
# # #             '[id*="truste-consent-button"]',
            
# # #             # OneTrust specific
# # #             '#onetrust-accept-btn-handler',
# # #         ]
        
# # #         iframe_selectors = [
# # #             'iframe[src*="consent"]',
# # #             'iframe[src*="cookie"]',
# # #             'iframe[id*="consent"]',
# # #         ]
        
# # #         success = False
        
# # #         for attempt in range(retries):
# # #             logger.debug(f"🎯 Consent detection attempt {attempt + 1}/{retries}")
            
# # #             try:
# # #                 # First check main page
# # #                 for selector in consent_selectors:
# # #                     try:
# # #                         element = page.locator(selector).first
# # #                         if await element.is_visible(timeout=2000):
# # #                             logger.info(f"✅ Found consent button: {selector}")
                            
# # #                             consent_interactions.append({
# # #                                 'selector': selector,
# # #                                 'attempt': attempt + 1,
# # #                                 'timestamp': time.time(),
# # #                                 'type': 'main_page'
# # #                             })
                            
# # #                             await element.click(timeout=5000)
# # #                             await page.wait_for_timeout(2000) # Wait for response
# # #                             success = True
# # #                             break
                            
# # #                     except Exception:
# # #                         continue
                
# # #                 if success:
# # #                     break
                
# # #                 # Check iframes
# # #                 for iframe_selector in iframe_selectors:
# # #                     try:
# # #                         iframe = page.locator(iframe_selector).first
# # #                         if await iframe.is_visible(timeout=1000):
# # #                             frame = await iframe.content_frame()
# # #                             if frame:
# # #                                 for selector in consent_selectors[:10]:
# # #                                     try:
# # #                                         element = frame.locator(selector).first
# # #                                         if await element.is_visible(timeout=1000):
# # #                                             logger.info(f"✅ Found consent button in iframe: {selector}")
                                            
# # #                                             consent_interactions.append({
# # #                                                 'selector': selector,
# # #                                                 'attempt': attempt + 1,
# # #                                                 'timestamp': time.time(),
# # #                                                 'type': 'iframe',
# # #                                                 'iframe_selector': iframe_selector
# # #                                             })
                                            
# # #                                             await element.click(timeout=5000)
# # #                                             await page.wait_for_timeout(2000)
# # #                                             success = True
# # #                                             break
# # #                                     except Exception:
# # #                                         continue
# # #                             if success:
# # #                                 break
# # #                     except Exception:
# # #                         continue
                
# # #                 if success:
# # #                     break
                    
# # #                 if attempt < retries - 1:
# # #                     await asyncio.sleep(2)
                    
# # #             except Exception as e:
# # #                 logger.debug(f"Consent attempt {attempt + 1} error: {e}")
        
# # #         if success:
# # #             logger.info("🎉 Successfully interacted with consent banner")
# # #         else:
# # #             logger.info("ℹ️ No consent banner found or interaction failed")
            
# # #         return success
    
# # #     def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
# # #         # (Same logic as before)
# # #         seen = set()
# # #         deduplicated = []
# # #         for cookie in cookies:
# # #             identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}"
# # #             if identifier not in seen:
# # #                 seen.add(identifier)
# # #                 deduplicated.append(cookie)
# # #         return deduplicated

# # #     def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
# # #         # (Same logic as before)
# # #         standardized = []
# # #         base_domain = self._get_base_domain(base_url)
# # #         for cookie in cookies:
# # #             try:
# # #                 cookie_domain = cookie.get('domain', '').lstrip('.')
# # #                 if not cookie_domain:
# # #                     cookie_domain = base_domain
                
# # #                 standardized.append({
# # #                     'name': cookie.get('name', ''),
# # #                     'value': cookie.get('value', ''),
# # #                     'domain': cookie_domain,
# # #                     'path': cookie.get('path', '/'),
# # #                     'expires': cookie.get('expires', -1),
# # #                     'httpOnly': cookie.get('httpOnly', False),
# # #                     'secure': cookie.get('secure', False),
# # #                     'sameSite': cookie.get('sameSite', 'Lax'),
# # #                     'is_third_party': cookie_domain != base_domain,
# # #                     'base_domain': self._get_base_domain(cookie_domain),
# # #                     'size': len(cookie.get('value', '')),
# # #                     'timestamp': time.time()
# # #                 })
# # #             except Exception as e:
# # #                 logger.debug(f"Cookie standardization error: {e}")
# # #                 continue
# # #         return standardized

# # #     def _get_base_domain(self, url_or_domain: str) -> str:
# # #         # (Same logic as before)
# # #         try:
# # #             extracted = tldextract.extract(url_or_domain, cache_dir="/tmp")
# # #             if extracted.domain and extracted.suffix:
# # #                 return f"{extracted.domain}.{extracted.suffix}"
# # #             return extracted.domain or url_or_domain
# # #         except Exception:
# # #             return url_or_domain


# # # scanner.py - World-class cookie scanner using Playwright with enhanced features

# # import asyncio
# # import time
# # import logging
# # from typing import List, Dict, Optional, Set
# # from urllib.parse import urljoin, urlparse
# # from playwright.async_api import async_playwright, Browser, BrowserContext, Page
# # import json
# # import hashlib
# # import tldextract
# # import sys # For platform check

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # # Handle potential asyncio policy issues on Windows for local dev
# # if sys.platform == 'win32':
# #     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# # class PlaywrightScanner:
# #     """
# #     World-class cookie scanner designed to compete with CookieYes and Termly,
# #     now featuring full-site crawling capabilities.
# #     """

# #     # Fixed configuration for consistency across Docker/Linux environments
# #     FIXED_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
# #     VIEWPORT = {'width': 1920, 'height': 1080}
# #     TIMEZONE = 'IST' # Assuming India Standard Time based on user context


# #     def __init__(self):
# #         self.browser: Optional[Browser] = None
# #         self.playwright: Optional[async_playwright] = None
# #         self.contexts: List[BrowserContext] = []

# #     async def initialize(self, headless: bool = True):
# #         """Initialize browser with locked configuration for consistency"""
# #         logger.info("🔧 Initializing world-class cookie scanner...")

# #         self.playwright = await async_playwright().start()

# #         # Launch with locked configuration for Docker consistency
# #         try:
# #             self.browser = await self.playwright.chromium.launch(
# #                 headless=headless,
# #                 args=[
# #                     '--no-sandbox',
# #                     '--disable-setuid-sandbox',
# #                     '--disable-dev-shm-usage',
# #                     '--disable-web-security', # Be cautious with this in production if not needed
# #                     '--disable-features=VizDisplayCompositor', # May help in headless stability
# #                     '--disable-background-timer-throttling',
# #                     '--disable-backgrounding-occluded-windows',
# #                     '--disable-renderer-backgrounding',
# #                     '--lang=en-US' # Set language consistently
# #                 ]
# #             )
# #             logger.info("✅ Browser initialized successfully")
# #         except Exception as e:
# #             logger.error(f"❌ Failed to launch browser: {e}")
# #             await self.close() # Clean up playwright if launch fails
# #             raise # Re-raise the exception

# #     async def close(self):
# #         """Gracefully close all contexts and browser"""
# #         logger.info("🔚 Closing scanner...")

# #         # Close all contexts
# #         for context in self.contexts[:]: # Iterate over a copy
# #             try:
# #                 await context.close()
# #                 self.contexts.remove(context)
# #             except Exception as e:
# #                 logger.warning(f"⚠️ Error closing context: {e}")
# #                 # Attempt to remove context even if close failed
# #                 if context in self.contexts:
# #                     self.contexts.remove(context)

# #         if self.browser:
# #             try:
# #                 await self.browser.close()
# #                 self.browser = None
# #             except Exception as e:
# #                 logger.error(f"❌ Error closing browser: {e}")

# #         if self.playwright:
# #             try:
# #                 await self.playwright.stop()
# #                 self.playwright = None
# #             except Exception as e:
# #                 logger.error(f"❌ Error stopping Playwright: {e}")

# #         logger.info("✅ Scanner closed successfully")

# #     async def create_consistent_context(self) -> BrowserContext:
# #         """Create browser context with locked settings for consistency"""
# #         if not self.browser:
# #              logger.error("❌ Cannot create context, browser is not initialized.")
# #              raise RuntimeError("Browser not initialized. Call initialize() first.")

# #         context = await self.browser.new_context(
# #             user_agent=self.FIXED_USER_AGENT,
# #             viewport=self.VIEWPORT,
# #             timezone_id=self.TIMEZONE,
# #             permissions=['geolocation', 'notifications'], # Adjust permissions as needed
# #             extra_http_headers={
# #                 'Accept-Language': 'en-US,en;q=0.9',
# #                 'Accept-Encoding': 'gzip, deflate, br',
# #                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# #                 'DNT': '1' # Do Not Track header
# #             },
# #             ignore_https_errors=True # Use with caution
# #         )

# #         self.contexts.append(context)
# #         return context

# #     async def run_crawl_and_scan(self, start_url: str, options: Dict = None) -> Dict:
# #         """
# #         Orchestrates a full-site crawl. Manages a queue and scans
# #         pages one by one, collecting cookies and links.
# #         """
# #         if not options:
# #             options = {}

# #         # Default scan options with values from input options if provided
# #         scan_options = {
# #             'wait_seconds': options.get('wait_seconds', 10),
# #             'max_pages': options.get('max_pages', 5),
# #             'deep_scroll': options.get('deep_scroll', True),
# #             'banner_timeout': options.get('banner_timeout', 10),
# #             'retry_banner_clicks': options.get('retry_banner_clicks', 3),
# #             'accept_consent': options.get('accept_consent', False) # Use provided option
# #             # Add other options here if needed, e.g., 'simulate_login'
# #         }

# #         logger.info(f"🚀 Starting world-class CRAWL of: {start_url} with options: {scan_options}")
# #         crawl_start_time = time.time()

# #         try:
# #             base_domain = self._get_base_domain(start_url)
# #             if not base_domain:
# #                 raise ValueError(f"Could not extract base domain from start URL: {start_url}")
# #         except Exception as e:
# #              logger.error(f"❌ Error extracting base domain from {start_url}: {e}")
# #              raise ValueError(f"Invalid start URL: {start_url}") from e


# #         crawl_queue = asyncio.Queue()
# #         await crawl_queue.put(start_url)

# #         visited_urls: Set[str] = {start_url} # Use a set for faster lookups
# #         all_page_results = []

# #         context = await self.create_consistent_context()
# #         page = await context.new_page()

# #         network_cookies: List[Dict] = []
# #         # xhr_cookies are less critical for cookie *discovery*, focus on set-cookie headers
# #         await self._setup_network_monitoring(page, network_cookies)

# #         consent_interactions: List[Dict] = [] # Track consent across all pages

# #         page_count = 0
# #         error_count = 0

# #         try:
# #             while not crawl_queue.empty() and page_count < scan_options['max_pages']:
# #                 try:
# #                     current_url = await asyncio.wait_for(crawl_queue.get(), timeout=10.0) # Timeout for queue get
# #                 except asyncio.TimeoutError:
# #                     logger.warning("⚠️ Timed out waiting for URL from crawl queue.")
# #                     continue # Skip if queue seems stuck

# #                 page_count += 1
# #                 logger.info(f"📄 Scanning page {page_count}/{scan_options['max_pages']}: {current_url}")

# #                 page_start_time = time.time()
# #                 page_data = None
# #                 try:
# #                     # Use the modified single-page scan function
# #                     page_data = await self._scan_single_page(
# #                         page, current_url, scan_options, consent_interactions
# #                     )

# #                     page_duration = time.time() - page_start_time

# #                     # Get cookies specific to this page's context/origin if possible
# #                     # Playwright's context.cookies() gets ALL cookies. We filter later.
# #                     # For now, just store the raw data associated with this page scan.
# #                     page_cookies_raw = await context.cookies([current_url])


# #                     page_result = {
# #                         "url": current_url,
# #                         "status": "COMPLETED",
# #                         "duration_seconds": round(page_duration, 2),
# #                         "cookies": page_cookies_raw, # Store raw cookies found *during* this page visit
# #                         "local_storage": page_data.get('local_storage', {}),
# #                         "session_storage": page_data.get('session_storage', {}),
# #                         "error": None
# #                     }
# #                     all_page_results.append(page_result)

# #                     # --- Link Discovery ---
# #                     found_links = page_data.get('links', [])
# #                     added_to_queue = 0
# #                     for link in found_links:
# #                         if crawl_queue.qsize() + page_count + added_to_queue >= scan_options['max_pages']:
# #                             break # Don't add more links than max_pages

# #                         try:
# #                             # Resolve relative links and handle potential errors
# #                             abs_link = urljoin(current_url, link)
# #                             parsed_link = urlparse(abs_link)

# #                             # Basic validity check and remove fragment
# #                             if parsed_link.scheme in ['http', 'https'] and parsed_link.netloc:
# #                                 clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
# #                                 # Remove trailing slash for consistency
# #                                 if clean_link.endswith('/') and len(clean_link) > 1:
# #                                      clean_link = clean_link[:-1]

# #                                 # Check if it's an internal link and not yet visited/queued
# #                                 if self._get_base_domain(clean_link) == base_domain and clean_link not in visited_urls:
# #                                     # Ignore common non-HTML file extensions
# #                                     ignored_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', '.xml', '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.avi']
# #                                     if not any(parsed_link.path.lower().endswith(ext) for ext in ignored_extensions):
# #                                         visited_urls.add(clean_link)
# #                                         await crawl_queue.put(clean_link)
# #                                         added_to_queue += 1

# #                         except Exception as link_e:
# #                             logger.debug(f"Link processing error for '{link}' on {current_url}: {link_e}")

# #                 except Exception as page_scan_e:
# #                     error_count += 1
# #                     logger.warning(f"⚠️ Failed to scan page {current_url}: {page_scan_e}", exc_info=True) # Log traceback
# #                     page_duration = time.time() - page_start_time
# #                     all_page_results.append({
# #                         "url": current_url,
# #                         "status": "FAILED",
# #                         "duration_seconds": round(page_duration, 2),
# #                         "cookies": [], "local_storage": {}, "session_storage": {},
# #                         "error": str(page_scan_e)
# #                     })
# #                     # Optional: Add a delay or retry mechanism here if needed

# #                 # Optional: Small delay between page scans to avoid overwhelming the server
# #                 await asyncio.sleep(1)

# #             crawl_duration = time.time() - crawl_start_time

# #             # Get ALL cookies from the entire context at the end
# #             # These represent the cumulative cookies set during the whole crawl
# #             final_all_context_cookies = await context.cookies()

# #             # Standardize the final list of cookies
# #             standardized_final_cookies = self._standardize_cookies(final_all_context_cookies, start_url)
# #             deduplicated_final_cookies = self._deduplicate_cookies(standardized_final_cookies)


# #             logger.info(f"✅ Crawl completed: Scanned {page_count} pages ({error_count} errors) in {crawl_duration:.2f}s. Found {len(deduplicated_final_cookies)} unique cookies.")

# #             return {
# #                 "scan_metadata": {
# #                     "start_url": start_url,
# #                     "base_domain": base_domain,
# #                     "total_duration_seconds": round(crawl_duration, 2),
# #                     "pages_scanned_count": page_count,
# #                     "scan_errors": error_count,
# #                     "user_agent": self.FIXED_USER_AGENT,
# #                     "scan_timestamp": time.time()
# #                 },
# #                 "page_results": all_page_results, # Contains raw cookies/storage per page
# #                  # Contains standardized, deduplicated cookies from the whole session
# #                 "final_unique_cookies": deduplicated_final_cookies,
# #                 "consent_interactions_count": len(consent_interactions),
# #                 "network_cookies_count": len(network_cookies) # Count for info
# #             }

# #         finally:
# #             # Ensure context is closed even if errors occur
# #              if context:
# #                  try:
# #                      await context.close()
# #                      if context in self.contexts:
# #                           self.contexts.remove(context)
# #                  except Exception as e:
# #                       logger.warning(f"⚠️ Error closing context during cleanup: {e}")


# #     async def _setup_network_monitoring(self, page: Page, network_cookies: List):
# #         """Set up network request monitoring for Set-Cookie headers."""

# #         async def handle_response(response):
# #             try:
# #                 # Check for Set-Cookie header
# #                 set_cookie_headers = await response.header_values('set-cookie')
# #                 if set_cookie_headers:
# #                     for header in set_cookie_headers:
# #                          network_cookies.append({
# #                              'url': response.url,
# #                              'set_cookie_header': header,
# #                              'status': response.status,
# #                              'timestamp': time.time()
# #                          })
# #             except Exception as e:
# #                 # Can be noisy, log as debug
# #                 logger.debug(f"Network monitoring error processing response for {response.url}: {e}")

# #         page.on('response', handle_response)


# #     async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
# #         """
# #         Scans a single page, handles consent, scrolls,
# #         and returns cookies, storage, AND links found on the page.
# #         """
# #         logger.debug(f"Navigating to: {url}")
# #         # Increased timeout for navigation and use 'load' state which waits for more resources
# #         await page.goto(url, wait_until='load', timeout=60000)

# #         # Wait for initial dynamic content/network activity to potentially settle
# #         await self._wait_for_dynamic_content(page)

# #         # Handle consent banner *before* scrolling, as scroll might hide it
# #         if options.get('accept_consent', False):
# #             await self._advanced_consent_handling(
# #                 page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
# #             )
# #             # Wait a bit after consent interaction for cookies to potentially be set
# #             await asyncio.sleep(2)

# #         # Enhanced scrolling
# #         if options.get('deep_scroll', True):
# #             await self._enhanced_auto_scroll(page)
# #             # Wait after scrolling for lazy-loaded content to potentially set cookies
# #             await self._wait_for_dynamic_content(page) # Check network again after scroll

# #         # Final wait period for everything to settle before collecting data
# #         logger.debug(f"Waiting {options['wait_seconds']}s for cookies on {url}")
# #         await asyncio.sleep(options['wait_seconds'])

# #         # --- Data Collection ---
# #         js_cookies_str = ""
# #         local_storage_data = {}
# #         session_storage_data = {}
# #         page_links = []

# #         try:
# #             js_cookies_str = await page.evaluate("() => document.cookie")
# #         except Exception as e:
# #             logger.warning(f"Could not get JS cookies from {url}: {e}")

# #         try:
# #             local_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))")
# #         except Exception as e:
# #             logger.warning(f"Could not get Local Storage from {url}: {e}")

# #         try:
# #             session_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))")
# #         except Exception as e:
# #             logger.warning(f"Could not get Session Storage from {url}: {e}")

# #         try:
# #             # Get href attribute directly for robustness
# #             page_links = await page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
# #             # Filter out null/empty hrefs that might come from the evaluate call
# #             page_links = [link for link in page_links if link]
# #         except Exception as e:
# #             logger.warning(f"Could not extract links from {url}: {e}")

# #         return {
# #             'js_cookies': js_cookies_str,
# #             'local_storage': local_storage_data,
# #             'session_storage': session_storage_data,
# #             'links': page_links # Return discovered links (href attributes)
# #         }

# #     async def _wait_for_dynamic_content(self, page: Page):
# #         """Wait for dynamic content to load (XHR, scripts, etc.)"""
# #         try:
# #             # Wait for network to be mostly idle (adjust connections count if needed)
# #             logger.debug(f"Waiting for network idle on {page.url}...")
# #             await page.wait_for_load_state('networkidle', timeout=15000)
# #             logger.debug(f"Network idle detected on {page.url}.")
# #             # Short additional wait
# #             await page.wait_for_timeout(1000)
# #         except Exception as e:
# #             # Timeouts are expected if page is constantly active, log as debug
# #             logger.debug(f"Wait for dynamic content/networkidle finished or timed out for {page.url}: {e}")


# #     async def _enhanced_auto_scroll(self, page: Page):
# #         """Enhanced auto-scrolling to trigger lazy-loaded content"""
# #         logger.debug(f"Performing enhanced scroll on {page.url}")
# #         try:
# #             await page.evaluate("""
# #             async () => {
# #                 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
# #                 let totalHeight = 0;
# #                 const distance = 100; // Scroll distance per step
# #                 const maxScrolls = 100; // Limit scrolls to prevent infinite loops
# #                 let scrolls = 0;

# #                 while (scrolls < maxScrolls) {
# #                     const scrollHeight = document.body.scrollHeight;
# #                     window.scrollBy(0, distance);
# #                     await sleep(100); // Wait for potential content loading
# #                     totalHeight += distance;
# #                     scrolls++;

# #                     // Break if we've reached the bottom (or didn't scroll further)
# #                     if (window.innerHeight + window.scrollY >= scrollHeight || scrollHeight === document.body.scrollHeight) {
# #                        // Optional: one final scroll to be sure
# #                        window.scrollTo(0, document.body.scrollHeight);
# #                        await sleep(200);
# #                        break;
# #                     }
# #                 }
# #                 // Scroll back to top
# #                 window.scrollTo(0, 0);
# #                 await sleep(200);
# #             }
# #             """)
# #             logger.debug(f"Finished enhanced scroll on {page.url}")
# #         except Exception as e:
# #              logger.warning(f"Error during enhanced scroll on {page.url}: {e}")


# #     async def _advanced_consent_handling(self, page: Page, timeout_sec: int, retries: int, consent_interactions: List) -> bool:
# #         """
# #         Attempts to find and click common "Accept All"-style consent buttons.
# #         """
# #         logger.info(f"🎯 Attempting advanced consent banner interaction on {page.url}")
# #         timeout_ms = timeout_sec * 1000 # Playwright uses milliseconds

# #         # Prioritized list of selectors - more specific or common ones first
# #         consent_selectors = [
# #             # Common CMP IDs/Classes (High confidence)
# #             '#onetrust-accept-btn-handler',
# #             '[id*="consent"] button[id*="accept"]',
# #              'button[id*="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
# #             'button[class*="accept-all"]', 'button[class*="optanon-allow-all"]',
# #             'button[id*="accept-all"]', 'button[data-accept-action]',
# #             'button[data-testid*="accept"]', 'button[data-cy*="accept"]',
# #             'button[data-gdpr-single-choice-accept]',

# #             # Common Text Patterns (Medium confidence)
# #             'button:text-matches("Accept all", "i")',
# #             'button:text-matches("Allow all", "i")',
# #             'button:text-matches("Agree", "i")',
# #             'button:text-matches("Accept", "i")', # More generic, lower priority
# #             'button:text-matches("OK", "i")',
# #             'button:text-matches("Got it", "i")',

# #             # Attributes containing keywords
# #             'button[id*="cookie"]', 'button[class*="cookie"]',
# #             'button[id*="consent"]', 'button[class*="consent"]',

# #             # Role-based + Text
# #             '[role="dialog"] button:text-matches("Accept", "i")',
# #             '[role="banner"] button:text-matches("Accept", "i")',

# #             # More Language Variations (add as needed)
# #             'button:text-matches("Accepter", "i")', # French
# #             'button:text-matches("Aceptar", "i")',  # Spanish
# #             'button:text-matches("Akzeptieren", "i")', # German
# #         ]

# #         # Simplified iframe checking - look for common names/ids
# #         iframe_selectors = [
# #              'iframe[id*="consent"]', 'iframe[name*="consent"]',
# #              'iframe[id*="cookie"]', 'iframe[name*="cookie"]',
# #              'iframe[title*="consent" i]', 'iframe[title*="cookie" i]'
# #         ]

# #         success = False

# #         for attempt in range(retries):
# #             logger.debug(f"Consent detection attempt {attempt + 1}/{retries} on {page.url}")
# #             clicked_in_attempt = False

# #             # 1. Check Main Page Frame
# #             for selector in consent_selectors:
# #                 try:
# #                     element = page.locator(selector).first # Target only the first match
# #                     # Check visibility with a shorter timeout within the loop
# #                     if await element.is_visible(timeout=1000):
# #                         logger.info(f"✅ Found potential consent button: {selector}")
# #                         await element.click(timeout=3000) # Short click timeout
# #                         logger.info(f"✅ Clicked consent button: {selector}")
# #                         consent_interactions.append({
# #                             'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(), 'type': 'main_page'
# #                         })
# #                         clicked_in_attempt = True
# #                         await page.wait_for_timeout(1500) # Wait briefly for banner to disappear/cookies to set
# #                         break # Assume first found accept button is enough
# #                 except Exception as e:
# #                     logger.debug(f"Selector '{selector}' not found/visible or click failed: {e}")
# #                     continue # Try next selector
# #             if clicked_in_attempt:
# #                 success = True
# #                 break # Exit retry loop if clicked on main page

# #             # 2. Check Iframes (only if not found on main page in this attempt)
# #             logger.debug("Checking iframes for consent buttons...")
# #             for frame_selector in iframe_selectors:
# #                  try:
# #                       frame_locator = page.locator(frame_selector).first
# #                       if await frame_locator.is_visible(timeout=500): # Quick check if iframe exists
# #                             frame = await frame_locator.content_frame()
# #                             if frame:
# #                                 logger.debug(f"Searching within iframe: {frame_selector}")
# #                                 for selector in consent_selectors[:15]: # Try top selectors in iframe
# #                                      try:
# #                                           element = frame.locator(selector).first
# #                                           if await element.is_visible(timeout=1000):
# #                                                 logger.info(f"✅ Found consent button in iframe '{frame_selector}': {selector}")
# #                                                 await element.click(timeout=3000)
# #                                                 logger.info(f"✅ Clicked consent button in iframe: {selector}")
# #                                                 consent_interactions.append({
# #                                                     'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(),
# #                                                     'type': 'iframe', 'iframe_selector': frame_selector
# #                                                 })
# #                                                 clicked_in_attempt = True
# #                                                 await page.wait_for_timeout(1500)
# #                                                 break # Found and clicked in iframe
# #                                      except Exception as e_iframe:
# #                                           logger.debug(f"Selector '{selector}' in iframe '{frame_selector}' failed: {e_iframe}")
# #                                           continue
# #                             if clicked_in_attempt: break # Stop checking other iframes
# #                  except Exception as e_frame_check:
# #                       logger.debug(f"Iframe check failed for '{frame_selector}': {e_frame_check}")
# #                       continue
# #                  if clicked_in_attempt: break # Stop checking other iframe types

# #             if clicked_in_attempt:
# #                 success = True
# #                 break # Exit retry loop if clicked in iframe

# #             # Wait before next retry if nothing was clicked in this attempt
# #             if not clicked_in_attempt and attempt < retries - 1:
# #                 logger.debug(f"Consent button not found in attempt {attempt + 1}, retrying...")
# #                 await asyncio.sleep(1) # Short delay before retry

# #         if success:
# #             logger.info(f"🎉 Successfully interacted with a consent banner on {page.url}")
# #         else:
# #             logger.info(f"ℹ️ No interactable consent banner found after {retries} attempts on {page.url}")

# #         return success

# #     def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
# #         """Remove duplicate cookies based on name, domain, and path."""
# #         seen: Set[str] = set()
# #         deduplicated = []
# #         for cookie in cookies:
# #             # Create a more robust unique identifier
# #             identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
# #             if identifier not in seen:
# #                 seen.add(identifier)
# #                 deduplicated.append(cookie)

# #         logger.debug(f"🔄 Deduplicated {len(cookies)} -> {len(deduplicated)} cookies based on name/domain/path")
# #         return deduplicated

# #     def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
# #         """Standardize cookie data format for consistency and add metadata."""
# #         standardized = []
# #         try:
# #             url_parts = urlparse(base_url)
# #             site_base_domain = self._get_base_domain(url_parts.netloc)
# #             if not site_base_domain: site_base_domain = url_parts.netloc # Fallback
# #         except Exception:
# #              logger.warning(f"Could not parse base_url {base_url} for standardization, using fallback.")
# #              site_base_domain = base_url # Raw fallback

# #         for cookie in cookies:
# #             try:
# #                 # Normalize domain (remove leading dot)
# #                 cookie_domain = cookie.get('domain', '').lstrip('.')
# #                 # If domain is missing, assume it's for the base domain of the site
# #                 if not cookie_domain:
# #                     cookie_domain = site_base_domain

# #                 cookie_base_domain = self._get_base_domain(cookie_domain)

# #                 # Determine SameSite (handle None or missing)
# #                 samesite = cookie.get('sameSite')
# #                 if samesite not in ['Strict', 'Lax', 'None']:
# #                      samesite = 'Lax' # Default according to modern browser standards if invalid/missing

# #                 standardized_cookie = {
# #                     'name': cookie.get('name', ''),
# #                     'value': cookie.get('value', ''),
# #                     'domain': cookie_domain, # The full domain from the cookie
# #                     'path': cookie.get('path', '/'),
# #                     'expires': cookie.get('expires', -1), # -1 indicates session cookie in Playwright
# #                     'httpOnly': cookie.get('httpOnly', False),
# #                     'secure': cookie.get('secure', False),
# #                     'sameSite': samesite,
# #                     # --- Added Metadata ---
# #                     'is_third_party': cookie_base_domain != site_base_domain if site_base_domain and cookie_base_domain else False,
# #                     'base_domain': cookie_base_domain or cookie_domain, # Calculated base domain
# #                     'size_bytes': len(cookie.get('name', '').encode('utf-8') + b'=' + cookie.get('value', '').encode('utf-8')),
# #                     'timestamp': time.time() # Timestamp when processed by scanner
# #                 }
# #                 standardized.append(standardized_cookie)

# #             except Exception as e:
# #                 logger.warning(f"Cookie standardization error for cookie '{cookie.get('name')}': {e}")
# #                 continue

# #         return standardized

# #     def _get_base_domain(self, url_or_domain: str) -> str:
# #         """
# #         Accurately extract the registrable domain (e.g., example.com, example.co.uk)
# #         using tldextract. Returns None if extraction fails badly.
# #         """
# #         if not url_or_domain or not isinstance(url_or_domain, str):
# #              return ""
# #         try:

# #             extracted = tldextract.extract(url_or_domain, include_psl_private_domains=True) # <--- FIX HERE
# #             if extracted.registered_domain:
# #                 return extracted.registered_domain
# #             elif extracted.domain:
# #                  return extracted.domain
# #             else:
# #                  # If it looks like an IP address, return it as is? Or empty? Decide policy.
# #                  # Let's return empty if it's likely just a TLD or invalid.
# #                  return ""
# #         except Exception as e:
# #             logger.error(f"Error extracting base domain from '{url_or_domain}': {e}")
# #             # Try a simple split as a last resort, might be wrong for .co.uk etc.
# #             parts = url_or_domain.split('.')
# #             if len(parts) >= 2:
# #                  return ".".join(parts[-2:])
# #             return url_or_domain # Return original if splitting fails


# import asyncio
# import time
# import logging
# from typing import List, Dict, Optional, Set
# from urllib.parse import urljoin, urlparse
# from playwright.async_api import async_playwright, Browser, BrowserContext, Page
# import json
# import hashlib
# import tldextract
# import sys # For platform check

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Handle potential asyncio policy issues on Windows for local dev
# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# class PlaywrightScanner:
#     """
#     World-class cookie scanner designed to compete with CookieYes and Termly,
#     now featuring full-site crawling capabilities.
#     """

#     # Fixed configuration for consistency across Docker/Linux environments
#     FIXED_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#     VIEWPORT = {'width': 1920, 'height': 1080}
#     TIMEZONE = 'IST' # Assuming India Standard Time based on user context


#     def _init_(self):
#         self.browser: Optional[Browser] = None
#         self.playwright: Optional[async_playwright] = None
#         self.contexts: List[BrowserContext] = []

#     async def initialize(self, headless: bool = True):
#         """Initialize browser with locked configuration for consistency"""
#         logger.info("🔧 Initializing world-class cookie scanner...")

#         self.playwright = await async_playwright().start()

#         # Launch with locked configuration for Docker consistency
#         try:
#             self.browser = await self.playwright.chromium.launch(
#                 headless=headless,
#                 args=[
#                     '--no-sandbox',
#                     '--disable-setuid-sandbox',
#                     '--disable-dev-shm-usage',
#                     '--disable-web-security', # Be cautious with this in production if not needed
#                     '--disable-features=VizDisplayCompositor', # May help in headless stability
#                     '--disable-background-timer-throttling',
#                     '--disable-backgrounding-occluded-windows',
#                     '--disable-renderer-backgrounding',
#                     '--lang=en-US' # Set language consistently
#                 ]
#             )
#             logger.info("✅ Browser initialized successfully")
#         except Exception as e:
#             logger.error(f"❌ Failed to launch browser: {e}")
#             await self.close() # Clean up playwright if launch fails
#             raise # Re-raise the exception

#     async def close(self):
#         """Gracefully close all contexts and browser"""
#         logger.info("🔚 Closing scanner...")

#         # Close all contexts
#         for context in self.contexts[:]: # Iterate over a copy
#             try:
#                 await context.close()
#                 self.contexts.remove(context)
#             except Exception as e:
#                 logger.warning(f"⚠ Error closing context: {e}")
#                 # Attempt to remove context even if close failed
#                 if context in self.contexts:
#                     self.contexts.remove(context)

#         if self.browser:
#             try:
#                 await self.browser.close()
#                 self.browser = None
#             except Exception as e:
#                 logger.error(f"❌ Error closing browser: {e}")

#         if self.playwright:
#             try:
#                 await self.playwright.stop()
#                 self.playwright = None
#             except Exception as e:
#                 logger.error(f"❌ Error stopping Playwright: {e}")

#         logger.info("✅ Scanner closed successfully")

#     async def create_consistent_context(self) -> BrowserContext:
#         """Create browser context with locked settings for consistency"""
#         if not self.browser:
#              logger.error("❌ Cannot create context, browser is not initialized.")
#              raise RuntimeError("Browser not initialized. Call initialize() first.")

#         context = await self.browser.new_context(
#             user_agent=self.FIXED_USER_AGENT,
#             viewport=self.VIEWPORT,
#             timezone_id=self.TIMEZONE,
#             permissions=['geolocation', 'notifications'], # Adjust permissions as needed
#             extra_http_headers={
#                 'Accept-Language': 'en-US,en;q=0.9',
#                 'Accept-Encoding': 'gzip, deflate, br',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
#                 'DNT': '1' # Do Not Track header
#             },
#             ignore_https_errors=True # Use with caution
#         )

#         self.contexts.append(context)
#         return context

#     async def run_crawl_and_scan(self, start_url: str, options: Dict = None) -> Dict:
#         """
#         Orchestrates a full-site crawl. Manages a queue and scans
#         pages one by one, collecting cookies and links.
#         """
#         if not options:
#             options = {}

#         # Default scan options with values from input options if provided
#         scan_options = {
#             'wait_seconds': options.get('wait_seconds', 10),
#             'max_pages': options.get('max_pages', 5),
#             'deep_scroll': options.get('deep_scroll', True),
#             'banner_timeout': options.get('banner_timeout', 10),
#             'retry_banner_clicks': options.get('retry_banner_clicks', 3),
#             'accept_consent': options.get('accept_consent', False) # Use provided option
#             # Add other options here if needed, e.g., 'simulate_login'
#         }

#         logger.info(f"🚀 Starting world-class CRAWL of: {start_url} with options: {scan_options}")
#         crawl_start_time = time.time()

#         try:
#             base_domain = self._get_base_domain(start_url)
#             if not base_domain:
#                 raise ValueError(f"Could not extract base domain from start URL: {start_url}")
#         except Exception as e:
#              logger.error(f"❌ Error extracting base domain from {start_url}: {e}")
#              raise ValueError(f"Invalid start URL: {start_url}") from e


#         crawl_queue = asyncio.Queue()
#         await crawl_queue.put(start_url)

#         visited_urls: Set[str] = {start_url} # Use a set for faster lookups
#         all_page_results = []

#         context = await self.create_consistent_context()
#         page = await context.new_page()

#         network_cookies: List[Dict] = []
#         # xhr_cookies are less critical for cookie discovery, focus on set-cookie headers
#         await self._setup_network_monitoring(page, network_cookies)

#         consent_interactions: List[Dict] = [] # Track consent across all pages

#         page_count = 0
#         error_count = 0

#         try:
#             while not crawl_queue.empty() and page_count < scan_options['max_pages']:
#                 try:
#                     current_url = await asyncio.wait_for(crawl_queue.get(), timeout=10.0) # Timeout for queue get
#                 except asyncio.TimeoutError:
#                     logger.warning("⚠ Timed out waiting for URL from crawl queue.")
#                     continue # Skip if queue seems stuck

#                 page_count += 1
#                 logger.info(f"📄 Scanning page {page_count}/{scan_options['max_pages']}: {current_url}")

#                 page_start_time = time.time()
#                 page_data = None
#                 try:
#                     # Use the modified single-page scan function
#                     page_data = await self._scan_single_page(
#                         page, current_url, scan_options, consent_interactions
#                     )

#                     page_duration = time.time() - page_start_time

#                     # Get cookies specific to this page's context/origin if possible
#                     # Playwright's context.cookies() gets ALL cookies. We filter later.
#                     # For now, just store the raw data associated with this page scan.
#                     page_cookies_raw = await context.cookies([current_url])


#                     page_result = {
#                         "url": current_url,
#                         "status": "COMPLETED",
#                         "duration_seconds": round(page_duration, 2),
#                         "cookies": page_cookies_raw, # Store raw cookies found during this page visit
#                         "local_storage": page_data.get('local_storage', {}),
#                         "session_storage": page_data.get('session_storage', {}),
#                         "error": None
#                     }
#                     all_page_results.append(page_result)

#                     # --- Link Discovery ---
#                     found_links = page_data.get('links', [])
#                     added_to_queue = 0
#                     for link in found_links:
#                         if crawl_queue.qsize() + page_count + added_to_queue >= scan_options['max_pages']:
#                             break # Don't add more links than max_pages

#                         try:
#                             # Resolve relative links and handle potential errors
#                             abs_link = urljoin(current_url, link)
#                             parsed_link = urlparse(abs_link)

#                             # Basic validity check and remove fragment
#                             if parsed_link.scheme in ['http', 'https'] and parsed_link.netloc:
#                                 clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
#                                 # Remove trailing slash for consistency
#                                 if clean_link.endswith('/') and len(clean_link) > 1:
#                                      clean_link = clean_link[:-1]

#                                 # Check if it's an internal link and not yet visited/queued
#                                 if self._get_base_domain(clean_link) == base_domain and clean_link not in visited_urls:
#                                     # Ignore common non-HTML file extensions
#                                     ignored_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', '.xml', '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.avi']
#                                     if not any(parsed_link.path.lower().endswith(ext) for ext in ignored_extensions):
#                                         visited_urls.add(clean_link)
#                                         await crawl_queue.put(clean_link)
#                                         added_to_queue += 1

#                         except Exception as link_e:
#                             logger.debug(f"Link processing error for '{link}' on {current_url}: {link_e}")

#                 except Exception as page_scan_e:
#                     error_count += 1
#                     logger.warning(f"⚠ Failed to scan page {current_url}: {page_scan_e}", exc_info=True) # Log traceback
#                     page_duration = time.time() - page_start_time
#                     all_page_results.append({
#                         "url": current_url,
#                         "status": "FAILED",
#                         "duration_seconds": round(page_duration, 2),
#                         "cookies": [], "local_storage": {}, "session_storage": {},
#                         "error": str(page_scan_e)
#                     })
#                     # Optional: Add a delay or retry mechanism here if needed

#                 # Optional: Small delay between page scans to avoid overwhelming the server
#                 await asyncio.sleep(1)

#             crawl_duration = time.time() - crawl_start_time

#             # Get ALL cookies from the entire context at the end
#             # These represent the cumulative cookies set during the whole crawl
#             final_all_context_cookies = await context.cookies()

#             # Standardize the final list of cookies
#             standardized_final_cookies = self._standardize_cookies(final_all_context_cookies, start_url)
#             deduplicated_final_cookies = self._deduplicate_cookies(standardized_final_cookies)


#             logger.info(f"✅ Crawl completed: Scanned {page_count} pages ({error_count} errors) in {crawl_duration:.2f}s. Found {len(deduplicated_final_cookies)} unique cookies.")

#             return {
#                 "scan_metadata": {
#                     "start_url": start_url,
#                     "base_domain": base_domain,
#                     "total_duration_seconds": round(crawl_duration, 2),
#                     "pages_scanned_count": page_count,
#                     "scan_errors": error_count,
#                     "user_agent": self.FIXED_USER_AGENT,
#                     "scan_timestamp": time.time()
#                 },
#                 "page_results": all_page_results, # Contains raw cookies/storage per page
#                  # Contains standardized, deduplicated cookies from the whole session
#                 "final_unique_cookies": deduplicated_final_cookies,
#                 "consent_interactions_count": len(consent_interactions),
#                 "network_cookies_count": len(network_cookies) # Count for info
#             }

#         finally:
#             # Ensure context is closed even if errors occur
#              if context:
#                  try:
#                      await context.close()
#                      if context in self.contexts:
#                           self.contexts.remove(context)
#                  except Exception as e:
#                       logger.warning(f"⚠ Error closing context during cleanup: {e}")


#     async def _setup_network_monitoring(self, page: Page, network_cookies: List):
#         """Set up network request monitoring for Set-Cookie headers."""

#         async def handle_response(response):
#             try:
#                 # Check for Set-Cookie header
#                 set_cookie_headers = await response.header_values('set-cookie')
#                 if set_cookie_headers:
#                     for header in set_cookie_headers:
#                          network_cookies.append({
#                              'url': response.url,
#                              'set_cookie_header': header,
#                              'status': response.status,
#                              'timestamp': time.time()
#                          })
#             except Exception as e:
#                 # Can be noisy, log as debug
#                 logger.debug(f"Network monitoring error processing response for {response.url}: {e}")

#         page.on('response', handle_response)


#     async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
#         """
#         Scans a single page, handles consent, scrolls,
#         and returns cookies, storage, AND links found on the page.
#         """
#         logger.debug(f"Navigating to: {url}")
#         # Increased timeout for navigation and use 'load' state which waits for more resources
#         await page.goto(url, wait_until='load', timeout=60000)

#         # Wait for initial dynamic content/network activity to potentially settle
#         await self._wait_for_dynamic_content(page)

#         # Handle consent banner before scrolling, as scroll might hide it
#         if options.get('accept_consent', False):
#             await self._advanced_consent_handling(
#                 page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
#             )
#             # Wait a bit after consent interaction for cookies to potentially be set
#             await asyncio.sleep(2)

#         # Enhanced scrolling
#         if options.get('deep_scroll', True):
#             await self._enhanced_auto_scroll(page)
#             # Wait after scrolling for lazy-loaded content to potentially set cookies
#             await self._wait_for_dynamic_content(page) # Check network again after scroll

#         # Final wait period for everything to settle before collecting data
#         logger.debug(f"Waiting {options['wait_seconds']}s for cookies on {url}")
#         await asyncio.sleep(options['wait_seconds'])

#         # --- Data Collection ---
#         js_cookies_str = ""
#         local_storage_data = {}
#         session_storage_data = {}
#         page_links = []

#         try:
#             js_cookies_str = await page.evaluate("() => document.cookie")
#         except Exception as e:
#             logger.warning(f"Could not get JS cookies from {url}: {e}")

#         try:
#             local_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))")
#         except Exception as e:
#             logger.warning(f"Could not get Local Storage from {url}: {e}")

#         try:
#             session_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))")
#         except Exception as e:
#             logger.warning(f"Could not get Session Storage from {url}: {e}")

#         try:
#             # Get href attribute directly for robustness
#             page_links = await page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
#             # Filter out null/empty hrefs that might come from the evaluate call
#             page_links = [link for link in page_links if link]
#         except Exception as e:
#             logger.warning(f"Could not extract links from {url}: {e}")

#         return {
#             'js_cookies': js_cookies_str,
#             'local_storage': local_storage_data,
#             'session_storage': session_storage_data,
#             'links': page_links # Return discovered links (href attributes)
#         }

#     async def _wait_for_dynamic_content(self, page: Page):
#         """Wait for dynamic content to load (XHR, scripts, etc.)"""
#         try:
#             # Wait for network to be mostly idle (adjust connections count if needed)
#             logger.debug(f"Waiting for network idle on {page.url}...")
#             await page.wait_for_load_state('networkidle', timeout=15000)
#             logger.debug(f"Network idle detected on {page.url}.")
#             # Short additional wait
#             await page.wait_for_timeout(1000)
#         except Exception as e:
#             # Timeouts are expected if page is constantly active, log as debug
#             logger.debug(f"Wait for dynamic content/networkidle finished or timed out for {page.url}: {e}")


#     async def _enhanced_auto_scroll(self, page: Page):
#         """Enhanced auto-scrolling to trigger lazy-loaded content"""
#         logger.debug(f"Performing enhanced scroll on {page.url}")
#         try:
#             await page.evaluate("""
#             async () => {
#                 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
#                 let totalHeight = 0;
#                 const distance = 100; // Scroll distance per step
#                 const maxScrolls = 100; // Limit scrolls to prevent infinite loops
#                 let scrolls = 0;

#                 while (scrolls < maxScrolls) {
#                     const scrollHeight = document.body.scrollHeight;
#                     window.scrollBy(0, distance);
#                     await sleep(100); // Wait for potential content loading
#                     totalHeight += distance;
#                     scrolls++;

#                     // Break if we've reached the bottom (or didn't scroll further)
#                     if (window.innerHeight + window.scrollY >= scrollHeight || scrollHeight === document.body.scrollHeight) {
#                        // Optional: one final scroll to be sure
#                        window.scrollTo(0, document.body.scrollHeight);
#                        await sleep(200);
#                        break;
#                     }
#                 }
#                 // Scroll back to top
#                 window.scrollTo(0, 0);
#                 await sleep(200);
#             }
#             """)
#             logger.debug(f"Finished enhanced scroll on {page.url}")
#         except Exception as e:
#              logger.warning(f"Error during enhanced scroll on {page.url}: {e}")


#     async def _advanced_consent_handling(self, page: Page, timeout_sec: int, retries: int, consent_interactions: List) -> bool:
#         """
#         Attempts to find and click common "Accept All"-style consent buttons.
#         """
#         logger.info(f"🎯 Attempting advanced consent banner interaction on {page.url}")
#         timeout_ms = timeout_sec * 1000 # Playwright uses milliseconds

#         # Prioritized list of selectors - more specific or common ones first
#         consent_selectors = [
#             # Common CMP IDs/Classes (High confidence)
#             '#onetrust-accept-btn-handler',
#             '[id*="consent"] button[id*="accept"]',
#              'button[id*="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
#             'button[class*="accept-all"]', 'button[class*="optanon-allow-all"]',
#             'button[id*="accept-all"]', 'button[data-accept-action]',
#             'button[data-testid*="accept"]', 'button[data-cy*="accept"]',
#             'button[data-gdpr-single-choice-accept]',

#             # Common Text Patterns (Medium confidence)
#             'button:text-matches("Accept all", "i")',
#             'button:text-matches("Allow all", "i")',
#             'button:text-matches("Agree", "i")',
#             'button:text-matches("Accept", "i")', # More generic, lower priority
#             'button:text-matches("OK", "i")',
#             'button:text-matches("Got it", "i")',

#             # Attributes containing keywords
#             'button[id*="cookie"]', 'button[class*="cookie"]',
#             'button[id*="consent"]', 'button[class*="consent"]',

#             # Role-based + Text
#             '[role="dialog"] button:text-matches("Accept", "i")',
#             '[role="banner"] button:text-matches("Accept", "i")',

#             # More Language Variations (add as needed)
#             'button:text-matches("Accepter", "i")', # French
#             'button:text-matches("Aceptar", "i")',  # Spanish
#             'button:text-matches("Akzeptieren", "i")', # German
#         ]

#         # Simplified iframe checking - look for common names/ids
#         iframe_selectors = [
#              'iframe[id*="consent"]', 'iframe[name*="consent"]',
#              'iframe[id*="cookie"]', 'iframe[name*="cookie"]',
#              'iframe[title*="consent" i]', 'iframe[title*="cookie" i]'
#         ]

#         success = False

#         for attempt in range(retries):
#             logger.debug(f"Consent detection attempt {attempt + 1}/{retries} on {page.url}")
#             clicked_in_attempt = False

#             # 1. Check Main Page Frame
#             for selector in consent_selectors:
#                 try:
#                     element = page.locator(selector).first # Target only the first match
#                     # Check visibility with a shorter timeout within the loop
#                     if await element.is_visible(timeout=1000):
#                         logger.info(f"✅ Found potential consent button: {selector}")
#                         await element.click(timeout=3000) # Short click timeout
#                         logger.info(f"✅ Clicked consent button: {selector}")
#                         consent_interactions.append({
#                             'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(), 'type': 'main_page'
#                         })
#                         clicked_in_attempt = True
#                         await page.wait_for_timeout(1500) # Wait briefly for banner to disappear/cookies to set
#                         break # Assume first found accept button is enough
#                 except Exception as e:
#                     logger.debug(f"Selector '{selector}' not found/visible or click failed: {e}")
#                     continue # Try next selector
#             if clicked_in_attempt:
#                 success = True
#                 break # Exit retry loop if clicked on main page

#             # 2. Check Iframes (only if not found on main page in this attempt)
#             logger.debug("Checking iframes for consent buttons...")
#             for frame_selector in iframe_selectors:
#                  try:
#                       frame_locator = page.locator(frame_selector).first
#                       if await frame_locator.is_visible(timeout=500): # Quick check if iframe exists
#                             frame = await frame_locator.content_frame()
#                             if frame:
#                                 logger.debug(f"Searching within iframe: {frame_selector}")
#                                 for selector in consent_selectors[:15]: # Try top selectors in iframe
#                                      try:
#                                           element = frame.locator(selector).first
#                                           if await element.is_visible(timeout=1000):
#                                                 logger.info(f"✅ Found consent button in iframe '{frame_selector}': {selector}")
#                                                 await element.click(timeout=3000)
#                                                 logger.info(f"✅ Clicked consent button in iframe: {selector}")
#                                                 consent_interactions.append({
#                                                     'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(),
#                                                     'type': 'iframe', 'iframe_selector': frame_selector
#                                                 })
#                                                 clicked_in_attempt = True
#                                                 await page.wait_for_timeout(1500)
#                                                 break # Found and clicked in iframe
#                                      except Exception as e_iframe:
#                                           logger.debug(f"Selector '{selector}' in iframe '{frame_selector}' failed: {e_iframe}")
#                                           continue
#                             if clicked_in_attempt: break # Stop checking other iframes
#                  except Exception as e_frame_check:
#                       logger.debug(f"Iframe check failed for '{frame_selector}': {e_frame_check}")
#                       continue
#                  if clicked_in_attempt: break # Stop checking other iframe types

#             if clicked_in_attempt:
#                 success = True
#                 break # Exit retry loop if clicked in iframe

#             # Wait before next retry if nothing was clicked in this attempt
#             if not clicked_in_attempt and attempt < retries - 1:
#                 logger.debug(f"Consent button not found in attempt {attempt + 1}, retrying...")
#                 await asyncio.sleep(1) # Short delay before retry

#         if success:
#             logger.info(f"🎉 Successfully interacted with a consent banner on {page.url}")
#         else:
#             logger.info(f"ℹ No interactable consent banner found after {retries} attempts on {page.url}")

#         return success

#     def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
#         """Remove duplicate cookies based on name, domain, and path."""
#         seen: Set[str] = set()
#         deduplicated = []
#         for cookie in cookies:
#             # Create a more robust unique identifier
#             identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
#             if identifier not in seen:
#                 seen.add(identifier)
#                 deduplicated.append(cookie)

#         logger.debug(f"🔄 Deduplicated {len(cookies)} -> {len(deduplicated)} cookies based on name/domain/path")
#         return deduplicated

#     def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
#         """Standardize cookie data format for consistency and add metadata."""
#         standardized = []
#         try:
#             url_parts = urlparse(base_url)
#             site_base_domain = self._get_base_domain(url_parts.netloc)
#             if not site_base_domain: site_base_domain = url_parts.netloc # Fallback
#         except Exception:
#              logger.warning(f"Could not parse base_url {base_url} for standardization, using fallback.")
#              site_base_domain = base_url # Raw fallback

#         for cookie in cookies:
#             try:
#                 # Normalize domain (remove leading dot)
#                 cookie_domain = cookie.get('domain', '').lstrip('.')
#                 # If domain is missing, assume it's for the base domain of the site
#                 if not cookie_domain:
#                     cookie_domain = site_base_domain

#                 cookie_base_domain = self._get_base_domain(cookie_domain)

#                 # Determine SameSite (handle None or missing)
#                 samesite = cookie.get('sameSite')
#                 if samesite not in ['Strict', 'Lax', 'None']:
#                      samesite = 'Lax' # Default according to modern browser standards if invalid/missing

#                 standardized_cookie = {
#                     'name': cookie.get('name', ''),
#                     'value': cookie.get('value', ''),
#                     'domain': cookie_domain, # The full domain from the cookie
#                     'path': cookie.get('path', '/'),
#                     'expires': cookie.get('expires', -1), # -1 indicates session cookie in Playwright
#                     'httpOnly': cookie.get('httpOnly', False),
#                     'secure': cookie.get('secure', False),
#                     'sameSite': samesite,
#                     # --- Added Metadata ---
#                     'is_third_party': cookie_base_domain != site_base_domain if site_base_domain and cookie_base_domain else False,
#                     'base_domain': cookie_base_domain or cookie_domain, # Calculated base domain
#                     'size_bytes': len(cookie.get('name', '').encode('utf-8') + b'=' + cookie.get('value', '').encode('utf-8')),
#                     'timestamp': time.time() # Timestamp when processed by scanner
#                 }
#                 standardized.append(standardized_cookie)

#             except Exception as e:
#                 logger.warning(f"Cookie standardization error for cookie '{cookie.get('name')}': {e}")
#                 continue

#         return standardized

#     def _get_base_domain(self, url_or_domain: str) -> str:
#         """
#         Accurately extract the registrable domain (e.g., example.com, example.co.uk)
#         using tldextract. Returns None if extraction fails badly.
#         """
#         if not url_or_domain or not isinstance(url_or_domain, str):
#              return ""
#         try:

#             extracted = tldextract.extract(url_or_domain, include_psl_private_domains=True) # <--- FIX HERE
#             if extracted.registered_domain:
#                 return extracted.registered_domain
#             elif extracted.domain:
#                  return extracted.domain
#             else:
#                  # If it looks like an IP address, return it as is? Or empty? Decide policy.
#                  # Let's return empty if it's likely just a TLD or invalid.
#                  return ""
#         except Exception as e:
#             logger.error(f"Error extracting base domain from '{url_or_domain}': {e}")
#             # Try a simple split as a last resort, might be wrong for .co.uk etc.
#             parts = url_or_domain.split('.')
#             if len(parts) >= 2:
#                  return ".".join(parts[-2:])
#             return url_or_domain # Return original if splitting fails


import asyncio
import time
import logging
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import json
import hashlib
import tldextract
import sys # For platform check

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handle potential asyncio policy issues on Windows for local dev
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

class PlaywrightScanner:
    """
    World-class cookie scanner designed to compete with CookieYes and Termly,
    now featuring full-site crawling capabilities.
    """

    # Fixed configuration for consistency across Docker/Linux environments
    FIXED_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    VIEWPORT = {'width': 1920, 'height': 1080}
    TIMEZONE = 'IST' # Assuming India Standard Time based on user context


    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright: Optional[async_playwright] = None
        self.contexts: List[BrowserContext] = []

    async def initialize(self, headless: bool = True):
        """Initialize browser with locked configuration for consistency"""
        logger.info("🔧 Initializing world-class cookie scanner...")

        self.playwright = await async_playwright().start()

        # Launch with locked configuration for Docker consistency
        try:
            self.browser = await self.playwright.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security', # Be cautious with this in production if not needed
                    '--disable-features=VizDisplayCompositor', # May help in headless stability
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--lang=en-US' # Set language consistently
                ]
            )
            logger.info("✅ Browser initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to launch browser: {e}")
            await self.close() # Clean up playwright if launch fails
            raise # Re-raise the exception

    async def close(self):
        """Gracefully close all contexts and browser"""
        logger.info("🔚 Closing scanner...")

        # Close all contexts
        for context in self.contexts[:]: # Iterate over a copy
            try:
                await context.close()
                self.contexts.remove(context)
            except Exception as e:
                logger.warning(f"⚠ Error closing context: {e}")
                # Attempt to remove context even if close failed
                if context in self.contexts:
                    self.contexts.remove(context)

        if self.browser:
            try:
                await self.browser.close()
                self.browser = None
            except Exception as e:
                logger.error(f"❌ Error closing browser: {e}")

        if self.playwright:
            try:
                await self.playwright.stop()
                self.playwright = None
            except Exception as e:
                logger.error(f"❌ Error stopping Playwright: {e}")

        logger.info("✅ Scanner closed successfully")

    async def create_consistent_context(self) -> BrowserContext:
        """Create browser context with locked settings for consistency"""
        if not self.browser:
             logger.error("❌ Cannot create context, browser is not initialized.")
             raise RuntimeError("Browser not initialized. Call initialize() first.")

        context = await self.browser.new_context(
            user_agent=self.FIXED_USER_AGENT,
            viewport=self.VIEWPORT,
            timezone_id=self.TIMEZONE,
            permissions=['geolocation', 'notifications'], # Adjust permissions as needed
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8',
                'DNT': '1' # Do Not Track header
            },
            ignore_https_errors=True # Use with caution
        )

        self.contexts.append(context)
        return context

    async def run_crawl_and_scan(self, start_url: str, options: Dict = None) -> Dict:
        """
        Orchestrates a full-site crawl. Manages a queue and scans
        pages one by one, collecting cookies and links.
        ✅ OPTIMIZED: Concurrent scanning + reduced waits + per-page metadata
        """
        if not options:
            options = {}

        # ✅ OPTIMIZED: Changed defaults for speed
        scan_options = {
            'wait_seconds': options.get('wait_seconds', 3),  # ✅ CHANGED: 10 → 3 seconds
            'max_pages': options.get('max_pages', 20),       # ✅ CHANGED: 5 → 20 pages
            'deep_scroll': options.get('deep_scroll', False), # ✅ CHANGED: True → False (saves 3s per page)
            'banner_timeout': options.get('banner_timeout', 10),
            'retry_banner_clicks': options.get('retry_banner_clicks', 3),
            'accept_consent': options.get('accept_consent', False),
            'concurrent_pages': options.get('concurrent_pages', 4)  # ✅ NEW: Concurrent scanning
        }

        logger.info(f"🚀 Starting world-class CRAWL of: {start_url} with options: {scan_options}")
        crawl_start_time = time.time()

        try:
            base_domain = self._get_base_domain(start_url)
            if not base_domain:
                raise ValueError(f"Could not extract base domain from start URL: {start_url}")
        except Exception as e:
             logger.error(f"❌ Error extracting base domain from {start_url}: {e}")
             raise ValueError(f"Invalid start URL: {start_url}") from e

        crawl_queue = asyncio.Queue()
        await crawl_queue.put(start_url)

        visited_urls: Set[str] = {start_url}
        all_page_results = []
        page_scan_metadata: List[Dict] = []  # ✅ NEW: Track per-page timing

        network_cookies: List[Dict] = []
        consent_interactions: List[Dict] = []

        page_count = 0
        error_count = 0

        try:
            # ✅ OPTIMIZED: Batch processing instead of sequential
            while page_count < scan_options['max_pages'] and not crawl_queue.empty():
                # Get batch of URLs for concurrent processing
                batch_urls = []
                while len(batch_urls) < scan_options['concurrent_pages'] and not crawl_queue.empty():
                    try:
                        current_url = await asyncio.wait_for(crawl_queue.get(), timeout=1.0)
                        batch_urls.append(current_url)
                    except asyncio.TimeoutError:
                        break

                if not batch_urls:
                    break

                # ✅ NEW: Process batch concurrently
                logger.info(f"📊 Processing {len(batch_urls)} pages concurrently...")
                batch_start = time.time()

                tasks = []
                for batch_url in batch_urls:
                    task = self._scan_page_concurrent(batch_url, scan_options, network_cookies, consent_interactions)
                    tasks.append(task)

                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                for idx, result in enumerate(batch_results):
                    if isinstance(result, Exception):
                        error_count += 1
                        logger.warning(f"⚠ Failed to scan {batch_urls[idx]}: {result}")
                        page_scan_metadata.append({
                            'url': batch_urls[idx],
                            'scan_duration_seconds': round(time.time() - batch_start, 2),
                            'page_status': 'failed',
                            'error': str(result)
                        })
                    elif result:
                        page_result = result['page_result']
                        all_page_results.append(page_result)
                        page_scan_metadata.append(result['metadata'])

                        # --- Link Discovery ---
                        found_links = result['links']
                        for link in found_links:
                            if page_count + len(batch_urls) >= scan_options['max_pages']:
                                break

                            try:
                                abs_link = urljoin(batch_urls[idx], link)
                                parsed_link = urlparse(abs_link)

                                if parsed_link.scheme in ['http', 'https'] and parsed_link.netloc:
                                    clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
                                    if clean_link.endswith('/') and len(clean_link) > 1:
                                         clean_link = clean_link[:-1]

                                    if self._get_base_domain(clean_link) == base_domain and clean_link not in visited_urls:
                                        ignored_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', '.xml', '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.avi']
                                        if not any(parsed_link.path.lower().endswith(ext) for ext in ignored_extensions):
                                            visited_urls.add(clean_link)
                                            await crawl_queue.put(clean_link)

                            except Exception as link_e:
                                logger.debug(f"Link processing error: {link_e}")

                page_count += len(batch_urls)
                batch_duration = time.time() - batch_start
                logger.info(f"✅ Batch completed in {batch_duration:.1f}s")

            crawl_duration = time.time() - crawl_start_time

            # Get ALL cookies from all pages
            final_all_context_cookies = []
            for result in all_page_results:
                final_all_context_cookies.extend(result.get('cookies', []))

            # Standardize the final list of cookies
            standardized_final_cookies = self._standardize_cookies(final_all_context_cookies, start_url)
            deduplicated_final_cookies = self._deduplicate_cookies(standardized_final_cookies)

            logger.info(f"✅ Crawl completed: Scanned {page_count} pages ({error_count} errors) in {crawl_duration:.2f}s. Found {len(deduplicated_final_cookies)} unique cookies.")

            return {
                "scan_metadata": {
                    "start_url": start_url,
                    "base_domain": base_domain,
                    "total_duration_seconds": round(crawl_duration, 2),
                    "pages_scanned_count": page_count,
                    "scan_errors": error_count,
                    "user_agent": self.FIXED_USER_AGENT,
                    "scan_timestamp": time.time(),
                    "avg_time_per_page": round(crawl_duration / max(page_count, 1), 2)  # ✅ NEW
                },
                "page_results": all_page_results,
                "pages_scan_metadata": page_scan_metadata,  # ✅ NEW: Per-page timing
                "final_unique_cookies": deduplicated_final_cookies,
                "consent_interactions_count": len(consent_interactions),
                "network_cookies_count": len(network_cookies)
            }

        finally:
            # Ensure context is closed even if errors occur
            pass

    async def _scan_page_concurrent(self, url: str, options: Dict, network_cookies: List, consent_interactions: List) -> Dict:
        """✅ NEW: Scan page with its own context for concurrent processing"""
        context = None
        page = None
        page_start = time.time()

        try:
            context = await self.create_consistent_context()
            page = await context.new_page()

            await self._setup_network_monitoring(page, network_cookies)

            page_data = await self._scan_single_page(page, url, options, consent_interactions)
            page_end = time.time()

            page_cookies_raw = await context.cookies([url])

            page_result = {
                "url": url,
                "status": "COMPLETED",
                "duration_seconds": round(page_end - page_start, 2),
                "cookies": page_cookies_raw,
                "local_storage": page_data.get('local_storage', {}),
                "session_storage": page_data.get('session_storage', {}),
                "error": None
            }

            return {
                'page_result': page_result,
                'links': page_data.get('links', []),
                'metadata': {
                    'url': url,
                    'scan_duration_seconds': round(page_end - page_start, 2),
                    'page_status': 'success',
                    'cookies_found': len(page_cookies_raw)
                }
            }

        except Exception as e:
            logger.warning(f"⚠ Failed to scan {url}: {e}")
            return None

        finally:
            if context:
                try:
                    await context.close()
                    if context in self.contexts:
                        self.contexts.remove(context)
                except Exception as e:
                    logger.warning(f"Error closing context: {e}")

    async def _setup_network_monitoring(self, page: Page, network_cookies: List):
        """Set up network request monitoring for Set-Cookie headers."""

        async def handle_response(response):
            try:
                # Check for Set-Cookie header
                set_cookie_headers = await response.header_values('set-cookie')
                if set_cookie_headers:
                    for header in set_cookie_headers:
                         network_cookies.append({
                             'url': response.url,
                             'set_cookie_header': header,
                             'status': response.status,
                             'timestamp': time.time()
                         })
            except Exception as e:
                # Can be noisy, log as debug
                logger.debug(f"Network monitoring error processing response for {response.url}: {e}")

        page.on('response', handle_response)


    async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
        """
        Scans a single page, handles consent, scrolls,
        and returns cookies, storage, AND links found on the page.
        ✅ OPTIMIZED: Reduced waits, disabled scroll by default
        """
        logger.debug(f"Navigating to: {url}")
        await page.goto(url, wait_until='load', timeout=60000)

        await self._wait_for_dynamic_content(page)

        if options.get('accept_consent', False):
            await self._advanced_consent_handling(
                page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
            )
            await asyncio.sleep(2)

        # ✅ OPTIMIZED: Scroll disabled by default (saves 3s per page)
        if options.get('deep_scroll', False):
            await self._enhanced_auto_scroll(page)
            await self._wait_for_dynamic_content(page)

        # ✅ OPTIMIZED: Reduced wait from 10s to 3s
        logger.debug(f"Waiting {options['wait_seconds']}s for cookies on {url}")
        await asyncio.sleep(options['wait_seconds'])

        # --- Data Collection ---
        js_cookies_str = ""
        local_storage_data = {}
        session_storage_data = {}
        page_links = []

        try:
            js_cookies_str = await page.evaluate("() => document.cookie")
        except Exception as e:
            logger.warning(f"Could not get JS cookies from {url}: {e}")

        try:
            local_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.localStorage))")
        except Exception as e:
            logger.warning(f"Could not get Local Storage from {url}: {e}")

        try:
            session_storage_data = await page.evaluate("() => JSON.parse(JSON.stringify(window.sessionStorage))")
        except Exception as e:
            logger.warning(f"Could not get Session Storage from {url}: {e}")

        try:
            # Get href attribute directly for robustness
            page_links = await page.evaluate("() => Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))")
            # Filter out null/empty hrefs that might come from the evaluate call
            page_links = [link for link in page_links if link]
        except Exception as e:
            logger.warning(f"Could not extract links from {url}: {e}")

        return {
            'js_cookies': js_cookies_str,
            'local_storage': local_storage_data,
            'session_storage': session_storage_data,
            'links': page_links
        }

    async def _wait_for_dynamic_content(self, page: Page):
        """Wait for dynamic content to load (XHR, scripts, etc.)"""
        try:
            logger.debug(f"Waiting for network idle on {page.url}...")
            await page.wait_for_load_state('networkidle', timeout=15000)
            logger.debug(f"Network idle detected on {page.url}.")
            await page.wait_for_timeout(1000)
        except Exception as e:
            logger.debug(f"Wait for dynamic content/networkidle finished or timed out: {e}")


    async def _enhanced_auto_scroll(self, page: Page):
        """Enhanced auto-scrolling to trigger lazy-loaded content"""
        logger.debug(f"Performing enhanced scroll on {page.url}")
        try:
            await page.evaluate("""
            async () => {
                const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
                let totalHeight = 0;
                const distance = 100;
                const maxScrolls = 100;
                let scrolls = 0;

                while (scrolls < maxScrolls) {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    await sleep(100);
                    totalHeight += distance;
                    scrolls++;

                    if (window.innerHeight + window.scrollY >= scrollHeight || scrollHeight === document.body.scrollHeight) {
                       window.scrollTo(0, document.body.scrollHeight);
                       await sleep(200);
                       break;
                    }
                }
                window.scrollTo(0, 0);
                await sleep(200);
            }
            """)
            logger.debug(f"Finished enhanced scroll on {page.url}")
        except Exception as e:
             logger.warning(f"Error during enhanced scroll on {page.url}: {e}")


    async def _advanced_consent_handling(self, page: Page, timeout_sec: int, retries: int, consent_interactions: List) -> bool:
        """
        Attempts to find and click common "Accept All"-style consent buttons.
        """
        logger.info(f"🎯 Attempting advanced consent banner interaction on {page.url}")
        timeout_ms = timeout_sec * 1000

        consent_selectors = [
            '#onetrust-accept-btn-handler',
            '[id*="consent"] button[id*="accept"]',
             'button[id*="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
            'button[class*="accept-all"]', 'button[class*="optanon-allow-all"]',
            'button[id*="accept-all"]', 'button[data-accept-action]',
            'button[data-testid*="accept"]', 'button[data-cy*="accept"]',
            'button[data-gdpr-single-choice-accept]',
            'button:text-matches("Accept all", "i")',
            'button:text-matches("Allow all", "i")',
            'button:text-matches("Agree", "i")',
            'button:text-matches("Accept", "i")',
            'button:text-matches("OK", "i")',
            'button:text-matches("Got it", "i")',
            'button[id*="cookie"]', 'button[class*="cookie"]',
            'button[id*="consent"]', 'button[class*="consent"]',
            '[role="dialog"] button:text-matches("Accept", "i")',
            '[role="banner"] button:text-matches("Accept", "i")',
            'button:text-matches("Accepter", "i")',
            'button:text-matches("Aceptar", "i")',
            'button:text-matches("Akzeptieren", "i")',
        ]

        iframe_selectors = [
             'iframe[id*="consent"]', 'iframe[name*="consent"]',
             'iframe[id*="cookie"]', 'iframe[name*="cookie"]',
             'iframe[title*="consent" i]', 'iframe[title*="cookie" i]'
        ]

        success = False

        for attempt in range(retries):
            logger.debug(f"Consent detection attempt {attempt + 1}/{retries} on {page.url}")
            clicked_in_attempt = False

            for selector in consent_selectors:
                try:
                    element = page.locator(selector).first
                    if await element.is_visible(timeout=1000):
                        logger.info(f"✅ Found potential consent button: {selector}")
                        await element.click(timeout=3000)
                        logger.info(f"✅ Clicked consent button: {selector}")
                        consent_interactions.append({
                            'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(), 'type': 'main_page'
                        })
                        clicked_in_attempt = True
                        await page.wait_for_timeout(1500)
                        break
                except Exception as e:
                    logger.debug(f"Selector '{selector}' not found/visible: {e}")
                    continue

            if clicked_in_attempt:
                success = True
                break

            logger.debug("Checking iframes for consent buttons...")
            for frame_selector in iframe_selectors:
                 try:
                      frame_locator = page.locator(frame_selector).first
                      if await frame_locator.is_visible(timeout=500):
                            frame = await frame_locator.content_frame()
                            if frame:
                                logger.debug(f"Searching within iframe: {frame_selector}")
                                for selector in consent_selectors[:15]:
                                     try:
                                          element = frame.locator(selector).first
                                          if await element.is_visible(timeout=1000):
                                                logger.info(f"✅ Found consent button in iframe: {selector}")
                                                await element.click(timeout=3000)
                                                logger.info(f"✅ Clicked consent button in iframe: {selector}")
                                                consent_interactions.append({
                                                    'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(),
                                                    'type': 'iframe', 'iframe_selector': frame_selector
                                                })
                                                clicked_in_attempt = True
                                                await page.wait_for_timeout(1500)
                                                break
                                     except Exception as e_iframe:
                                          logger.debug(f"Selector in iframe failed: {e_iframe}")
                                          continue
                            if clicked_in_attempt: break
                 except Exception as e_frame_check:
                      logger.debug(f"Iframe check failed: {e_frame_check}")
                      continue
                 if clicked_in_attempt: break

            if clicked_in_attempt:
                success = True
                break

            if not clicked_in_attempt and attempt < retries - 1:
                logger.debug(f"Consent button not found in attempt {attempt + 1}, retrying...")
                await asyncio.sleep(1)

        if success:
            logger.info(f"🎉 Successfully interacted with consent banner on {page.url}")
        else:
            logger.info(f"ℹ No interactable consent banner found after {retries} attempts on {page.url}")

        return success

    # def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
    #     """Remove duplicate cookies based on name, domain, and path."""
    #     seen: Set[str] = set()
    #     deduplicated = []
    #     for cookie in cookies:
    #         identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
    #         if identifier not in seen:
    #             seen.add(identifier)
    #             deduplicated.append(cookie)

    #     logger.debug(f"🔄 Deduplicated {len(cookies)} -> {len(deduplicated)} cookies")
    #     return deduplicated

    def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
        """Remove ONLY exact duplicates (same name, domain, path)"""
        seen: Set[str] = set()
        deduplicated = []

        for cookie in cookies:
            # Exact match only - don't generalize
            identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"

            if identifier not in seen:
                seen.add(identifier)
                deduplicated.append(cookie)

        logger.debug(f"Deduplicated {len(cookies)} → {len(deduplicated)} cookies")
        return deduplicated

    def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
        """Standardize cookie data format for consistency and add metadata."""
        standardized = []
        try:
            url_parts = urlparse(base_url)
            site_base_domain = self._get_base_domain(url_parts.netloc)
            if not site_base_domain: site_base_domain = url_parts.netloc
        except Exception:
             logger.warning(f"Could not parse base_url {base_url}")
             site_base_domain = base_url

        for cookie in cookies:
            try:
                cookie_domain = cookie.get('domain', '').lstrip('.')
                if not cookie_domain:
                    cookie_domain = site_base_domain

                cookie_base_domain = self._get_base_domain(cookie_domain)

                samesite = cookie.get('sameSite')
                if samesite not in ['Strict', 'Lax', 'None']:
                     samesite = 'Lax'

                standardized_cookie = {
                    'name': cookie.get('name', ''),
                    'value': cookie.get('value', ''),
                    'domain': cookie_domain,
                    'path': cookie.get('path', '/'),
                    'expires': cookie.get('expires', -1),
                    'httpOnly': cookie.get('httpOnly', False),
                    'secure': cookie.get('secure', False),
                    'sameSite': samesite,
                    'is_third_party': cookie_base_domain != site_base_domain if site_base_domain and cookie_base_domain else False,
                    'base_domain': cookie_base_domain or cookie_domain,
                    'size_bytes': len(cookie.get('name', '').encode('utf-8') + b'=' + cookie.get('value', '').encode('utf-8')),
                    'timestamp': time.time()
                }
                standardized.append(standardized_cookie)

            except Exception as e:
                logger.warning(f"Cookie standardization error: {e}")
                continue

        return standardized

    def _get_base_domain(self, url_or_domain: str) -> str:
        """
        Accurately extract the registrable domain (e.g., example.com, example.co.uk)
        using tldextract. Returns None if extraction fails badly.
        """
        if not url_or_domain or not isinstance(url_or_domain, str):
             return ""
        try:
            extracted = tldextract.extract(url_or_domain, include_psl_private_domains=True)
            if extracted.registered_domain:
                return extracted.registered_domain
            elif extracted.domain:
                 return extracted.domain
            else:
                 return ""
        except Exception as e:
            logger.error(f"Error extracting base domain from '{url_or_domain}': {e}")
            parts = url_or_domain.split('.')
            if len(parts) >= 2:
                 return ".".join(parts[-2:])
            return url_or_domain
