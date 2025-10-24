# #worker.py - Celery worker for processing cookie scan jobs with advanced scanning and enrichment

# import asyncio
# from celery import Celery
# from sqlalchemy.orm import sessionmaker
# from collections import Counter
# from datetime import datetime
# import os
# import sys
# import tldextract
# from scanner import PlaywrightScanner
# from enrichment import WorldClassCookieEnricher
# from models import Job, Site, JobStatus, RawCookie, EnrichedCookieDB
# from database import engine

# # This line is for local Windows development and doesn't affect Docker
# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# # Initialize Celery to connect to Redis using the environment variable from docker-compose
# # The second argument is a fallback for local development
# celery_app = Celery('cookie_worker',
#                     broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
#                     backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

# SessionLocal = sessionmaker(bind=engine)

# def _get_base_domain(url_or_domain: str) -> str:
#     """
#     Accurately extract the base domain (e.g., google.com) from a URL 
#     or domain string using tldextract.
#     """
#     try:
#         extracted = tldextract.extract(url_or_domain,cache_dir="/tmp")
#         if extracted.domain and extracted.suffix:
#             return f"{extracted.domain}.{extracted.suffix}"
#         return extracted.domain or url_or_domain
#     except Exception:
#         return url_or_domain

# @celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
# def process_scan_job(self, job_id: str):
#     """
#     The main Celery task that orchestrates the entire scan and enrichment process.
#     This synchronous function sets up an asyncio event loop to run our async code.
#     """
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     try:
#         loop.run_until_complete(async_process_scan_job(job_id))
#     finally:
#         loop.close()

# async def async_process_scan_job(job_id: str):
#     """
#     The core async function that performs the scan, enrichment, and database operations.
#     """
#     db = SessionLocal()
#     scanner = None
#     job = db.query(Job).filter(Job.id == job_id).first()
    
#     if not job:
#         print(f"❌ Job {job_id} not found.")
#         return

#     try:
#         # --- 1. SCANNING PHASE ---
#         job.status = JobStatus.RUNNING
#         job.started_at = datetime.utcnow()
#         db.commit()
      
#         # Instantiate the advanced scanner
#         scanner = PlaywrightScanner()
#         await scanner.initialize()
        
#         # Use scan options from the job if they exist
#         scan_options = job.scan_options or {}
#         raw_data = await scanner.scan_url(job.site.url, scan_options)
    
#         # Save comprehensive metadata from the scan results
#         job.pages_scanned = len(raw_data.get('visited_urls', [job.site.url]))
#         job.consent_interactions = len(raw_data.get('consent_interactions', []))
#         db.commit()

#         all_items_to_enrich = []
#         site_base_domain = _get_base_domain(job.site.url)
        
#         cookies = raw_data['browser_cookies']
#         all_items_to_enrich.extend(cookies)
        
#         for key, value in raw_data.get('local_storage', {}).items():
#             all_items_to_enrich.append({
#                 'name': key,
#                 'value': str(value),
#                 'domain': site_base_domain,
#                 'source': 'local',
#                 'path': '/',
#                 'expires': -1,
#                 'httpOnly': False,
#                 'secure': False,
#                 'sameSite': 'None'
#             })
            
#         for key, value in raw_data.get('session_storage', {}).items():
#             all_items_to_enrich.append({
#                 'name': key,
#                 'value': str(value),
#                 'domain': site_base_domain,
#                 'source': 'session',
#                 'path': '/',
#                 'expires': -1,
#                 'httpOnly': False,
#                 'secure': False,
#                 'sameSite': 'None'
#             })
        
#         # Persist all raw cookies found by the scanner
#         for item in all_items_to_enrich:
#             db.add(RawCookie(
#                 job_id=job.id,
#                 name=item['name'],
#                 value=item.get('value', ''),
#                 domain=item.get('domain', ''),
#                 path=item.get('path', '/'),
#                 expiry_epoch=item.get('expires', -1),
#                 secure=item.get('secure', False),
#                 httponly=item.get('httpOnly', False),
#                 samesite=item.get('sameSite', 'None'),
#                 source=item.get('source', 'browser') # Default to 'browser' if not specified
#             ))
#         db.commit()
        
        
#         # --- 2. ENRICHMENT PHASE ---
#         job.status = JobStatus.ENRICHING
#         db.commit()
    
#         api_key = os.getenv('GOOGLE_API_KEY')
#         db_path = os.getenv('COOKIE_DB_PATH', 'exhaustive_cookie_database.json')
        
       
#         enricher = WorldClassCookieEnricher(google_api_key=api_key, cookie_db_path=db_path)
        
#         enrichment_cache = {}
#         enriched_list = []
        
#         for item in all_items_to_enrich:
#             enriched = await enricher.enrich_cookie(item, job.site.url, enrichment_cache)
#             enriched_list.append(enriched)
#             db.add(EnrichedCookieDB(
#                 job_id=job.id,
#                 normalized_name=enriched['cookie'], 
#                 base_domain=enriched['domain'],
#                 description=enriched['description'],
#                 duration_iso=enriched['duration_iso'],
#                 duration_human=enriched['duration_human'],
#                 type=enriched['type'],
#                 confidence=enriched['confidence'],
#                 kb_source=enriched.get('kb_source'),
#                 is_third_party=enriched['is_third_party']
#             ))
#         db.commit()
        
#         category_counts = Counter([e['type'] for e in enriched_list])
#         job.status = JobStatus.COMPLETED
#         job.completed_at = datetime.utcnow()
#         job.total_cookies = len(all_items_to_enrich) 
#         job.summary_by_category = dict(category_counts)
        
#         # Update the parent site with the latest scan information
#         site = db.query(Site).filter(Site.id == job.site_id).first()
#         if site:
#             site.last_scan_job_id = job.id
#             site.last_scan_date = job.completed_at
        
#         db.commit()
#         print(f"✅ Scan completed successfully for job_id: {job_id}")
        
#     except Exception as e:
#         print(f"❌ Error in scan job {job_id}: {e}")
#         if job:
#             job.status = JobStatus.FAILED
#             job.error = str(e)
#             job.completed_at = datetime.utcnow()
#             db.commit()
#     finally:
#         if scanner:
#             await scanner.close()
#         db.close()

#worker.py - Celery worker for processing cookie scan jobs with advanced scanning and enrichment

import asyncio
from celery import Celery
from sqlalchemy.orm import sessionmaker
from collections import Counter
from datetime import datetime
import os
import sys
import tldextract
import uuid

from scanner import PlaywrightScanner
from enrichment import WorldClassCookieEnricher,WorldClassCookieKnowledgeBase
from models import (
    Job, Site, JobStatus, RawCookie, EnrichedCookieDB, 
    PageScanResult, PageRawCookieAssociation
)
from database import engine

# (Celery app setup as before)
celery_app = Celery('cookie_worker',
                    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
                    backend=os.getenv('REDIS_URL', 'redis://localhost:6379/0'))

SessionLocal = sessionmaker(bind=engine)

def _get_base_domain(url_or_domain: str) -> str:
    # (Same logic as before)
    try:
        extracted = tldextract.extract(url_or_domain, cache_dir="/tmp")
        if extracted.domain and extracted.suffix:
            return f"{extracted.domain}.{extracted.suffix}"
        return extracted.domain or url_or_domain
    except Exception:
        return url_or_domain


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def process_scan_job(self, job_id: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(async_process_scan_job(job_id))
    finally:
        loop.close()


async def async_process_scan_job(job_id: str):
    """
    REWRITTEN: The core async function that calls the crawler,
    processes results, and saves to the new DB schema.
    """
    db = SessionLocal()
    scanner = None
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        print(f"❌ Job {job_id} not found.")
        return

    # Map to store unique RawCookie objects for this job
    # key: 'name|domain|path|source', value: RawCookie object
    job_raw_cookies_map = {}
    
    try:
        # --- 1. CRAWLING & SCANNING PHASE ---
        job.status = JobStatus.CRAWLING
        job.started_at = datetime.utcnow()
        db.commit()
        
        scanner = PlaywrightScanner()
        await scanner.initialize()
        
        # Pass scan options from the job
        scan_options = job.scan_options or {}
        
        # This one function now does the entire crawl
        crawl_data = await scanner.run_crawl_and_scan(job.site.url, scan_options)
        
        job.status = JobStatus.RUNNING # Change status to "processing"
        db.commit()

        site_base_domain = _get_base_domain(job.site.url)
        all_items_to_enrich = [] # This will be the deduplicated list

        # --- 2. SAVING PAGE & COOKIE DATA (Goal 3) ---
        for page_res in crawl_data.get('page_results', []):
            # 2a. Save the PageScanResult
            page_scan_entry = PageScanResult(
                id=uuid.uuid4(),
                job_id=job.id,
                site_id=job.site_id,
                page_url=page_res['url'],
                scan_duration=page_res['duration_seconds'],
                status=page_res['status'],
                cookies_found_count=len(page_res['cookies']) + len(page_res['local_storage']) + len(page_res['session_storage']),
                error=page_res.get('error')
            )
            db.add(page_scan_entry)
            db.flush() # Need the ID for associations
            
            if page_res['status'] == 'FAILED':
                continue # Skip cookie processing for failed pages
                
            # --- Combine all items from this page ---
            page_items = []
            page_items.extend(page_res.get('cookies', []))
            
            for key, value in page_res.get('local_storage', {}).items():
                page_items.append({
                    'name': key, 'value': str(value), 'domain': site_base_domain,
                    'source': 'local', 'path': '/', 'expires': -1,
                    'httpOnly': False, 'secure': False, 'sameSite': 'None'
                })
            for key, value in page_res.get('session_storage', {}).items():
                page_items.append({
                    'name': key, 'value': str(value), 'domain': site_base_domain,
                    'source': 'session', 'path': '/', 'expires': -1,
                    'httpOnly': False, 'secure': False, 'sameSite': 'None'
                })

            # 2b. Process each item (cookie/storage) found on the page
            for item in page_items:
                item_name = item.get('name', 'UNKNOWN')
                item_domain = item.get('domain', site_base_domain)
                item_path = item.get('path', '/')
                item_source = item.get('source', 'browser')
                
                # Create a unique key for this cookie type
                unique_key = f"{item_name}|{item_domain}|{item_path}|{item_source}"
                
                raw_cookie_entry = None
                if unique_key not in job_raw_cookies_map:
                    # This is the first time we've seen this cookie in this job
                    raw_cookie_entry = RawCookie(
                        id=uuid.uuid4(),
                        job_id=job.id,
                        unique_key=unique_key,
                        name=item_name,
                        value=item.get('value', ''),
                        domain=item_domain,
                        path=item_path,
                        expiry_epoch=item.get('expires', -1),
                        secure=item.get('secure', False),
                        httponly=item.get('httpOnly', False),
                        samesite=item.get('sameSite', 'None'),
                        source=item_source
                    )
                    db.add(raw_cookie_entry)
                    db.flush() # Need the ID
                    job_raw_cookies_map[unique_key] = raw_cookie_entry
                    all_items_to_enrich.append(item) # Add the *original data* for enrichment
                else:
                    raw_cookie_entry = job_raw_cookies_map[unique_key]
                
                # 2c. Create the association
                association = PageRawCookieAssociation(
                    page_scan_result_id=page_scan_entry.id,
                    raw_cookie_id=raw_cookie_entry.id
                )
                db.add(association)

        # Commit all page scans, raw cookies, and associations
        db.commit()

        # --- 3. ENRICHMENT PHASE (Goal 2) ---
        job.status = JobStatus.ENRICHING
        db.commit()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        db_path = os.getenv('COOKIE_DB_PATH', 'exhaustive_cookie_database.json')
        
        enricher = WorldClassCookieEnricher(google_api_key=api_key, cookie_db_path=db_path)
        
        enrichment_cache = {}
        enriched_list = []
        
        for item in all_items_to_enrich:
            # Pass the site_url for better AI context
            enriched = await enricher.enrich_cookie(item, job.site.url, enrichment_cache)
            enriched_list.append(enriched)
            
            # Find the matching unique_key
            item_name = item.get('name', 'UNKNOWN')
            item_domain = item.get('domain', site_base_domain)
            item_path = item.get('path', '/')
            item_source = item.get('source', 'browser')
            unique_key = f"{item_name}|{item_domain}|{item_path}|{item_source}"

            db.add(EnrichedCookieDB(
                job_id=job.id,
                raw_cookie_unique_key=unique_key, # <-- Save the link
                normalized_name=enriched['cookie'], 
                base_domain=enriched['domain'],
                description=enriched['description'],
                duration_iso=enriched['duration_iso'],
                duration_human=enriched['duration_human'],
                type=enriched['type'],
                confidence=enriched['confidence'],
                kb_source=enriched.get('kb_source'),
                is_third_party=enriched['is_third_party']
            ))
        db.commit()
        WorldClassCookieKnowledgeBase.save_to_json()

        # --- 4. FINALIZATION ---
        category_counts = Counter([e['type'] for e in enriched_list])
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        job.total_cookies = len(all_items_to_enrich) # Total *unique* cookies
        job.summary_by_category = dict(category_counts)
        job.pages_scanned = crawl_data['scan_metadata']['pages_scanned_count']
        job.consent_interactions = crawl_data['consent_interactions_count']
        
        site = db.query(Site).filter(Site.id == job.site_id).first()
        if site:
            site.last_scan_job_id = job.id
            site.last_scan_date = job.completed_at
            
        db.commit()
        print(f"✅ Crawl & Scan completed successfully for job_id: {job_id}")
        
    except Exception as e:
        print(f"❌ Error in scan job {job_id}: {e}")
        if job:
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()
    finally:
        if scanner:
            await scanner.close()
        db.close()