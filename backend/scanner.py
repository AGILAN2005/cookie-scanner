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


#     def __init__(self):
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
#             raise 

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
#         ✅ OPTIMIZED: Concurrent scanning + reduced waits + per-page metadata
#         """
#         if not options:
#             options = {}

#         # ✅ OPTIMIZED: Changed defaults for speed
#         scan_options = {
#             'wait_seconds': options.get('wait_seconds', 3),  # ✅ CHANGED: 10 → 3 seconds
#             'max_pages': options.get('max_pages', 20),       # ✅ CHANGED: 5 → 20 pages
#             'deep_scroll': options.get('deep_scroll', False), # ✅ CHANGED: True → False (saves 3s per page)
#             'banner_timeout': options.get('banner_timeout', 10),
#             'retry_banner_clicks': options.get('retry_banner_clicks', 3),
#             'accept_consent': options.get('accept_consent', False),
#             'concurrent_pages': options.get('concurrent_pages', 4)  # ✅ NEW: Concurrent scanning
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

#         visited_urls: Set[str] = {start_url}
#         all_page_results = []
#         page_scan_metadata: List[Dict] = []  # ✅ NEW: Track per-page timing

#         network_cookies: List[Dict] = []
#         consent_interactions: List[Dict] = []

#         page_count = 0
#         error_count = 0

#         try:
#             # ✅ OPTIMIZED: Batch processing instead of sequential
#             while page_count < scan_options['max_pages'] and not crawl_queue.empty():
#                 # Get batch of URLs for concurrent processing
#                 batch_urls = []
#                 while len(batch_urls) < scan_options['concurrent_pages'] and not crawl_queue.empty():
#                     try:
#                         current_url = await asyncio.wait_for(crawl_queue.get(), timeout=1.0)
#                         batch_urls.append(current_url)
#                     except asyncio.TimeoutError:
#                         break

#                 if not batch_urls:
#                     break

#                 # ✅ NEW: Process batch concurrently
#                 logger.info(f"📊 Processing {len(batch_urls)} pages concurrently...")
#                 batch_start = time.time()

#                 tasks = []
#                 for batch_url in batch_urls:
#                     task = self._scan_page_concurrent(batch_url, scan_options, network_cookies, consent_interactions)
#                     tasks.append(task)

#                 batch_results = await asyncio.gather(*tasks, return_exceptions=True)

#                 for idx, result in enumerate(batch_results):
#                     if isinstance(result, Exception):
#                         error_count += 1
#                         logger.warning(f"⚠ Failed to scan {batch_urls[idx]}: {result}")
#                         page_scan_metadata.append({
#                             'url': batch_urls[idx],
#                             'scan_duration_seconds': round(time.time() - batch_start, 2),
#                             'page_status': 'failed',
#                             'error': str(result)
#                         })
#                     elif result:
#                         page_result = result['page_result']
#                         all_page_results.append(page_result)
#                         page_scan_metadata.append(result['metadata'])

#                         # --- Link Discovery ---
#                         found_links = result['links']
#                         for link in found_links:
#                             if page_count + len(batch_urls) >= scan_options['max_pages']:
#                                 break

#                             try:
#                                 abs_link = urljoin(batch_urls[idx], link)
#                                 parsed_link = urlparse(abs_link)

#                                 if parsed_link.scheme in ['http', 'https'] and parsed_link.netloc:
#                                     clean_link = f"{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}"
#                                     if clean_link.endswith('/') and len(clean_link) > 1:
#                                          clean_link = clean_link[:-1]

#                                     if self._get_base_domain(clean_link) == base_domain and clean_link not in visited_urls:
#                                         ignored_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.css', '.js', '.xml', '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.mp3', '.avi']
#                                         if not any(parsed_link.path.lower().endswith(ext) for ext in ignored_extensions):
#                                             visited_urls.add(clean_link)
#                                             await crawl_queue.put(clean_link)

#                             except Exception as link_e:
#                                 logger.debug(f"Link processing error: {link_e}")

#                 page_count += len(batch_urls)
#                 batch_duration = time.time() - batch_start
#                 logger.info(f"✅ Batch completed in {batch_duration:.1f}s")

#             crawl_duration = time.time() - crawl_start_time

#             # Get ALL cookies from all pages
#             final_all_context_cookies = []
#             for result in all_page_results:
#                 final_all_context_cookies.extend(result.get('cookies', []))

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
#                     "scan_timestamp": time.time(),
#                     "avg_time_per_page": round(crawl_duration / max(page_count, 1), 2)  # ✅ NEW
#                 },
#                 "page_results": all_page_results,
#                 "pages_scan_metadata": page_scan_metadata,  # ✅ NEW: Per-page timing
#                 "final_unique_cookies": deduplicated_final_cookies,
#                 "consent_interactions_count": len(consent_interactions),
#                 "network_cookies_count": len(network_cookies)
#             }

#         finally:
#             # Ensure context is closed even if errors occur
#             pass

#     async def _scan_page_concurrent(self, url: str, options: Dict, network_cookies: List, consent_interactions: List) -> Dict:
#         """✅ NEW: Scan page with its own context for concurrent processing"""
#         context = None
#         page = None
#         page_start = time.time()

#         try:
#             context = await self.create_consistent_context()
#             page = await context.new_page()

#             await self._setup_network_monitoring(page, network_cookies)

#             page_data = await self._scan_single_page(page, url, options, consent_interactions)
#             page_end = time.time()

#             page_cookies_raw = await context.cookies([url])

#             page_result = {
#                 "url": url,
#                 "status": "COMPLETED",
#                 "duration_seconds": round(page_end - page_start, 2),
#                 "cookies": page_cookies_raw,
#                 "local_storage": page_data.get('local_storage', {}),
#                 "session_storage": page_data.get('session_storage', {}),
#                 "error": None
#             }

#             return {
#                 'page_result': page_result,
#                 'links': page_data.get('links', []),
#                 'metadata': {
#                     'url': url,
#                     'scan_duration_seconds': round(page_end - page_start, 2),
#                     'page_status': 'success',
#                     'cookies_found': len(page_cookies_raw)
#                 }
#             }

#         except Exception as e:
#             logger.warning(f"⚠ Failed to scan {url}: {e}")
#             return None

#         finally:
#             if context:
#                 try:
#                     await context.close()
#                     if context in self.contexts:
#                         self.contexts.remove(context)
#                 except Exception as e:
#                     logger.warning(f"Error closing context: {e}")

#     # async def _setup_network_monitoring(self, page: Page, network_cookies: List):
#     #     """Set up network request monitoring for Set-Cookie headers."""

#     #     async def handle_response(response):
#     #         try:
#     #             # Check for Set-Cookie header
#     #             set_cookie_headers = await response.header_values('set-cookie')
#     #             if set_cookie_headers:
#     #                 for header in set_cookie_headers:
#     #                      network_cookies.append({
#     #                          'url': response.url,
#     #                          'set_cookie_header': header,
#     #                          'status': response.status,
#     #                          'timestamp': time.time()
#     #                      })
#     #         except Exception as e:
#     #             # Can be noisy, log as debug
#     #             logger.debug(f"Network monitoring error processing response for {response.url}: {e}")

#     #     page.on('response', handle_response)
    
#     async def _setup_network_monitoring(self, page: Page, network_cookies: List):
#         """Set up network request monitoring for Set-Cookie headers and JS cookie changes."""
#         async def handle_response(response):
#             try:
#                 set_cookie_headers = await response.header_values('set-cookie')
#                 if set_cookie_headers:
#                     for header in set_cookie_headers:
#                         network_cookies.append({
#                             'url': response.url,
#                             'set_cookie_header': header,
#                             'status': response.status,
#                             'timestamp': time.time(),
#                             'source': 'header'
#                         })
#             except Exception as e:
#                 logger.debug(f"Network monitoring error for {response.url}: {e}")

#         async def handle_request_finished(request):
#             try:
#                 response = await request.response()
#                 if response:
#                     cookies_header = await response.header_values('set-cookie')
#                     if cookies_header:
#                         for header in cookies_header:
#                             network_cookies.append({
#                                 'url': response.url,
#                                 'set_cookie_header': header,
#                                 'status': response.status,
#                                 'timestamp': time.time(),
#                                 'source': 'xhr'
#                             })
#             except Exception:
#                 pass

#         page.on('response', handle_response)
#         page.on('requestfinished', handle_request_finished)

#         # Inject JS MutationObserver to watch document.cookie changes
#         await page.add_init_script("""
#             (function() {
#                 const origCookie = document.__lookupSetter__('cookie');
#                 let lastCookie = document.cookie;
#                 setInterval(() => {
#                     if (document.cookie !== lastCookie) {
#                         lastCookie = document.cookie;
#                         window._cookieChanged = true;
#                     }
#                 }, 1000);
#             })();
#         """)


#     async def _scan_single_page(self, page: Page, url: str, options: Dict, consent_interactions: List) -> Dict:
#         """
#         Scans a single page, handles consent, scrolls,
#         and returns cookies, storage, AND links found on the page.
#         ✅ OPTIMIZED: Reduced waits, disabled scroll by default
#         """
#         logger.debug(f"Navigating to: {url}")
#         await page.goto(url, wait_until='load', timeout=60000)

#         await self._wait_for_dynamic_content(page)

#         if options.get('accept_consent', False):
#             await self._advanced_consent_handling(
#                 page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
#             )
#             await asyncio.sleep(2)

#         # ✅ OPTIMIZED: Scroll disabled by default (saves 3s per page)
#         if options.get('deep_scroll', False):
#             await self._enhanced_auto_scroll(page)
#             await self._wait_for_dynamic_content(page)

#         # ✅ OPTIMIZED: Reduced wait from 10s to 3s
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
#             'links': page_links
#         }

#     async def _wait_for_dynamic_content(self, page: Page):
#         """Wait for dynamic content to load (XHR, scripts, etc.)"""
#         try:
#             logger.debug(f"Waiting for network idle on {page.url}...")
#             await page.wait_for_load_state('networkidle', timeout=15000)
#             logger.debug(f"Network idle detected on {page.url}.")
#             await page.wait_for_timeout(1000)
#         except Exception as e:
#             logger.debug(f"Wait for dynamic content/networkidle finished or timed out: {e}")


#     async def _enhanced_auto_scroll(self, page: Page):
#         """Enhanced auto-scrolling to trigger lazy-loaded content"""
#         logger.debug(f"Performing enhanced scroll on {page.url}")
#         try:
#             await page.evaluate("""
#             async () => {
#                 const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
#                 let totalHeight = 0;
#                 const distance = 100;
#                 const maxScrolls = 100;
#                 let scrolls = 0;

#                 while (scrolls < maxScrolls) {
#                     const scrollHeight = document.body.scrollHeight;
#                     window.scrollBy(0, distance);
#                     await sleep(100);
#                     totalHeight += distance;
#                     scrolls++;

#                     if (window.innerHeight + window.scrollY >= scrollHeight || scrollHeight === document.body.scrollHeight) {
#                        window.scrollTo(0, document.body.scrollHeight);
#                        await sleep(200);
#                        break;
#                     }
#                 }
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
#         timeout_ms = timeout_sec * 1000

#         consent_selectors = [
#             '#onetrust-accept-btn-handler',
#             '[id*="consent"] button[id*="accept"]',
#              'button[id*="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]',
#             'button[class*="accept-all"]', 'button[class*="optanon-allow-all"]',
#             'button[id*="accept-all"]', 'button[data-accept-action]',
#             'button[data-testid*="accept"]', 'button[data-cy*="accept"]',
#             'button[data-gdpr-single-choice-accept]',
#             'button:text-matches("Accept all", "i")',
#             'button:text-matches("Allow all", "i")',
#             'button:text-matches("Agree", "i")',
#             'button:text-matches("Accept", "i")',
#             'button:text-matches("OK", "i")',
#             'button:text-matches("Got it", "i")',
#             'button[id*="cookie"]', 'button[class*="cookie"]',
#             'button[id*="consent"]', 'button[class*="consent"]',
#             '[role="dialog"] button:text-matches("Accept", "i")',
#             '[role="banner"] button:text-matches("Accept", "i")',
#             'button:text-matches("Accepter", "i")',
#             'button:text-matches("Aceptar", "i")',
#             'button:text-matches("Akzeptieren", "i")',
#         ]

#         iframe_selectors = [
#              'iframe[id*="consent"]', 'iframe[name*="consent"]',
#              'iframe[id*="cookie"]', 'iframe[name*="cookie"]',
#              'iframe[title*="consent" i]', 'iframe[title*="cookie" i]'
#         ]

#         success = False

#         for attempt in range(retries):
#             logger.debug(f"Consent detection attempt {attempt + 1}/{retries} on {page.url}")
#             clicked_in_attempt = False

#             for selector in consent_selectors:
#                 try:
#                     element = page.locator(selector).first
#                     if await element.is_visible(timeout=1000):
#                         logger.info(f"✅ Found potential consent button: {selector}")
#                         await element.click(timeout=3000)
#                         logger.info(f"✅ Clicked consent button: {selector}")
#                         consent_interactions.append({
#                             'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(), 'type': 'main_page'
#                         })
#                         clicked_in_attempt = True
#                         await page.wait_for_timeout(1500)
#                         break
#                 except Exception as e:
#                     logger.debug(f"Selector '{selector}' not found/visible: {e}")
#                     continue

#             if clicked_in_attempt:
#                 success = True
#                 break

#             logger.debug("Checking iframes for consent buttons...")
#             for frame_selector in iframe_selectors:
#                  try:
#                       frame_locator = page.locator(frame_selector).first
#                       if await frame_locator.is_visible(timeout=500):
#                             frame = await frame_locator.content_frame()
#                             if frame:
#                                 logger.debug(f"Searching within iframe: {frame_selector}")
#                                 for selector in consent_selectors[:15]:
#                                      try:
#                                           element = frame.locator(selector).first
#                                           if await element.is_visible(timeout=1000):
#                                                 logger.info(f"✅ Found consent button in iframe: {selector}")
#                                                 await element.click(timeout=3000)
#                                                 logger.info(f"✅ Clicked consent button in iframe: {selector}")
#                                                 consent_interactions.append({
#                                                     'selector': selector, 'attempt': attempt + 1, 'timestamp': time.time(),
#                                                     'type': 'iframe', 'iframe_selector': frame_selector
#                                                 })
#                                                 clicked_in_attempt = True
#                                                 await page.wait_for_timeout(1500)
#                                                 break
#                                      except Exception as e_iframe:
#                                           logger.debug(f"Selector in iframe failed: {e_iframe}")
#                                           continue
#                             if clicked_in_attempt: break
#                  except Exception as e_frame_check:
#                       logger.debug(f"Iframe check failed: {e_frame_check}")
#                       continue
#                  if clicked_in_attempt: break

#             if clicked_in_attempt:
#                 success = True
#                 break

#             if not clicked_in_attempt and attempt < retries - 1:
#                 logger.debug(f"Consent button not found in attempt {attempt + 1}, retrying...")
#                 await asyncio.sleep(1)

#         if success:
#             logger.info(f"🎉 Successfully interacted with consent banner on {page.url}")
#         else:
#             logger.info(f"ℹ No interactable consent banner found after {retries} attempts on {page.url}")

#         return success

#     # def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
#     #     """Remove duplicate cookies based on name, domain, and path."""
#     #     seen: Set[str] = set()
#     #     deduplicated = []
#     #     for cookie in cookies:
#     #         identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
#     #         if identifier not in seen:
#     #             seen.add(identifier)
#     #             deduplicated.append(cookie)

#     #     logger.debug(f"🔄 Deduplicated {len(cookies)} -> {len(deduplicated)} cookies")
#     #     return deduplicated

#     def _deduplicate_cookies(self, cookies: List[Dict]) -> List[Dict]:
#         """Remove ONLY exact duplicates (same name, domain, path)"""
#         seen: Set[str] = set()
#         deduplicated = []

#         for cookie in cookies:
#             # Exact match only - don't generalize
#             identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"

#             if identifier not in seen:
#                 seen.add(identifier)
#                 deduplicated.append(cookie)

#         logger.debug(f"Deduplicated {len(cookies)} → {len(deduplicated)} cookies")
#         return deduplicated

#     def _standardize_cookies(self, cookies: List[Dict], base_url: str) -> List[Dict]:
#         """Standardize cookie data format for consistency and add metadata."""
#         standardized = []
#         try:
#             url_parts = urlparse(base_url)
#             site_base_domain = self._get_base_domain(url_parts.netloc)
#             if not site_base_domain: site_base_domain = url_parts.netloc
#         except Exception:
#              logger.warning(f"Could not parse base_url {base_url}")
#              site_base_domain = base_url

#         for cookie in cookies:
#             try:
#                 cookie_domain = cookie.get('domain', '').lstrip('.')
#                 if not cookie_domain:
#                     cookie_domain = site_base_domain

#                 cookie_base_domain = self._get_base_domain(cookie_domain)

#                 samesite = cookie.get('sameSite')
#                 if samesite not in ['Strict', 'Lax', 'None']:
#                      samesite = 'Lax'

#                 standardized_cookie = {
#                     'name': cookie.get('name', ''),
#                     'value': cookie.get('value', ''),
#                     'domain': cookie_domain,
#                     'path': cookie.get('path', '/'),
#                     'expires': cookie.get('expires', -1),
#                     'httpOnly': cookie.get('httpOnly', False),
#                     'secure': cookie.get('secure', False),
#                     'sameSite': samesite,
#                     'is_third_party': cookie_base_domain != site_base_domain if site_base_domain and cookie_base_domain else False,
#                     'base_domain': cookie_base_domain or cookie_domain,
#                     'size_bytes': len(cookie.get('name', '').encode('utf-8') + b'=' + cookie.get('value', '').encode('utf-8')),
#                     'timestamp': time.time()
#                 }
#                 standardized.append(standardized_cookie)

#             except Exception as e:
#                 logger.warning(f"Cookie standardization error: {e}")
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
#             extracted = tldextract.extract(url_or_domain, include_psl_private_domains=True)
#             if extracted.registered_domain:
#                 return extracted.registered_domain
#             elif extracted.domain:
#                  return extracted.domain
#             else:
#                  return ""
#         except Exception as e:
#             logger.error(f"Error extracting base domain from '{url_or_domain}': {e}")
#             parts = url_or_domain.split('.')
#             if len(parts) >= 2:
#                  return ".".join(parts[-2:])
#             return url_or_domain


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
from http.cookies import SimpleCookie # ✅ PATCH: Import SimpleCookie to parse raw headers

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
        self.domain_cache: Dict[str, str] = {} # ✅ PATCH: Add cache for tldextract

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
            raise 

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
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
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

            # ✅ PATCH: Parse and process raw network cookies
            logger.info(f"Parsing {len(network_cookies)} raw network cookie headers...")
            parsed_network_cookies = []
            for item in network_cookies:
                try:
                    parsed_list = self._parse_set_cookie_header(item['set_cookie_header'], item['url'])
                    parsed_network_cookies.extend(parsed_list)
                except Exception as e:
                    logger.warning(f"Failed to parse Set-Cookie header: {item['set_cookie_header']} - Error: {e}")

            # ✅ PATCH: Merge context cookies AND network cookies
            all_found_cookies = final_all_context_cookies + parsed_network_cookies

            # Standardize the final list of cookies
            standardized_final_cookies = self._standardize_cookies(all_found_cookies, start_url)
            deduplicated_final_cookies = self._deduplicate_cookies(standardized_final_cookies)

            logger.info(f"✅ Crawl completed: Scanned {page_count} pages ({error_count} errors) in {crawl_duration:.2f}s. Found {len(deduplicated_final_cookies)} unique cookies (from {len(all_found_cookies)} total).")

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
                "network_cookies_found_count": len(network_cookies) # Renamed for clarity
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

            # ✅ PATCH: Implement 2-stage cookie scan
            # --- STAGE 1: Pre-Interaction Scan ---
            await page.goto(url, wait_until='load', timeout=60000)
            await self._wait_for_dynamic_content(page)
            await asyncio.sleep(2) # Wait for banner to load
            
            logger.debug(f"Capturing pre-consent cookies for {url}")
            pre_consent_cookies = await context.cookies()

            # --- STAGE 2: Interaction and Post-Interaction Scan ---
            # _scan_single_page now ONLY handles interaction and returns links/storage
            page_data = await self._scan_single_page(page, url, options, consent_interactions)

            logger.debug(f"Capturing post-consent cookies for {url}")
            post_consent_cookies = await context.cookies()
            
            page_end = time.time()
            # ✅ PATCH: Merge pre- and post-consent cookies
            all_page_cookies = pre_consent_cookies + post_consent_cookies

            # ✅✅ FIX: Deduplicate the cookie list before returning
            page_cookies_raw = []
            seen_cookies = set()
            for cookie in all_page_cookies:
                # Create a unique key for each cookie
                identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
                if identifier not in seen_cookies:
                    seen_cookies.add(identifier)
                    page_cookies_raw.append(cookie)
            
            logger.debug(f"Deduplicated {len(all_page_cookies)} -> {len(page_cookies_raw)} cookies for {url}")

            page_result = {
                "url": url,
                "status": "COMPLETED",
                "duration_seconds": round(page_end - page_start, 2),
                "cookies": page_cookies_raw, # Use the deduplicated list
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
            return None # Will be caught as an exception by gather

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
        ✅ PATCH: This function now ONLY handles page interaction (consent, scroll)
        and final data extraction (storage, links). Cookie collection is
        handled by the caller (_scan_page_concurrent).
        """
        
        # Navigation and initial wait are now done in _scan_page_concurrent
        # await page.goto(url, wait_until='load', timeout=60000)
        # await self._wait_for_dynamic_content(page)

        if options.get('accept_consent', False):
            await self._advanced_consent_handling(
                page, options['banner_timeout'], options['retry_banner_clicks'], consent_interactions
            )
            await asyncio.sleep(2) # Wait for actions to complete

        # ✅ OPTIMIZED: Scroll disabled by default (saves 3s per page)
        if options.get('deep_scroll', False):
            await self._enhanced_auto_scroll(page)
            await self._wait_for_dynamic_content(page) # Wait after scroll

        # ✅ OPTIMIZED: Reduced wait from 10s to 3s
        logger.debug(f"Waiting {options['wait_seconds']}s for post-interaction scripts on {url}")
        await asyncio.sleep(options['wait_seconds'])

        # --- Data Collection (Storage and Links ONLY) ---
        local_storage_data = {}
        session_storage_data = {}
        page_links = []

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
            # ✅ PATCH: Cookie collection removed from this function
            # 'js_cookies': js_cookies_str, 
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
    #    """Remove duplicate cookies based on name, domain, and path."""
    #    seen: Set[str] = set()
    #    deduplicated = []
    #    for cookie in cookies:
    #         identifier = f"{cookie.get('name', '')}|{cookie.get('domain', '')}|{cookie.get('path', '/')}"
    #         if identifier not in seen:
    #             seen.add(identifier)
    #             deduplicated.append(cookie)

    #    logger.debug(f"🔄 Deduplicated {len(cookies)} -> {len(deduplicated)} cookies")
    #    return deduplicated

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
        ✅ PATCH: Now caches results for performance.
        """
        if not url_or_domain or not isinstance(url_or_domain, str):
             return ""
        
        # ✅ PATCH: Use cache
        if url_or_domain in self.domain_cache:
            return self.domain_cache[url_or_domain]
            
        try:
            extracted = tldextract.extract(url_or_domain, include_psl_private_domains=True)
            if extracted.registered_domain:
                result = extracted.registered_domain
            elif extracted.domain:
                result = extracted.domain
            else:
                result = ""
            
            self.domain_cache[url_or_domain] = result # ✅ PATCH: Store in cache
            return result
        except Exception as e:
            logger.error(f"Error extracting base domain from '{url_or_domain}': {e}")
            parts = url_or_domain.split('.')
            if len(parts) >= 2:
                result = ".".join(parts[-2:])
            else:
                result = url_or_domain
            
            self.domain_cache[url_or_domain] = result # ✅ PATCH: Store in cache
            return result

    # ✅ PATCH: New helper function to parse raw Set-Cookie headers
    def _parse_set_cookie_header(self, header_str: str, request_url: str) -> List[Dict]:
        """
        Parses a raw Set-Cookie header string into a Playwright-like cookie dict.
        """
        cookies = SimpleCookie()
        cookies.load(header_str)
        
        parsed_list = []
        
        try:
            request_domain = urlparse(request_url).netloc
        except Exception:
            request_domain = ""

        for key, morsel in cookies.items():
            # Create a standard cookie dict
            cookie = {
                'name': morsel.key,
                'value': morsel.value,
                'domain': morsel['domain'].lstrip('.') if morsel['domain'] else request_domain,
                'path': morsel['path'] or '/',
                'expires': -1,
                'httpOnly': morsel['httponly'],
                'secure': morsel['secure'],
                'sameSite': 'Lax' # Default, SimpleCookie doesn't parse SameSite
            }

            # Handle expires
            if morsel['expires']:
                try:
                    # Convert expires string to timestamp
                    cookie['expires'] = time.mktime(time.strptime(morsel['expires'], "%a, %d %b %Y %H:%M:%S %Z"))
                except ValueError:
                    cookie['expires'] = -1 # Failed to parse

            # Handle SameSite (SimpleCookie doesn't support it well)
            if 'samesite=strict' in header_str.lower():
                cookie['sameSite'] = 'Strict'
            elif 'samesite=none' in header_str.lower():
                cookie['sameSite'] = 'None'
            elif 'samesite=lax' in header_str.lower():
                cookie['sameSite'] = 'Lax'

            parsed_list.append(cookie)
            
        return parsed_list
