KNOWN_COOKIE_PATTERNS_2 = {

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


    
    # ✅ TIER 1: Complete hardcoded dictionary of ALL common cookie patterns
KNOWN_COOKIE_PATTERNS = {
        
        # ========== GOOGLE ANALYTICS (GA4 & UNIVERSAL) ==========
        '_ga': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '2 years'},
        'ga': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '2 years'},  # GA4 property
        '_gid': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 day'},
        '_gat': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 minute'},
        'gat': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 minute'},
        '_gat_UA-': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': '1 minute'},
        '_gac': {'type': 'Advertising', 'provider': 'Google Ads', 'duration_human': '90 days'},
        'gac': {'type': 'Advertising', 'provider': 'Google Ads', 'duration_human': '90 days'},
        '__utma': {'type': 'Performance', 'provider': 'Google Analytics', 'duration_human': '2 years'},
        '__utmb': {'type': 'Performance', 'provider': 'Google Analytics', 'duration_human': '30 minutes'},
        '__utmc': {'type': 'Performance', 'provider': 'Google Analytics', 'duration_human': 'Session'},
        '__utmz': {'type': 'Performance', 'provider': 'Google Analytics', 'duration_human': '6 months'},
        '__utmt': {'type': 'Performance', 'provider': 'Google Analytics', 'duration_human': '10 minutes'},
        
        # ========== FACEBOOK PIXEL ==========
        '_fbp': {'type': 'Advertising', 'provider': 'Facebook', 'duration_human': '90 days'},
        'fr': {'type': 'Advertising', 'provider': 'Facebook', 'duration_human': '90 days'},
        'datr': {'type': 'Analytics', 'provider': 'Facebook', 'duration_human': '2 years'},
        'c_user': {'type': 'Analytics', 'provider': 'Facebook', 'duration_human': 'Session'},
        'xs': {'type': 'Analytics', 'provider': 'Facebook', 'duration_human': 'Session'},
        'sb': {'type': 'Necessary', 'provider': 'Facebook', 'duration_human': '2 years'},
        'spin': {'type': 'Necessary', 'provider': 'Facebook', 'duration_human': '24 hours'},
        'presence': {'type': 'Essential', 'provider': 'Facebook', 'duration_human': 'Session'},
        'wd': {'type': 'Necessary', 'provider': 'Facebook', 'duration_human': '7 days'},
        
        # ========== GOOGLE ADS / DOUBLECLICK ==========
        'IDE': {'type': 'Advertising', 'provider': 'Google DoubleClick', 'duration_human': '13 months'},
        'ANID': {'type': 'Advertising', 'provider': 'Google Ads', 'duration_human': '13 months'},
        'NID': {'type': 'Advertising', 'provider': 'Google', 'duration_human': '6 months'},
        'RUL': {'type': 'Advertising', 'provider': 'Google DoubleClick', 'duration_human': '1 year'},
        
        # ========== HUBSPOT ==========
        '__hstc': {'type': 'Analytics', 'provider': 'HubSpot', 'duration_human': '13 months'},
        '__hssc': {'type': 'Necessary', 'provider': 'HubSpot', 'duration_human': '30 minutes'},
        '__hssrc': {'type': 'Necessary', 'provider': 'HubSpot', 'duration_human': 'Session'},
        'hubspotutk': {'type': 'Analytics', 'provider': 'HubSpot', 'duration_human': '13 months'},
        
        # ========== LINKEDIN ==========
        'bcookie': {'type': 'Analytics', 'provider': 'LinkedIn', 'duration_human': '2 years'},
        'bscookie': {'type': 'Analytics', 'provider': 'LinkedIn', 'duration_human': '2 years'},
        'lidc': {'type': 'Essential', 'provider': 'LinkedIn', 'duration_human': '1 day'},
        'AnalyticsSyncHistory': {'type': 'Analytics', 'provider': 'LinkedIn', 'duration_human': '30 days'},
        'li_gc': {'type': 'Necessary', 'provider': 'LinkedIn', 'duration_human': '2 years'},
        'UserMatchHistory': {'type': 'Analytics', 'provider': 'LinkedIn', 'duration_human': '30 days'},
        
        # ========== TWITTER / X ==========
        'personalization_id': {'type': 'Analytics', 'provider': 'Twitter', 'duration_human': '2 years'},
        'guest_id': {'type': 'Analytics', 'provider': 'Twitter', 'duration_human': '2 years'},
        'external_referer': {'type': 'Analytics', 'provider': 'Twitter', 'duration_human': '1 week'},
        'muc_ads': {'type': 'Advertising', 'provider': 'Twitter', 'duration_human': '2 years'},
        
        # ========== MARKETING & TRACKING ==========
        '_utma': {'type': 'Analytics', 'provider': 'Universal Analytics', 'duration_human': '2 years'},
        '_utmb': {'type': 'Analytics', 'provider': 'Universal Analytics', 'duration_human': '30 minutes'},
        '_utmc': {'type': 'Analytics', 'provider': 'Universal Analytics', 'duration_human': 'Session'},
        '_utmz': {'type': 'Analytics', 'provider': 'Universal Analytics', 'duration_human': '6 months'},
        '_utmt': {'type': 'Analytics', 'provider': 'Universal Analytics', 'duration_human': '10 minutes'},
        'utm_source': {'type': 'Analytics', 'provider': 'Generic UTM', 'duration_human': 'Session'},
        'utm_medium': {'type': 'Analytics', 'provider': 'Generic UTM', 'duration_human': 'Session'},
        'utm_campaign': {'type': 'Analytics', 'provider': 'Generic UTM', 'duration_human': 'Session'},
        
        # ========== AMPLITUDE ==========
        'amplitude_id': {'type': 'Analytics', 'provider': 'Amplitude', 'duration_human': '10 years'},
        'amplitude_cookie': {'type': 'Analytics', 'provider': 'Amplitude', 'duration_human': '10 years'},
        'amplitude_user_id': {'type': 'Analytics', 'provider': 'Amplitude', 'duration_human': '10 years'},
        'AMP_TOKEN': {'type': 'Analytics', 'provider': 'Amplitude', 'duration_human': '1 year'},
        
        # ========== MIXPANEL ==========
        'mp_a': {'type': 'Analytics', 'provider': 'Mixpanel', 'duration_human': 'indefinite'},
        'mp_b': {'type': 'Analytics', 'provider': 'Mixpanel', 'duration_human': '5 years'},
        'mp_d': {'type': 'Analytics', 'provider': 'Mixpanel', 'duration_human': '5 years'},
        '__mpa': {'type': 'Analytics', 'provider': 'Mixpanel', 'duration_human': '2 years'},
        
        # ========== SEGMENT ==========
        'ajs_anonymous_id': {'type': 'Analytics', 'provider': 'Segment', 'duration_human': '1 year'},
        'ajs_user_id': {'type': 'Analytics', 'provider': 'Segment', 'duration_human': '1 year'},
        'ajs_group_id': {'type': 'Analytics', 'provider': 'Segment', 'duration_human': '1 year'},
        
        # ========== HOTJAR ==========
        '_hjid': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '1 year'},
        '_hjFirstSeen': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '1 year'},
        '_hjIncludedInSessionSample': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': 'Session'},
        '_hjRecordingEnabled': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': 'Session'},
        'hjSession': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '30 minutes'},
        'hjSessionUser': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': '1 year'},
        '_hjViewportId': {'type': 'Analytics', 'provider': 'Hotjar', 'duration_human': 'Session'},
        
        # ========== CRAZY EGG ==========
        '_ce_cpt': {'type': 'Analytics', 'provider': 'Crazy Egg', 'duration_human': 'Session'},
        '_ce_phc': {'type': 'Analytics', 'provider': 'Crazy Egg', 'duration_human': 'indefinite'},
        '_CEFT': {'type': 'Analytics', 'provider': 'Crazy Egg', 'duration_human': '13 months'},
        
        # ========== HEAP ==========
        'heap_id': {'type': 'Analytics', 'provider': 'Heap', 'duration_human': '1 year'},
        '_heapid': {'type': 'Analytics', 'provider': 'Heap', 'duration_human': '1 year'},
        
        # ========== MARKETO ==========
        '_mkto_trk': {'type': 'Marketing', 'provider': 'Marketo', 'duration_human': '2 years'},
        'mkt_tok': {'type': 'Marketing', 'provider': 'Marketo', 'duration_human': 'Session'},
        
        # ========== PARDOT / SALESFORCE ==========
        '_pardot': {'type': 'Marketing', 'provider': 'Pardot', 'duration_human': '1 year'},
        'visitor_id': {'type': 'Analytics', 'provider': 'Pardot', 'duration_human': '1 year'},
        
        # ========== GOOGLE OPTIMIZE ==========
        '_gaexp': {'type': 'Functional', 'provider': 'Google Optimize', 'duration_human': '90 days'},
        '_opt_utmc': {'type': 'Functional', 'provider': 'Google Optimize', 'duration_human': '90 days'},
        '_opt_awcid': {'type': 'Functional', 'provider': 'Google Optimize', 'duration_human': 'Session'},
        
        # ========== KISSMETRICS ==========
        'km_ai': {'type': 'Analytics', 'provider': 'KISSmetrics', 'duration_human': '1 year'},
        'km_ck': {'type': 'Analytics', 'provider': 'KISSmetrics', 'duration_human': '1 year'},
        'km_lk': {'type': 'Analytics', 'provider': 'KISSmetrics', 'duration_human': 'Session'},
        
        # ========== VIMEO ==========
        'player': {'type': 'Functional', 'provider': 'Vimeo', 'duration_human': '1 year'},
        'vimeo_wd': {'type': 'Essential', 'provider': 'Vimeo', 'duration_human': '1 year'},
        
        # ========== YOUTUBE ==========
        'VISITOR_INFO1_LIVE': {'type': 'Analytics', 'provider': 'YouTube', 'duration_human': '8 months'},
        'YSC': {'type': 'Analytics', 'provider': 'YouTube', 'duration_human': 'Session'},
        'LOGIN_INFO': {'type': 'Essential', 'provider': 'YouTube', 'duration_human': '2 years'},
        'PREF': {'type': 'Functional', 'provider': 'YouTube', 'duration_human': '8 months'},
        
        # ========== WORDPRESS ==========
        'wordpress_logged_in': {'type': 'Necessary', 'provider': 'WordPress', 'duration_human': '14 days'},
        'wordpress_': {'type': 'Necessary', 'provider': 'WordPress', 'duration_human': '14 days'},
        'wp-settings': {'type': 'Functional', 'provider': 'WordPress', 'duration_human': '1 year'},
        'wp-settings-time': {'type': 'Functional', 'provider': 'WordPress', 'duration_human': '1 year'},
        
        # ========== SHOPIFY ==========
        '_shopify_y': {'type': 'Essential', 'provider': 'Shopify', 'duration_human': 'Session'},
        '_shopify_tm': {'type': 'Essential', 'provider': 'Shopify', 'duration_human': 'Session'},
        '_shopid': {'type': 'Essential', 'provider': 'Shopify', 'duration_human': 'Session'},
        '_landing_page': {'type': 'Analytics', 'provider': 'Shopify', 'duration_human': 'Session'},
        
        # ========== STRIPE ==========
        'stripe_sid': {'type': 'Essential', 'provider': 'Stripe', 'duration_human': 'Session'},
        'm': {'type': 'Essential', 'provider': 'Stripe', 'duration_human': 'Session'},
        
        # ========== PAYPAL ==========
        'tsrce': {'type': 'Essential', 'provider': 'PayPal', 'duration_human': 'Session'},
        'cookie_check': {'type': 'Essential', 'provider': 'PayPal', 'duration_human': 'Session'},
        'nsid': {'type': 'Analytics', 'provider': 'PayPal', 'duration_human': '90 days'},
        
        # ========== AMAZON ASSOCIATES ==========
        'rms_src': {'type': 'Advertising', 'provider': 'Amazon', 'duration_human': '1 year'},
        'session-id': {'type': 'Essential', 'provider': 'Amazon', 'duration_human': '1 year'},
        'session-id-time': {'type': 'Essential', 'provider': 'Amazon', 'duration_human': '1 year'},
        
        # ========== CLOUDFLARE ==========
        'cf_clearance': {'type': 'Essential', 'provider': 'Cloudflare', 'duration_human': 'Session'},
        '__cfruid': {'type': 'Essential', 'provider': 'Cloudflare', 'duration_human': 'Session'},
        '__cfduid': {'type': 'Essential', 'provider': 'Cloudflare', 'duration_human': '1 month'},
        
        # ========== ADDTHIS ==========
        'di': {'type': 'Analytics', 'provider': 'AddThis', 'duration_human': '13 months'},
        'dt': {'type': 'Analytics', 'provider': 'AddThis', 'duration_human': 'Session'},
        '__atuvc': {'type': 'Analytics', 'provider': 'AddThis', 'duration_human': '13 months'},
        '__atuvs': {'type': 'Analytics', 'provider': 'AddThis', 'duration_human': 'Session'},
        
        # ========== PINTEREST ==========
        '_pinterest_sess': {'type': 'Essential', 'provider': 'Pinterest', 'duration_human': 'Session'},
        '_pinterest_ct_ua': {'type': 'Analytics', 'provider': 'Pinterest', 'duration_human': '1 year'},
        'e': {'type': 'Analytics', 'provider': 'Pinterest', 'duration_human': '1 year'},
        
        # ========== REDDIT ==========
        'reddit_session': {'type': 'Essential', 'provider': 'Reddit', 'duration_human': 'Session'},
        'csv': {'type': 'Analytics', 'provider': 'Reddit', 'duration_human': 'Session'},
        
        # ========== DISQUS ==========
        '__jid': {'type': 'Essential', 'provider': 'Disqus', 'duration_human': 'Session'},
        'XSRF-TOKEN': {'type': 'Necessary', 'provider': 'Disqus', 'duration_human': 'Session'},
        
        # ========== RECAPTCHA ==========
        '_GRECAPTCHA': {'type': 'Necessary', 'provider': 'Google reCAPTCHA', 'duration_human': '6 months'},
        'rc::a': {'type': 'Necessary', 'provider': 'Google reCAPTCHA', 'duration_human': '6 months'},
        'rc::b': {'type': 'Necessary', 'provider': 'Google reCAPTCHA', 'duration_human': 'Session'},
        'rc::c': {'type': 'Necessary', 'provider': 'Google reCAPTCHA', 'duration_human': 'Session'},
        
        # ========== AUTH0 ==========
        'auth0': {'type': 'Essential', 'provider': 'Auth0', 'duration_human': '1 month'},
        'auth0.is.authenticated': {'type': 'Essential', 'provider': 'Auth0', 'duration_human': '1 month'},
        
        # ========== OKTA ==========
        'okta': {'type': 'Essential', 'provider': 'Okta', 'duration_human': '1 month'},
        'okta-core': {'type': 'Essential', 'provider': 'Okta', 'duration_human': '1 month'},
        
        # ========== SESSION & AUTH ==========
        'PHPSESSID': {'type': 'Essential', 'provider': 'PHP', 'duration_human': 'Session'},
        'JSESSIONID': {'type': 'Essential', 'provider': 'Java', 'duration_human': 'Session'},
        'ASPSESSIONID': {'type': 'Essential', 'provider': 'ASP.NET', 'duration_human': 'Session'},
        'sessionid': {'type': 'Essential', 'provider': 'Generic', 'duration_human': 'Session'},
        'session_id': {'type': 'Essential', 'provider': 'Generic', 'duration_human': 'Session'},
        '_session': {'type': 'Essential', 'provider': 'Generic', 'duration_human': 'Session'},
        '__Host-session': {'type': 'Essential', 'provider': 'Generic', 'duration_human': 'Session'},
        
        # ========== CSRF PROTECTION ==========
        'csrf': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': 'Session'},
        'csrf_token': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': 'Session'},
        '_csrf': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': 'Session'},
        'XSRF-TOKEN': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': 'Session'},
        
        # ========== CONSENT & PREFERENCES ==========
        'CookieConsent': {'type': 'Necessary', 'provider': 'CookieConsent', 'duration_human': '1 year'},
        'cookieconsent_status': {'type': 'Necessary', 'provider': 'Cookie Consent', 'duration_human': '1 year'},
        'OptanonConsent': {'type': 'Necessary', 'provider': 'OneTrust', 'duration_human': '1 year'},
        'OptanonAlertBoxClosed': {'type': 'Necessary', 'provider': 'OneTrust', 'duration_human': '1 year'},
        'CybotCookiebotConsent': {'type': 'Necessary', 'provider': 'Cookiebot', 'duration_human': '1 year'},
        'euconsent': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': '1 year'},
        'euconsent-v2': {'type': 'Necessary', 'provider': 'Generic', 'duration_human': '1 year'},
        'TCString': {'type': 'Necessary', 'provider': 'TCF', 'duration_human': '1 year'},
        'addtl_consent': {'type': 'Necessary', 'provider': 'Google GMP', 'duration_human': '1 year'},
        
        # ========== LANGUAGE & LOCALIZATION ==========
        'lang': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'language': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'locale': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'hl': {'type': 'Functional', 'provider': 'Google', 'duration_human': '1 year'},
        'gl': {'type': 'Functional', 'provider': 'Google', 'duration_human': '1 year'},
        
        # ========== USER PREFERENCES ==========
        'theme': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'dark_mode': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'preferences': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        'user_preferences': {'type': 'Functional', 'provider': 'Generic', 'duration_human': '1 year'},
        
        # ========== TRACKING PIXELS & BEACONS ==========
        'IDE': {'type': 'Advertising', 'provider': 'Google', 'duration_human': '13 months'},
        'ANID': {'type': 'Advertising', 'provider': 'Google', 'duration_human': '13 months'},
        'NID': {'type': 'Advertising', 'provider': 'Google', 'duration_human': '6 months'},
        'dc_gtm': {'type': 'Analytics', 'provider': 'Google Tag Manager', 'duration_human': 'Session'},
        '_ga_gtag_event': {'type': 'Analytics', 'provider': 'Google Analytics', 'duration_human': 'Session'},
        
        # ========== E-COMMERCE ==========
        'cart': {'type': 'Essential', 'provider': 'Generic', 'duration_human': '30 days'},
        'cart_id': {'type': 'Essential', 'provider': 'Generic', 'duration_human': '30 days'},
        'checkout': {'type': 'Essential', 'provider': 'Generic', 'duration_human': '30 days'},
        'user_id': {'type': 'Essential', 'provider': 'Generic', 'duration_human': '1 year'},
        'customer_id': {'type': 'Essential', 'provider': 'Generic', 'duration_human': '1 year'},
    }