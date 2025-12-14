"""SVG mockup generator for slide cards"""

def generate_slide_mockup(card_title: str, color_key: str) -> str:
    """Generate SVG mockup for slide card"""
    card_title_lower = card_title.lower()
    
    if 'data card' in card_title_lower or 'data cards' in card_title_lower:
        # Simple data card mockup - rectangles with numbers
        return """<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="60" height="40" rx="4" fill="#E5E5EA" stroke="#C7C7CC" stroke-width="1"/>
            <text x="50" y="42" font-family="-apple-system" font-size="12" font-weight="600" fill="#1D1D1F" text-anchor="middle">1,234</text>
            <text x="50" y="55" font-family="-apple-system" font-size="9" fill="#8E8E93" text-anchor="middle">Users</text>
            
            <rect x="90" y="20" width="60" height="40" rx="4" fill="#E5E5EA" stroke="#C7C7CC" stroke-width="1"/>
            <text x="120" y="42" font-family="-apple-system" font-size="12" font-weight="600" fill="#1D1D1F" text-anchor="middle">567</text>
            <text x="120" y="55" font-family="-apple-system" font-size="9" fill="#8E8E93" text-anchor="middle">Orders</text>
            
            <rect x="160" y="20" width="60" height="40" rx="4" fill="#E5E5EA" stroke="#C7C7CC" stroke-width="1"/>
            <text x="190" y="42" font-family="-apple-system" font-size="12" font-weight="600" fill="#1D1D1F" text-anchor="middle">89%</text>
            <text x="190" y="55" font-family="-apple-system" font-size="9" fill="#8E8E93" text-anchor="middle">Growth</text>
        </svg>"""
    
    elif 'infographic' in card_title_lower or 'infographics' in card_title_lower:
        # Rich infographic mockup - charts and visualizations
        return """<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="100" rx="6" fill="#FFFFFF" stroke="#E5E5EA" stroke-width="1"/>
            
            <!-- Bar chart -->
            <rect x="30" y="80" width="20" height="30" rx="2" fill="#007AFF"/>
            <rect x="55" y="70" width="20" height="40" rx="2" fill="#007AFF"/>
            <rect x="80" y="60" width="20" height="50" rx="2" fill="#007AFF"/>
            <rect x="105" y="50" width="20" height="60" rx="2" fill="#007AFF"/>
            <rect x="130" y="55" width="20" height="55" rx="2" fill="#007AFF"/>
            
            <!-- Trend line -->
            <path d="M 30 90 L 50 85 L 70 75 L 90 65 L 110 55 L 130 60" stroke="#34C759" stroke-width="2" fill="none"/>
            <circle cx="30" cy="90" r="3" fill="#34C759"/>
            <circle cx="50" cy="85" r="3" fill="#34C759"/>
            <circle cx="70" cy="75" r="3" fill="#34C759"/>
            <circle cx="90" cy="65" r="3" fill="#34C759"/>
            <circle cx="110" cy="55" r="3" fill="#34C759"/>
            <circle cx="130" cy="60" r="3" fill="#34C759"/>
            
            <!-- Icon -->
            <circle cx="190" cy="50" r="15" fill="#FF9500" opacity="0.2"/>
            <text x="190" y="55" font-family="-apple-system" font-size="16" fill="#FF9500" text-anchor="middle">↑</text>
        </svg>"""
    
    elif 'story' in card_title_lower or 'story-driven' in card_title_lower:
        # Story-driven slide mockup - dynamic, AI-generated look
        return """<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="100" rx="6" fill="#FFFFFF" stroke="#AF52DE" stroke-width="2"/>
            
            <!-- Story elements -->
            <rect x="30" y="30" width="60" height="8" rx="4" fill="#AF52DE" opacity="0.3"/>
            <rect x="30" y="45" width="80" height="6" rx="3" fill="#E5E5EA"/>
            <rect x="30" y="55" width="70" height="6" rx="3" fill="#E5E5EA"/>
            
            <!-- Visual element -->
            <circle cx="160" cy="50" r="20" fill="#AF52DE" opacity="0.2"/>
            <path d="M 150 50 L 160 45 L 170 50 L 160 55 Z" fill="#AF52DE"/>
            
            <!-- Data visualization -->
            <rect x="30" y="75" width="180" height="30" rx="4" fill="#F9F0FF"/>
            <rect x="35" y="85" width="30" height="15" rx="2" fill="#AF52DE" opacity="0.6"/>
            <rect x="70" y="80" width="30" height="20" rx="2" fill="#AF52DE" opacity="0.6"/>
            <rect x="105" y="90" width="30" height="10" rx="2" fill="#AF52DE" opacity="0.6"/>
            <rect x="140" y="75" width="30" height="25" rx="2" fill="#AF52DE" opacity="0.6"/>
            
            <!-- AI sparkle -->
            <circle cx="200" cy="35" r="2" fill="#AF52DE"/>
            <circle cx="210" cy="30" r="1.5" fill="#AF52DE" opacity="0.7"/>
            <circle cx="205" cy="40" r="1.5" fill="#AF52DE" opacity="0.7"/>
        </svg>"""
    
    else:
        # Default simple mockup
        return """<svg viewBox="0 0 240 140" xmlns="http://www.w3.org/2000/svg">
            <rect x="20" y="20" width="200" height="100" rx="6" fill="#F5F5F7" stroke="#E5E5EA" stroke-width="1"/>
            <rect x="30" y="30" width="60" height="8" rx="4" fill="#C7C7CC"/>
            <rect x="30" y="45" width="80" height="6" rx="3" fill="#E5E5EA"/>
            <rect x="30" y="55" width="70" height="6" rx="3" fill="#E5E5EA"/>
        </svg>"""
