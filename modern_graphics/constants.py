"""Constants for Modern Graphics Generator"""

MODERN_COLORS = {
    "blue": {"gradient": ("#EBF5FF", "#E3F2FD"), "shadow": "rgba(0, 122, 255, 0.12)"},
    "green": {"gradient": ("#F0F9F4", "#E8F5E9"), "shadow": "rgba(52, 199, 89, 0.12)"},
    "orange": {"gradient": ("#FFF8F0", "#FFF3E0"), "shadow": "rgba(255, 149, 0, 0.12)"},
    "purple": {"gradient": ("#F9F0FF", "#F3E5F5"), "shadow": "rgba(175, 82, 222, 0.12)"},
    "red": {"gradient": ("#FFF0F0", "#FFE5E5"), "shadow": "rgba(255, 59, 48, 0.12)"},
    "gray": {"gradient": ("#F5F5F7", "#F5F5F7"), "shadow": "rgba(0, 0, 0, 0.08)"},
}

# Alias for backward compatibility during migration
APPLE_COLORS = MODERN_COLORS

BASE_STYLES = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #FFFFFF;
            padding: 60px 40px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        @media (max-width: 768px) {
            body {
                padding: 40px 20px;
            }
        }
        
        @media (max-width: 480px) {
            body {
                padding: 24px 16px;
            }
        }
    """

ATTRIBUTION_STYLES = """
        .attribution {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            font-weight: 500;
            color: #8E8E93;
            letter-spacing: 0.02em;
            text-align: right;
            padding: 6px 12px;
            border-radius: 20px;
            background: rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(0, 0, 0, 0.06);
            max-width: 100%;
        }
        
        .attribution .attribution-sep {
            color: rgba(142, 142, 147, 0.6);
            font-weight: 400;
            user-select: none;
        }
        
        .attribution .context {
            color: #8E8E93;
        }
        
        .attribution .copyright {
            color: #8E8E93;
        }
        
        @media (prefers-color-scheme: dark) {
            .attribution {
                background: rgba(255, 255, 255, 0.06);
                border-color: rgba(255, 255, 255, 0.08);
                color: rgba(255, 255, 255, 0.7);
            }
            .attribution .context,
            .attribution .copyright { color: rgba(255, 255, 255, 0.7); }
            .attribution .attribution-sep { color: rgba(255, 255, 255, 0.4); }
        }
    """
