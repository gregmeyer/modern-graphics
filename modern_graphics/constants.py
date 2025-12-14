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
            font-size: 12px;
            font-weight: 500;
            color: #C7C7CC;
            letter-spacing: -0.01em;
            text-align: right;
        }
        
        .attribution .context {
            margin-bottom: 2px;
            color: #C7C7CC;
        }
        
        .attribution .copyright {
            color: #C7C7CC;
        }
    """
