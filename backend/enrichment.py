#enrichment.py - Advanced cookie enrichment module with tiered knowledge base and AI integration
import re
import json
import time
import logging
from typing import Optional, Dict, List
import google.generativeai as genai
import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
# import threading
import fcntl
import errno
from patterns import KNOWN_COOKIE_PATTERNS
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorldClassCookieKnowledgeBase:
    """Manages an extensive, tiered knowledge base of cookies."""
    COOKIE_DB = {}
    _json_path = None 
    # _lock = threading.Lock() 

    @classmethod
    def load_from_json(cls, json_path: str):
        """Load an external cookie database from a JSON file."""
        if json_path and isinstance(json_path, str):
            cls._json_path = json_path
        else:
            logger.warning("⚠️ Invalid JSON path provided for cookie database.")
            cls._json_path = None
            return
        cls.KNOWN_COOKIE_PATTERNS = KNOWN_COOKIE_PATTERNS
        possible_paths = [Path(json_path), Path.cwd() / json_path]
        for path in possible_paths:
            if path.exists():
                try:
                    if not cls._json_path:
                        logger.error(f"❌ Cannot load from {path}, _json_path is not set.")
                        continue
                    with open(path, 'r', encoding='utf-8') as f:
                        cls.COOKIE_DB = json.load(f)
                    logger.info(f"✅ Loaded {len(cls.COOKIE_DB)} cookies from external database: {path}")
                    return
                except Exception as e:
                    logger.error(f"❌ Error reading cookie database {path}: {e}")
        # Only log if _json_path was valid but file wasn't found/readable
        if cls._json_path:
            logger.info(f"ℹ️ External cookie database '{cls._json_path}' not found or unreadable. Using built-in KB only.")
        else:
            logger.warning("⚠️ No valid JSON path set, cannot load external DB. Using built-in KB only.")
        # for path in possible_paths:
        #     if path.exists():
        #         try:
        #             with cls._lock:    
        #                 with open(path, 'r', encoding='utf-8') as f:
        #                     cls.COOKIE_DB = json.load(f)
        #             logger.info(f"✅ Loaded {len(cls.COOKIE_DB)} cookies from external database: {path}")
        #             return
        #         except Exception as e:
        #             logger.error(f"❌ Error reading cookie database {path}: {e}")
        # logger.info("ℹ️ External cookie database not found. Using built-in knowledge base only.")

    @classmethod
    def get_cookie_info(cls, normalized_name: str) -> Optional[Dict]:
        """Get cookie info by checking the external DB first, then the built-in patterns."""
        if normalized_name in cls.COOKIE_DB:
            return cls.COOKIE_DB[normalized_name]
        
        for pattern, info in cls.KNOWN_COOKIE_PATTERNS.items():
            if pattern.endswith('*') and normalized_name.startswith(pattern[:-1]):
                return info
            elif normalized_name == pattern:
                return info
        return None
    @classmethod
    def add_cookie_info(cls, normalized_name: str, info: Dict):
        """Adds a new cookie to the in-memory knowledge base.""" 
        # Don't add if it's already in the hardcoded patterns
        is_in_static = False
        for pattern in cls.KNOWN_COOKIE_PATTERNS:
             if pattern.endswith('*') and normalized_name.startswith(pattern[:-1]):
                 is_in_static = True
                 break
             elif normalized_name == pattern:
                 is_in_static = True
                 break
        if not is_in_static and normalized_name not in cls.COOKIE_DB:
            # Only log if it's a high-confidence AI source
            if info.get('kb_source') == 'AI Enrichment':
                logger.info(f"🧠 Learning new cookie via AI: {normalized_name}")
            
            # Save the core details
            cls.COOKIE_DB[normalized_name] = {
                "type": info.get('type', 'Uncategorized'),
                "provider": info.get('provider', 'Unknown'),
                "duration_human": info.get('duration_human', 'Session'),
                "description": info.get('description', 'No description available.')
            }

    # @classmethod
    # def save_to_json(cls):
    #     """Saves the in-memory DB back to the JSON file, thread-safe."""
    #     if not cls._json_path:
    #         logger.warning("⚠️ Cannot save Knowledge Base: JSON path not set.")
    #         return
        
    #     path = Path(cls._json_path)
    #     if not path.is_absolute():
    #         path = Path.cwd() / cls._json_path

    #     with cls._lock:
    #         try:
    #             logger.info(f"💾 Saving {len(cls.COOKIE_DB)} cookies to Knowledge Base: {path}")
    #             # Sort keys for a clean, consistent file
    #             sorted_db = dict(sorted(cls.COOKIE_DB.items()))
    #             with open(path, 'w', encoding='utf-8') as f:
    #                 json.dump(sorted_db, f, indent=4)
    #             logger.info("✅ Knowledge Base saved successfully.")
    #         except Exception as e:
    #             logger.error(f"❌ Failed to save Knowledge Base: {e}")

    @classmethod
    def save_to_json(cls):
        """Saves the in-memory DB back to the JSON file, process-safe using fcntl."""
        if not cls._json_path:
            # Log the warning from add_cookie_info if path wasn't set during load
            if not hasattr(cls, '_path_warning_logged'):
                 logger.warning("⚠️ Cannot save Knowledge Base: JSON path not set during initialization.")
                 cls._path_warning_logged = True # Log only once
            return

        # Resolve the path relative to CWD if necessary
        path = Path(cls._json_path)
        if not path.is_absolute():
            # Use Path.resolve() for robustness
            try:
                path = (Path.cwd() / cls._json_path).resolve()
            except Exception as e:
                 logger.error(f"❌ Error resolving path '{cls._json_path}': {e}. Cannot save KB.")
                 return


        # Ensure parent directory exists
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"❌ Could not create directory for KB file '{path}': {e}. Cannot save KB.")
            return

        # Process-safe file writing with exclusive lock
        try:
            # Open file first, creates/truncates it
            with open(path, 'w', encoding='utf-8') as f:
                fd = f.fileno()
                locked = False
                try:
                    # Attempt to acquire exclusive, non-blocking lock
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    logger.info(f"💾 Saving {len(cls.COOKIE_DB)} cookies to Knowledge Base: {path}")
                    # Sort keys for a clean, consistent file
                    sorted_db = dict(sorted(cls.COOKIE_DB.items()))
                    json.dump(sorted_db, f, indent=4)
                    # Ensure data is written before releasing lock
                    f.flush()
                    os.fsync(fd)
                    logger.info("✅ Knowledge Base saved successfully.")
                except BlockingIOError:
                     # Another process holds the lock
                     logger.warning(f"🔒 Knowledge Base file '{path}' is locked by another process. Skipping save.")
                except (IOError, OSError) as e:
                     logger.error(f"❌ File lock/write error saving Knowledge Base to '{path}': {e}")
                finally:
                    # Always release the lock if acquired
                    if locked:
                        try:
                             fcntl.flock(fd, fcntl.LOCK_UN)
                        except Exception as unlock_e:
                             logger.error(f"❌ Error releasing lock on '{path}': {unlock_e}")

        except (IOError, OSError, PermissionError) as e:
            logger.error(f"❌ Failed to open/write Knowledge Base file '{path}': {e}")
        except Exception as e:
            # Catch unexpected errors during the process
            logger.error(f"❌ Unexpected error saving Knowledge Base to '{path}': {e}")

class WorldClassCookieEnricher:
    """Implements the Tiered, Knowledge-First Enrichment Strategy."""
    
    VALID_CATEGORIES = ["Essential", "Analytics", "Advertising", "Functional", "Performance", "Security", "Uncategorized"]

    def __init__(self, google_api_key: str, cookie_db_path: str):
        if google_api_key:
            try:
                genai.configure(api_key=google_api_key)
                model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
                self.model = genai.GenerativeModel(model_name)
                logger.info(f"✅ AI model '{model_name}' initialized.")
            except Exception as e:
                self.model = None
                logger.warning(f"⚠️ AI model initialization failed: {e}")
        else:
            logger.warning(f"⚠️ AI model initialization failed: No API key provided.")
            self.model = None
        
        WorldClassCookieKnowledgeBase.load_from_json(cookie_db_path)

    def _normalize_cookie_name(self, name: str) -> str:
        """Normalize dynamic cookie names to match known patterns."""
        # if name.startswith('_ga_'): 
        #     return '_ga_*'
        # if name.startswith('_gat_UA-'): 
        #     return '_gat_UA-*'
        # if name.startswith('wordpress_logged_in_'):
        #     return 'wordpress_logged_in_*'
        return name

    def _get_base_domain(self, domain: str) -> str:
        parts = domain.lstrip('.').split('.')
        return '.'.join(parts[-2:]) if len(parts) >= 2 else domain

    def _duration_to_iso(self, duration_human: str) -> str:
        """Robustly convert human-readable duration to ISO 8601 format."""
        if not duration_human: 
            return 'PT0S'
        duration_lower = duration_human.lower()
        if 'session' in duration_lower: 
            return 'PT0S'
        
        value = int(re.search(r'(\d+)', duration_lower).group(1)) if re.search(r'(\d+)', duration_lower) else 1
        
        if 'minute' in duration_lower: 
            return f"PT{value}M"
        if 'hour' in duration_lower: 
            return f"PT{value}H"
        if 'day' in duration_lower: 
            return f"P{value}D"
        if 'month' in duration_lower: 
            return f"P{value}M"
        if 'year' in duration_lower: 
            return f"P{value}Y"
        return 'PT0S'

    def _classify_by_heuristics(self, cookie: Dict) -> Dict:
        """Smarter heuristic fallback using domain and name clues."""
        name = cookie.get('name', '').lower()
        domain = cookie.get('domain', '').lower()

        # High-confidence domain rules
        if any(d in domain for d in ['google-analytics.com', 'googletagmanager.com']): 
            return {'type': 'Analytics', 'confidence': 0.8}
        if any(d in domain for d in ['doubleclick.net', 'ads.google.com']): 
            return {'type': 'Advertising', 'confidence': 0.8}
        if 'cloudflare' in domain: 
            return {'type': 'Essential', 'confidence': 0.85}
        if 'facebook' in domain or 'fb' in domain: 
            return {'type': 'Advertising', 'confidence': 0.8}

        # Medium-confidence name rules
        if any(k in name for k in ['_ga', '_gid', '_utm', 'analytics']): 
            return {'type': 'Analytics', 'confidence': 0.6}
        if any(k in name for k in ['ad', 'targeting', 'pixel', '_fbp']): 
            return {'type': 'Advertising', 'confidence': 0.6}
        if any(k in name for k in ['session', 'auth', 'token', 'csrf', 'jwt']): 
            return {'type': 'Essential', 'confidence': 0.7}
        
        # Low-confidence fallback
        return {'type': 'Uncategorized', 'confidence': 0.2}

    # async def _enrich_from_ai_with_retries(self, cookie_data: Dict, max_retries: int = 2) -> Optional[Dict]:
    #     """Upgraded AI prompt with self-correction loop."""
    #     if not self.model: 
    #         return None
        
    #     prompt = f"""
    #     Analyze this cookie and respond ONLY in valid JSON.

    #     Cookie to Analyze:
    #     - Name: "{cookie_data['name']}"
    #     - Domain: "{cookie_data['domain']}"

    #     Required JSON Schema:
    #     {{
    #       "description": "A single-paragraph explanation of the cookie's purpose.",
    #       "category": "Choose ONE from this strict list: {self.VALID_CATEGORIES}",
    #       "duration_human": "A simple duration like '2 years', '30 days', or 'Session'.",
    #       "provider": "The company that sets the cookie (e.g., 'Google Analytics')."
    #     }}
    #     """
    #     for attempt in range(max_retries):
    #         try:
    #             response = await self.model.generate_content_async(prompt)
    #             response_text = response.text.strip().replace('```json', '').replace('```', '').strip()
    #             parsed = json.loads(response_text)

    #             if parsed.get('category') in self.VALID_CATEGORIES and 'description' in parsed:
    #                 return {
    #                     'description': parsed['description'],
    #                     'type': parsed['category'],
    #                     'duration_human': parsed.get('duration_human', 'Session'),
    #                     'provider': parsed.get('provider', self._get_base_domain(cookie_data['domain']).title()),
    #                     'confidence': 0.75,
    #                     'kb_source': 'AI Enrichment',
    #                     'duration_iso': self._duration_to_iso(parsed.get('duration_human', 'Session'))
    #                 }
    #             else:
    #                 prompt += "\n\nYour previous response was invalid. The 'category' must be one of the provided options. Adhere strictly to the JSON schema."
    #                 logger.warning(f"Invalid AI response for '{cookie_data['name']}'. Retrying...")
    #         except Exception as e:
    #             logger.error(f"AI enrichment attempt {attempt + 1} failed for '{cookie_data['name']}': {e}")
    #             await asyncio.sleep(1)
    #     return None
    async def _enrich_from_ai_with_retries(self, cookie_data: Dict, site_context_domain: str, max_retries: int = 2) -> Optional[Dict]:
        """Upgraded AI prompt with self-correction loop and site context."""
        if not self.model: 
            return None
        
        # --- NEW: Add context to the prompt ---
        prompt = f"""
        Analyze this cookie and respond ONLY in valid JSON.

        Context:
        - This cookie was found on a website: "{site_context_domain}"
        - Use this context to make a better guess if the cookie's purpose is unclear.

        Cookie to Analyze:
        - Name: "{cookie_data['name']}"
        - Domain: "{cookie_data['domain']}"

        Required JSON Schema:
        {{
          "description": "A single-paragraph explanation of the cookie's purpose.",
          "category": "Choose ONE from this strict list: {self.VALID_CATEGORIES}",
          "duration_human": "A simple duration like '2 years', '30 days', or 'Session'.",
          "provider": "The company that sets the cookie (e.g., 'Google Analytics' or '{site_context_domain}')."
        }}
        """
        for attempt in range(max_retries):
            try:
                response = await self.model.generate_content_async(prompt)
                response_text = response.text.strip().replace('```json', '').replace('```', '').strip()
                parsed = json.loads(response_text)

                if parsed.get('category') in self.VALID_CATEGORIES and 'description' in parsed:
                    # Determine provider: if provider is the same as site, use the site domain
                    provider = parsed.get('provider', self._get_base_domain(cookie_data['domain']).title())
                    if provider.lower() == site_context_domain:
                         provider = site_context_domain.title()
                         
                    return {
                        'description': parsed['description'],
                        'type': parsed['category'],
                        'duration_human': parsed.get('duration_human', 'Session'),
                        'provider': provider,
                        'confidence': 0.75,
                        'kb_source': 'AI Enrichment',
                        'duration_iso': self._duration_to_iso(parsed.get('duration_human', 'Session'))
                    }
                else:
                    prompt += "\n\nYour previous response was invalid. The 'category' must be one of the provided options. Adhere strictly to the JSON schema."
                    logger.warning(f"Invalid AI response for '{cookie_data['name']}'. Retrying...")
            except Exception as e:
                logger.error(f"AI enrichment attempt {attempt + 1} failed for '{cookie_data['name']}': {e}")
                await asyncio.sleep(1)
        return None
    
    # async def enrich_cookie(self, cookie: Dict, visited_url: str, cache: dict) -> Dict:
    #     """Main tiered enrichment pipeline: Knowledge Base -> AI -> Heuristics."""
    #     normalized_name = self._normalize_cookie_name(cookie['name'])
        
    #     if normalized_name in cache:
    #         return cache[normalized_name]

    #     base_domain = self._get_base_domain(cookie.get('domain', visited_url))
    #     is_third_party = base_domain != self._get_base_domain(visited_url)
        
    #     # --- Tier 1: Check the Knowledge Base (Highest Accuracy) ---
    #     kb_info = WorldClassCookieKnowledgeBase.get_cookie_info(normalized_name)
    #     if kb_info:
    #         result = {
    #             'cookie': normalized_name, 'domain': base_domain, 'is_third_party': is_third_party,
    #             'description': kb_info.get('description', f"This is a {kb_info.get('type', 'Functional')} cookie set by {kb_info.get('provider', 'this site')}. A detailed description is not yet available in our database."),
    #             'type': kb_info.get('type', 'Other'),
    #             'duration_human': kb_info.get('duration_human', 'Session'),
    #             'duration_iso': self._duration_to_iso(kb_info.get('duration_human', 'Session')),
    #             'provider': kb_info.get('provider', base_domain.title()),
    #             'confidence': 0.99, 'kb_source': 'Knowledge Base',
    #         }
    #         cache[normalized_name] = result
    #         return result
        
    #     # --- Tier 2: Use Upgraded AI with Self-Correction ---
    #     ai_result = await self._enrich_from_ai_with_retries({'name': cookie['name'], 'domain': base_domain})
    #     if ai_result:
    #         result = {'cookie': normalized_name, 'domain': base_domain, 'is_third_party': is_third_party, **ai_result}
    #         cache[normalized_name] = result
    #         return result
    async def enrich_cookie(self, cookie: Dict, visited_url: str, cache: dict) -> Dict:
        """Main tiered enrichment pipeline: Knowledge Base -> AI -> Heuristics."""
        normalized_name = self._normalize_cookie_name(cookie['name'])
        
        if normalized_name in cache:
            return cache[normalized_name]

        base_domain = self._get_base_domain(cookie.get('domain', visited_url))
        site_base_domain = self._get_base_domain(visited_url) # Get the site's main domain
        is_third_party = base_domain != site_base_domain
        
        # --- Tier 1: Check the Knowledge Base (Highest Accuracy) ---
        kb_info = WorldClassCookieKnowledgeBase.get_cookie_info(normalized_name)
        if kb_info:
            result = {
                'cookie': normalized_name, 'domain': base_domain, 'is_third_party': is_third_party,
                'description': kb_info.get('description', f"This is a {kb_info.get('type', 'Functional')} cookie set by {kb_info.get('provider', 'this site')}. A detailed description is not yet available in our database."),
                'type': kb_info.get('type', 'Other'),
                'duration_human': kb_info.get('duration_human', 'Session'),
                'duration_iso': self._duration_to_iso(kb_info.get('duration_human', 'Session')),
                'provider': kb_info.get('provider', base_domain.title()),
                'confidence': 0.99, 'kb_source': 'Knowledge Base',
            }
            cache[normalized_name] = result
            return result
        # --- Tier 2: Use Upgraded AI with Self-Correction and Site Context ---
        ai_result = await self._enrich_from_ai_with_retries(
            {'name': cookie['name'], 'domain': base_domain}, 
            site_base_domain 
        )
        if ai_result:
            result = {'cookie': normalized_name, 'domain': base_domain, 'is_third_party': is_third_party, **ai_result}
            WorldClassCookieKnowledgeBase.add_cookie_info(normalized_name, result)
            cache[normalized_name] = result
            return result

        # --- Tier 3: Use Smarter Heuristic Fallback (Lowest Accuracy) ---
        heuristic_result = self._classify_by_heuristics(cookie)
        result = {
            'cookie': normalized_name, 'domain': base_domain, 'is_third_party': is_third_party,
            'description': "This cookie could not be automatically categorized and requires manual review for a precise description of its purpose.",
            'duration_human': 'Session', 'duration_iso': 'PT0S',
            'provider': base_domain.title(),
            'type': heuristic_result['type'], 'confidence': heuristic_result['confidence'], 'kb_source': 'Heuristic Fallback',
        }
        WorldClassCookieKnowledgeBase.add_cookie_info(normalized_name, result)
        cache[normalized_name] = result
        return result