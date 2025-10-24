# # models.py - Pydantic models and SQLAlchemy ORM definitions

# from datetime import datetime
# from enum import Enum
# from typing import Optional, List
# from pydantic import BaseModel, HttpUrl
# from sqlalchemy import (
#     Column, String, DateTime, Integer, JSON, Float,
#     Boolean, Text, ForeignKey
# )
# from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
# import uuid

# from database import Base

# class JobStatus(str, Enum):
#     QUEUED = "QUEUED"
#     RUNNING = "RUNNING"
#     ENRICHING = "ENRICHING"
#     COMPLETED = "COMPLETED"
#     FAILED = "FAILED"

# class ScanOptions(BaseModel):
#     accept_consent: bool = False
#     simulate_user_actions: List[str] = ["scroll"]
#     headless: bool = True
#     wait_seconds: int = 10

# class ScanRequest(BaseModel):
#     url: HttpUrl
#     type: Optional[str] = 'ROOT'
#     version: Optional[str] = None
#     ownerName: Optional[str] = None
#     ownerEmail: Optional[str] = None
#     options: ScanOptions = ScanOptions()

# class JobResponse(BaseModel):
#     job_id: str
#     status: JobStatus

# class SiteUpdateRequest(BaseModel):
#     version: str
#     owner_name: str
#     owner_email: str
#     type: str

# class Site(Base):
#     """Master table for all registered websites."""
#     __tablename__ = "sites"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     url = Column(Text, nullable=False, unique=True)
#     type = Column(String, nullable=False)
#     version = Column(String)
#     owner_name = Column(Text, nullable=False)
#     owner_email = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     last_scan_job_id = Column(UUID(as_uuid=True), nullable=True)
#     last_scan_date = Column(DateTime, nullable=True)

#     jobs = relationship("Job", back_populates="site")

# class Job(Base):
#     """Table for every individual scan job."""
#     __tablename__ = "jobs"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    
#     status = Column(String, default=JobStatus.QUEUED)
#     error = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     started_at = Column(DateTime)
#     completed_at = Column(DateTime)
    
#     total_cookies = Column(Integer)
#     summary_by_category = Column(JSON)
    
#     pages_scanned = Column(Integer, default=1)
#     consent_interactions = Column(Integer, default=0)
#     scan_options = Column(JSON)
    
#     site = relationship("Site", back_populates="jobs")

# class RawCookie(Base):
#     """Table for raw cookie data from a scan."""
#     __tablename__ = "raw_cookies"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
#     name = Column(Text, nullable=False)
#     value = Column(Text)
#     domain = Column(Text)
#     path = Column(Text)
#     expiry_epoch = Column(Float)
#     secure = Column(Boolean)
#     httponly = Column(Boolean)
#     samesite = Column(Text)
#     source = Column(Text)

# class EnrichedCookieDB(Base):
#     """Table for processed, enriched cookie data."""
#     __tablename__ = "enriched_cookies"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
#     normalized_name = Column(Text)
#     base_domain = Column(Text)
#     description = Column(Text)
#     type = Column(Text)
#     confidence = Column(Float)
#     duration_iso = Column(Text)
#     duration_human = Column(Text)
#     kb_source = Column(Text)
#     llm_prompt = Column(Text)
#     llm_response = Column(Text)
#     is_third_party = Column(Boolean, default=False)
   
# models.py - Pydantic models and SQLAlchemy ORM definitions

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from sqlalchemy import (
    Column, String, DateTime, Integer, JSON, Float,
    Boolean, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    CRAWLING = "CRAWLING"  # <-- NEW
    RUNNING = "RUNNING"
    ENRICHING = "ENRICHING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ScanOptions(BaseModel):
    accept_consent: bool = False
    simulate_user_actions: List[str] = ["scroll"]
    headless: bool = True
    wait_seconds: int = 10
    max_pages: int = 5  # <-- NEW: Add a limit to the crawl

class ScanRequest(BaseModel):
    url: HttpUrl
    type: Optional[str] = 'ROOT'
    version: Optional[str] = None
    ownerName: Optional[str] = None
    ownerEmail: Optional[str] = None
    options: ScanOptions = ScanOptions()

class JobResponse(BaseModel):
    job_id: str
    status: JobStatus

class SiteUpdateRequest(BaseModel):
    version: str
    owner_name: str
    owner_email: str
    type: str

class Site(Base):
    """Master table for all registered websites."""
    __tablename__ = "sites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(Text, nullable=False, unique=True)
    type = Column(String, nullable=False)
    version = Column(String)
    owner_name = Column(Text, nullable=False)
    owner_email = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    last_scan_job_id = Column(UUID(as_uuid=True), nullable=True)
    last_scan_date = Column(DateTime, nullable=True)

    jobs = relationship("Job", back_populates="site")
    # NEW: Relationship to page scan results
    page_scans = relationship("PageScanResult", back_populates="site")


class Job(Base):
    """Table for every individual scan job."""
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False)
    
    status = Column(String, default=JobStatus.QUEUED)
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    total_cookies = Column(Integer)
    summary_by_category = Column(JSON)
    
    pages_scanned = Column(Integer, default=0) # <-- This will now be a counter
    consent_interactions = Column(Integer, default=0)
    scan_options = Column(JSON)
    
    site = relationship("Site", back_populates="jobs")
    # NEW: Relationship to page scan results
    page_scan_results = relationship("PageScanResult", back_populates="job")


# NEW TABLE: Stores metadata for each page scanned (Goal 3)
class PageScanResult(Base):
    __tablename__ = "page_scan_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    site_id = Column(UUID(as_uuid=True), ForeignKey("sites.id"), nullable=False) # For easier querying
    
    page_url = Column(Text, nullable=False)
    scan_duration = Column(Float)
    status = Column(String, nullable=False) # e.g., 'COMPLETED', 'FAILED'
    cookies_found_count = Column(Integer, default=0)
    error = Column(Text)
    
    job = relationship("Job", back_populates="page_scan_results")
    site = relationship("Site", back_populates="page_scans")
    
    # NEW: Many-to-Many relationship with RawCookie
    raw_cookies = relationship(
        "RawCookie",
        secondary="page_raw_cookie_association",
        back_populates="found_on_pages"
    )


class RawCookie(Base):
    """Table for raw cookie data from a scan. A cookie is unique per job."""
    __tablename__ = "raw_cookies"
    
    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # <-- Use UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
    # Unique identifier for a cookie type within a job
    unique_key = Column(String, index=True) # e.g., 'name|domain|path|source'
    
    name = Column(Text, nullable=False)
    value = Column(Text)
    domain = Column(Text)
    path = Column(Text)
    expiry_epoch = Column(Float)
    secure = Column(Boolean)
    httponly = Column(Boolean)
    samesite = Column(Text)
    source = Column(Text) # 'browser', 'local', 'session'

    # NEW: Many-to-Many relationship with PageScanResult
    found_on_pages = relationship(
        "PageScanResult",
        secondary="page_raw_cookie_association",
        back_populates="raw_cookies"
    )


# NEW TABLE: Association table for Many-to-Many relationship
class PageRawCookieAssociation(Base):
    __tablename__ = "page_raw_cookie_association"
    
    page_scan_result_id = Column(UUID(as_uuid=True), ForeignKey("page_scan_results.id"), primary_key=True)
    raw_cookie_id = Column(UUID(as_uuid=True), ForeignKey("raw_cookies.id"), primary_key=True)


class EnrichedCookieDB(Base):
    """Table for processed, enriched cookie data. One entry per job per unique cookie."""
    __tablename__ = "enriched_cookies"
    
    id = Column(Integer, primary_key=True, autoincrement=True) # Keep this as is
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
    # This should match the RawCookie's unique_key
    raw_cookie_unique_key = Column(String, index=True) # <-- NEW
    
    normalized_name = Column(Text)
    base_domain = Column(Text)
    description = Column(Text)
    type = Column(Text)
    confidence = Column(Float)
    duration_iso = Column(Text)
    duration_human = Column(Text)
    kb_source = Column(Text)
    llm_prompt = Column(Text)
    llm_response = Column(Text)
    is_third_party = Column(Boolean, default=False)

# class PageScanMetadata(Base):
#     """Stores detailed timing and metadata for each page scanned"""
#     _tablename_ = "page_scan_metadata"
    
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    
#     # Page details
#     url = Column(Text, nullable=False, index=True)
#     page_depth = Column(Integer, default=0)  # 0 = homepage, 1 = /about, etc.
    
#     # Timing
#     scan_start_timestamp = Column(Float, nullable=False)
#     scan_end_timestamp = Column(Float, nullable=False)
#     scan_duration_seconds = Column(Float, nullable=False)
    
#     # Cookie counts
#     cookies_before_scan = Column(Integer, default=0)
#     cookies_after_scan = Column(Integer, default=0)
#     new_cookies_found = Column(Integer, default=0)
    
#     # Status
#     page_status = Column(String(20), default='success')  # success, failed, timeout
#     status_code = Column(Integer, default=200)
#     error_message = Column(Text, nullable=True)
    
#     # Relationships
#     job = relationship("Job", back_populates="page_metadata")
    
#     created_at = Column(DateTime, default=datetime.utcnow)