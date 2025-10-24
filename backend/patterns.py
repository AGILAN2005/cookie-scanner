KNOWN_COOKIE_PATTERNS = {

        '_ga': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '2 years'},
        '_gid': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 day'},
        '_gat': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 minute'},
        # '_ga_*': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '2 years'},
        # '_gat_UA-*': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 minute'},
        
        # Legacy Google Analytics
        '__utma': {'type': 'Analytics', 'provider': 'Google Analytics (Legacy)', 'duration_human': '2 years'},
        '__utmb': {'type': 'Analytics', 'provider': 'Google Analytics (Legacy)', 'duration_human': '30 minutes'},
        '__utmc': {'type': 'Analytics', 'provider': 'Google Analytics (Legacy)', 'duration_human': 'Session'},
        '__utmz': {'type': 'Analytics', 'provider': 'Google Analytics (Legacy)', 'duration_human': '6 months'},

        # Google Ads & DoubleClick
        'IDE': {'type': 'Advertising', 'provider': 'DoubleClick (Google)', 'duration_human': '13 months'},
        'test_cookie': {'type': 'Advertising', 'provider': 'DoubleClick (Google)', 'duration_human': '15 minutes'},
        'NID': {'type': 'Advertising', 'provider': 'Google', 'duration_human': '6 months'},
        'CONSENT': {'type': 'Necessary', 'provider': 'Google', 'duration_human': '2 years'},

        # HubSpot
        '__hstc': {'type': 'Analytics', 'provider': 'HubSpot', 'duration_human': '6 months'},
        '__hssc': {'type': 'Analytics', 'provider': 'HubSpot', 'duration_human': '30 minutes'},
        'hubspotutk': {'type': 'Analytics', 'provider': 'HubSpot', 'duration_human': '6 months'},
        'messagesUtk': {'type': 'Functional', 'provider': 'HubSpot Chat', 'duration_human': '6 months'},

        # Cloudflare
        '__cf_bm': {'type': 'Essential', 'provider': 'Cloudflare', 'duration_human': '30 minutes'},
        '_cfuvid': {'type': 'Essential', 'provider': 'Cloudflare', 'duration_human': 'Session'},

        # Facebook/Meta
        '_fbp': {'type': 'Advertising', 'provider': 'Facebook Pixel', 'duration_human': '3 months'},
        'fr': {'type': 'Advertising', 'provider': 'Facebook', 'duration_human': '3 months'},

        # YouTube
        'YSC': {'type': 'Functional', 'provider': 'YouTube', 'duration_human': 'Session'},
        'VISITOR_INFO1_LIVE': {'type': 'Functional', 'provider': 'YouTube', 'duration_human': '6 months'},

        # LinkedIn
        'li_gc': {'type': 'Functional', 'provider': 'LinkedIn', 'duration_human': '6 months'},
        'AnalyticsSyncHistory': {'type': 'Analytics', 'provider': 'LinkedIn', 'duration_human': '1 month'},
        'UserMatchHistory': {'type': 'Advertising', 'provider': 'LinkedIn', 'duration_human': '1 month'},

        # Hotjar
        '_hjid': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '1 year'},
        '_hjFirstSeen': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '30 minutes'},

        # Common Session Cookies
        'PHPSESSID': {'type': 'Essential', 'provider': 'PHP', 'duration_human': 'Session'},
        'JSESSIONID': {'type': 'Essential', 'provider': 'Java Application Server', 'duration_human': 'Session'},
        'ASP.NET_SessionId': {'type': 'Essential', 'provider': 'ASP.NET', 'duration_human': 'Session'},
    }
