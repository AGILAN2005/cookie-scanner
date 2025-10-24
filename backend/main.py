# Enhanced Main.py - Optimized FastAPI Application

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Optional
import uuid
import asyncio
import logging
import time

from models import (
    ScanRequest, JobResponse, Site, Job, EnrichedCookieDB, 
    RawCookie, JobStatus, SiteUpdateRequest,PageScanResult
)
from database import get_db, engine, Base
from worker import process_scan_job
from scanner import PlaywrightScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="World-Class Cookie Scanner API",
    description="Professional cookie scanning platform competing with CookieYes and Termly",
    version="2.0.0"
)

# Global scanner instance for better performance
scanner_instance = None

@app.on_event("startup")
async def on_startup():
    """Initialize application with enhanced configuration"""
    global scanner_instance
    
    logger.info("🚀 Starting World-Class Cookie Scanner API...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize scanner instance
    try:
        scanner_instance = PlaywrightScanner()
        await scanner_instance.initialize()
        logger.info("✅ Scanner initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize scanner: {e}")
        scanner_instance = None
    
    logger.info("🎉 Application startup completed")

@app.on_event("shutdown")
async def on_shutdown():
    """Graceful shutdown"""
    global scanner_instance
    
    logger.info("🔚 Shutting down application...")
    
    if scanner_instance:
        try:
            await scanner_instance.close()
            logger.info("✅ Scanner closed successfully")
        except Exception as e:
            logger.error(f"❌ Error closing scanner: {e}")
    
    logger.info("👋 Application shutdown completed")

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "World-Class Cookie Scanner API is running",
        "version": "2.0.0",
        "scanner_status": "ready" if scanner_instance else "initializing",
        "timestamp": time.time()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    scanner_status = "ready"
    scanner_details = {}
    
    if scanner_instance:
        try:
            # Test scanner functionality
            scanner_details = {
                "browser_initialized": scanner_instance.browser is not None,
                "playwright_initialized": scanner_instance.playwright is not None,
                "active_contexts": len(scanner_instance.contexts)
            }
        except Exception as e:
            scanner_status = "error"
            scanner_details = {"error": str(e)}
    else:
        scanner_status = "not_initialized"
    
    return {
        "status": "healthy",
        "scanner_status": scanner_status,
        "scanner_details": scanner_details,
        "timestamp": time.time()
    }

@app.post("/scan", response_model=JobResponse)
async def create_scan(scan_request: ScanRequest, db: Session = Depends(get_db)):
    """Create enhanced scan job with validation"""
    
    logger.info(f"📝 Creating scan job for: {scan_request.url}")
    
    try:
        # Enhanced URL validation
        if not _is_valid_url(str(scan_request.url)):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        # Check if site exists
        site = db.query(Site).filter(Site.url == str(scan_request.url)).first()
        
        if not site:
            site = Site(
                url=str(scan_request.url),
                type=scan_request.type,
                version=scan_request.version,
                owner_name=scan_request.ownerName,
                owner_email=scan_request.ownerEmail,
            )
            db.add(site)
            db.commit()
            db.refresh(site)
            logger.info(f"✅ Created new site: {site.id}")
        
        #-- UPDATED: Save the provided scan options to the new DB field
        new_job = Job(
            site_id=site.id,
            status=JobStatus.QUEUED,
            scan_options=scan_request.options.dict() # Convert Pydantic model to dict
        )
        
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        
        # Update site's last scan job
        site.last_scan_job_id = new_job.id
        db.commit()
        
        # Queue job for processing
        process_scan_job.delay(str(new_job.id))
        
        logger.info(f"🚀 Scan job queued: {new_job.id}")
        
        return JobResponse(
            job_id=str(new_job.id),
            status=new_job.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to create scan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create scan: {str(e)}")

@app.get("/sites")
def get_sites(db: Session = Depends(get_db)):
    """Get all sites with enhanced data"""
    
    try:
        sites_with_jobs = db.query(Site).options(
            joinedload(Site.jobs)
        ).order_by(Site.created_at.desc()).all()
        
        results = []
        
        for i, site in enumerate(sites_with_jobs):
            latest_job = None
            if site.last_scan_job_id:
                latest_job = next((job for job in site.jobs if job.id == site.last_scan_job_id), None)
            
            # Enhanced site information
            site_info = {
                "id": str(site.id),
                "siteId": f"WEB{str(i + 1).zfill(3)}",
                "url": site.url,
                "scanStatus": latest_job.status if latest_job else "PENDING",
                "type": site.type,
                "version": site.version,
                "owner": site.owner_name,
                "created": site.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "updated": site.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
                "status": "PUBLISHED" if latest_job and latest_job.status == JobStatus.COMPLETED else "PENDING",
                "lastScanJobId": str(site.last_scan_job_id) if site.last_scan_job_id else None,
                "totalScans": len(site.jobs),
                "lastScanDate": latest_job.completed_at.strftime("%d/%m/%Y %H:%M:%S") if latest_job and latest_job.completed_at else None,
                "cookieCount": latest_job.total_cookies if latest_job else 0
            }
            
            results.append(site_info)
        
        logger.info(f"📊 Retrieved {len(results)} sites")
        return results
        
    except Exception as e:
        logger.error(f"❌ Failed to fetch sites: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sites: {str(e)}")

@app.put("/site/{site_id}")
def update_site(site_id: str, site_update: SiteUpdateRequest, db: Session = Depends(get_db)):
    """Update site information"""
    
    try:
        site = db.query(Site).filter(Site.id == site_id).first()
        
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
        
        # Update fields
        site.version = site_update.version
        site.owner_name = site_update.owner_name
        site.owner_email = site_update.owner_email
        site.type = site_update.type
        
        db.commit()
        db.refresh(site)
        
        logger.info(f"✅ Updated site: {site_id}")
        return site
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update site: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update site: {str(e)}")

@app.delete("/site/{site_id}", status_code=204)
def delete_site(site_id: str, db: Session = Depends(get_db)):
    """Delete site and associated data"""
    
    try:
        site = db.query(Site).filter(Site.id == site_id).first()
        
        if not site:
            raise HTTPException(status_code=404, detail="Site not found")
        
        # Delete associated jobs and cookies (cascade should handle this)
        db.delete(site)
        db.commit()
        
        logger.info(f"🗑️ Deleted site: {site_id}")
        return {"message": "Site deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to delete site: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete site: {str(e)}")

# @app.get("/result/{job_id}")
# def get_scan_result(job_id: str, db: Session = Depends(get_db)):
#     """Get comprehensive scan results"""
    
#     try:
#         job = db.query(Job).filter(Job.id == job_id).first()
        
#         if not job:
#             raise HTTPException(status_code=404, detail="Job not found")
        
#         if job.status != JobStatus.COMPLETED:
#             return {
#                 "status": job.status,
#                 "message": "Scan not completed yet.",
#                 "progress": _get_job_progress(job),
#                 "estimated_completion": _estimate_completion_time(job)
#             }
        
#         # Get enriched cookies
#         enriched_cookies = db.query(EnrichedCookieDB).filter(EnrichedCookieDB.job_id == job.id).all()
#         raw_cookies_dict = {rc.name: rc for rc in db.query(RawCookie).filter(RawCookie.job_id == job.id).all()}
        
#         # Build comprehensive cookie results
#         cookie_results = []
#         for ec in enriched_cookies:
#             raw_cookie = raw_cookies_dict.get(ec.normalized_name)
            
#             cookie_data = {
#                 "name": ec.normalized_name,
#                 "category": ec.type,
#                 "domain": ec.base_domain,
#                 "purpose": ec.description,
#                 "duration_human": ec.duration_human,
#                 "duration_iso": ec.duration_iso,
#                 "secure": raw_cookie.secure if raw_cookie else False,
#                 "httpOnly": raw_cookie.httponly if raw_cookie else False,
#                 "sameSite": raw_cookie.samesite if raw_cookie else None,
#                 "vendor": ec.kb_source or ec.base_domain,
#                 "is_third_party": ec.is_third_party,
#                 "confidence": ec.confidence,
#                 "data_source": ec.kb_source,
#                 "size": len(raw_cookie.value) if raw_cookie else 0
#             }
            
#             cookie_results.append(cookie_data)
        
#         # Enhanced scan results
#         result = {
#             "url": job.site.url,
#             "scannedAt": job.completed_at.isoformat(),
#             "totalCookies": job.total_cookies,
#             "summaryByCategory": job.summary_by_category,
#             "cookies": cookie_results,
#             "scanMetadata": {
#                 "duration_seconds": (job.completed_at - job.started_at).total_seconds() if job.started_at and job.completed_at else None,
#                 "pages_scanned": job.pages_scanned or 1,
#                 "consent_interactions": job.consent_interactions or 0,
#                 "scan_version": "2.0.0",
#                 "scanner_type": "PlaywrightScanner"
#             },
#             "complianceInsights": _generate_compliance_insights(cookie_results),
#             "recommendations": _generate_recommendations(cookie_results)
#         }
        
#         logger.info(f"📊 Retrieved scan results for job: {job_id}")
#         return result
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"❌ Failed to get scan result: {e}")
#         raise HTTPException(status_code=500, detail=f"Failed to get scan result: {str(e)}")

@app.get("/result/{job_id}")
def get_scan_result(job_id: str, db: Session = Depends(get_db)):
    """MODIFIED: Get comprehensive scan results with page-level metadata"""
    
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status not in [JobStatus.COMPLETED, JobStatus.FAILED]: # Allow viewing failed jobs
            return {
                "status": job.status,
                "message": "Scan not completed yet.",
                "progress": _get_job_progress(job, db), # Pass DB for progress
                "estimated_completion": _estimate_completion_time(job)
            }
            
        # Get enriched cookies
        enriched_cookies = db.query(EnrichedCookieDB).filter(EnrichedCookieDB.job_id == job.id).all()
        
        # Get all raw cookies for this job (to find raw details)
        raw_cookies_map = {
            rc.unique_key: rc for rc in db.query(RawCookie).filter(RawCookie.job_id == job.id).all()
        }
        
        # --- NEW: Get Page Scan Metadata (Goal 3) ---
        page_scan_results = db.query(PageScanResult).filter(PageScanResult.job_id == job.id).order_by(PageScanResult.page_url).all()
        pages_scanned_details = [
            {
                "url": p.page_url,
                "status": p.status,
                "scan_duration_seconds": p.scan_duration,
                "cookies_found": p.cookies_found_count,
                "error": p.error
            } for p in page_scan_results
        ]
        
        # Build comprehensive cookie results
        cookie_results = []
        for ec in enriched_cookies:
            # Find the corresponding raw cookie
            raw_cookie = raw_cookies_map.get(ec.raw_cookie_unique_key)
            
            cookie_data = {
                "name": ec.normalized_name,
                "category": ec.type,
                "domain": ec.base_domain,
                "purpose": ec.description,
                "duration_human": ec.duration_human,
                "duration_iso": ec.duration_iso,
                "secure": raw_cookie.secure if raw_cookie else False,
                "httpOnly": raw_cookie.httponly if raw_cookie else False,
                "sameSite": raw_cookie.samesite if raw_cookie else None,
                "vendor": ec.kb_source or ec.base_domain,
                "is_third_party": ec.is_third_party,
                "confidence": ec.confidence,
                "data_source": ec.kb_source,
                "size": len(raw_cookie.value) if raw_cookie else 0,
                "source_type": raw_cookie.source if raw_cookie else 'browser' # 'browser', 'local', 'session'
            }
            
            cookie_results.append(cookie_data)
        
        # Enhanced scan results
        result = {
            "url": job.site.url,
            "scannedAt": job.completed_at.isoformat() if job.completed_at else None,
            "totalUniqueCookies": job.total_cookies,
            "summaryByCategory": job.summary_by_category,
            "cookies": cookie_results,
            "scanMetadata": {
                "duration_seconds": (job.completed_at - job.started_at).total_seconds() if job.started_at and job.completed_at else None,
                "pages_scanned_count": job.pages_scanned,
                "consent_interactions": job.consent_interactions,
                "scan_version": "2.1.0-crawler", # New version
                "scanner_type": "PlaywrightScanner (Crawl Mode)",
                # --- NEW: Page-level metadata ---
                "pages_scanned_details": pages_scanned_details 
            },
            "complianceInsights": _generate_compliance_insights(cookie_results),
            "recommendations": _generate_recommendations(cookie_results),
            "error": job.error if job.status == JobStatus.FAILED else None
        }
        
        logger.info(f"📊 Retrieved scan results for job: {job_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get scan result: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get scan result: {str(e)}")


@app.get("/status/{job_id}")
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """Get detailed job status"""
    
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        status_info = {
            "job_id": str(job.id),
            "status": job.status,
            "error": job.error,
            "progress": _get_job_progress(job,db),
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "duration_seconds": (job.completed_at - job.started_at).total_seconds() if job.started_at and job.completed_at else None,
            "estimated_completion": _estimate_completion_time(job) if job.status in [JobStatus.QUEUED, JobStatus.RUNNING] else None
        }
        
        return status_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get job status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get job status: {str(e)}")

@app.post("/scan/immediate")
async def immediate_scan(scan_request: ScanRequest, background_tasks: BackgroundTasks):
    """Immediate scan for testing purposes"""
    
    if not scanner_instance:
        raise HTTPException(status_code=503, detail="Scanner not available")
    
    try:
        logger.info(f"🚀 Starting immediate scan of: {scan_request.url}")
        
        # Perform immediate scan
        scan_options = {
            "wait_seconds": 10,
            "max_pages": 1,
            "deep_scroll": True,
            "banner_timeout": 5,
            "retry_banner_clicks": 2
        }
        
        results = await scanner_instance.scan_url(str(scan_request.url), scan_options)
        
        # Return immediate results
        return {
            "url": str(scan_request.url),
            "status": "completed",
            "cookies_found": len(results.get('browser_cookies', [])),
            "pages_scanned": len(results.get('visited_urls', [])),
            "scan_duration": results.get('scan_metadata', {}).get('duration_seconds'),
            "timestamp": time.time(),
            "detailed_results": results
        }
        
    except Exception as e:
        logger.error(f"❌ Immediate scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

# Utility functions

def _is_valid_url(url: str) -> bool:
    """Validate URL format"""
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

# def _get_job_progress(job) -> Dict:
#     """Calculate job progress"""
#     if job.status == JobStatus.COMPLETED:
#         return {"percentage": 100, "stage": "completed"}
#     elif job.status == JobStatus.RUNNING:
#         return {"percentage": 50, "stage": "scanning"}
#     elif job.status == JobStatus.QUEUED:
#         return {"percentage": 0, "stage": "queued"}
#     else:
#         return {"percentage": 0, "stage": "unknown"}

def _get_job_progress(job, db: Session) -> Dict:
    """MODIFIED: Calculate job progress based on crawl"""
    if job.status == JobStatus.COMPLETED:
        return {"percentage": 100, "stage": "completed"}
    elif job.status == JobStatus.FAILED:
        return {"percentage": 100, "stage": "failed"}
    elif job.status == JobStatus.ENRICHING:
        return {"percentage": 90, "stage": "enriching"}
    elif job.status == JobStatus.RUNNING:
        return {"percentage": 80, "stage": "processing_data"}
    elif job.status == JobStatus.CRAWLING:
        # Try to get a percentage
        try:
            total_pages = db.query(PageScanResult).filter(PageScanResult.job_id == job.id).count()
            max_pages = job.scan_options.get('max_pages', 300)
            percentage = min(75, int((total_pages / max_pages) * 75)) # Crawling is 0-75%
            return {"percentage": percentage, "stage": f"crawling_page_{total_pages}"}
        except Exception:
            return {"percentage": 10, "stage": "crawling"}
    elif job.status == JobStatus.QUEUED:
        return {"percentage": 0, "stage": "queued"}
    else:
        return {"percentage": 0, "stage": "unknown"}

def _estimate_completion_time(job) -> Optional[str]:
    """Estimate job completion time"""
    if job.status == JobStatus.COMPLETED:
        return None
    
    # Simple estimation based on average scan time
    average_scan_time = 60  # seconds
    
    if job.started_at:
        elapsed = (time.time() - job.started_at.timestamp())
        remaining = max(0, average_scan_time - elapsed)
        return f"{int(remaining)} seconds"
    else:
        return f"{average_scan_time} seconds"

def _generate_compliance_insights(cookies: List[Dict]) -> Dict:
    """Generate compliance insights"""
    
    total_cookies = len(cookies)
    third_party = len([c for c in cookies if c.get('is_third_party')])
    tracking_cookies = len([c for c in cookies if c.get('category') in ['Analytics', 'Advertising']])
    
    return {
        "total_cookies": total_cookies,
        "third_party_cookies": third_party,
        "tracking_cookies": tracking_cookies,
        "compliance_score": max(0, 100 - (third_party * 2) - (tracking_cookies * 3)),
        "gdpr_impact": "high" if tracking_cookies > 5 else "medium" if tracking_cookies > 0 else "low",
        "ccpa_impact": "high" if third_party > 3 else "medium" if third_party > 0 else "low"
    }

def _generate_recommendations(cookies: List[Dict]) -> List[str]:
    """Generate compliance recommendations"""
    
    recommendations = []
    
    third_party = len([c for c in cookies if c.get('is_third_party')])
    tracking_cookies = len([c for c in cookies if c.get('category') in ['Analytics', 'Advertising']])
    
    if tracking_cookies > 0:
        recommendations.append("Implement cookie consent banner for analytics and advertising cookies")
    
    if third_party > 5:
        recommendations.append("Review third-party cookie usage and consider alternatives")
    
    insecure_cookies = len([c for c in cookies if not c.get('secure')])
    if insecure_cookies > 0:
        recommendations.append(f"Set Secure flag on {insecure_cookies} cookies for HTTPS sites")
    
    if len(recommendations) == 0:
        recommendations.append("Your cookie usage appears compliant with current standards")
    
    return recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)