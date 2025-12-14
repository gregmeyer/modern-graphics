"""Story-driven slide generator - Compelling Apple-style hero slide"""

from typing import Optional, Dict, List
from ..base import BaseGenerator
from ..constants import ATTRIBUTION_STYLES


def generate_story_slide(
    generator: BaseGenerator,
    title: str,
    what_changed: str,
    time_period: str,
    what_it_means: str,
    insight: Optional[str] = None,
    evolution_data: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    Generate a compelling story-driven hero slide
    
    Args:
        generator: BaseGenerator instance
        title: Main slide title
        what_changed: What changed (the change)
        time_period: Over what time period
        what_it_means: What it means (the meaning/implication)
        insight: Optional key insight/takeaway
        evolution_data: Optional list of evolution stages
    """
    
    if insight is None:
        insight = "What changed, over what time period, and what does it mean? This is the basic insight you're building when you tell a story about data."
    
    if evolution_data is None:
        evolution_data = [
            {'era': '2010s', 'label': 'Manual Slides', 'icon': '📊'},
            {'era': '2020s', 'label': 'Automated Slides', 'icon': '⚡'},
            {'era': '2024+', 'label': 'Story-Driven', 'icon': '✨'}
        ]
    
    # Hero visual: Forward-looking story-driven transformation
    # Shows: Manual pain → Story input → Dynamic AI-generated output
    hero_visual = """<svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg">
        <!-- Left: The Tension - Manual slide building with last-minute change -->
        <g opacity="0.75">
            <!-- Person working on slide -->
            <circle cx="100" cy="140" r="20" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
            <rect x="90" y="160" width="20" height="35" rx="10" fill="rgba(255,255,255,0.4)" stroke="rgba(255,255,255,0.7)" stroke-width="2"/>
            
            <!-- Slide being edited manually -->
            <rect x="50" y="220" width="100" height="70" rx="6" fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.6)" stroke-width="2.5"/>
            <!-- Content lines -->
            <line x1="60" y1="235" x2="140" y2="235" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <line x1="60" y1="250" x2="120" y2="250" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <rect x="65" y="260" width="40" height="20" rx="3" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
            
            <!-- Last-minute change indicator (red alert) -->
            <circle cx="160" cy="180" r="18" fill="rgba(255,59,48,0.4)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <text x="160" y="188" font-family="-apple-system" font-size="20" font-weight="700" fill="rgba(255,255,255,0.95)" text-anchor="middle">!</text>
            <!-- Stress lines -->
            <path d="M 145 165 L 150 160 M 175 165 L 170 160 M 145 195 L 150 200 M 175 195 L 170 200" stroke="rgba(255,255,255,0.7)" stroke-width="2" stroke-linecap="round"/>
            
            <!-- Manual tools scattered -->
            <rect x="30" y="120" width="12" height="25" rx="2" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5" transform="rotate(-30 36 132)"/>
            <rect x="170" y="110" width="15" height="15" rx="2" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
        </g>
        
        <!-- Transformation arrow -->
        <path d="M 220 255 L 320 255" stroke="rgba(255,255,255,0.9)" stroke-width="10" stroke-linecap="round"/>
        <path d="M 310 245 L 320 255 L 310 265" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        
        <!-- Center: Your Story (the input) - Forward-looking, aspirational -->
        <g opacity="0.95">
            <!-- Story container (modern, fluid) -->
            <path d="M 340 100 Q 380 80 450 100 Q 480 120 450 140 Q 480 160 450 180 Q 480 200 450 220 Q 420 240 380 220 Q 340 200 360 180 Q 340 160 360 140 Q 340 120 360 100 Z" 
                  fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.9)" stroke-width="3.5"/>
            
            <!-- Story elements (narrative flow) -->
            <path d="M 370 120 Q 400 110 430 120" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M 375 150 Q 400 145 425 150" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            <path d="M 370 180 Q 400 175 430 180" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round"/>
            
            <!-- Story points -->
            <circle cx="370" cy="120" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="110" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="430" cy="120" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="150" r="4" fill="rgba(255,255,255,0.9)"/>
            <circle cx="400" cy="180" r="4" fill="rgba(255,255,255,0.9)"/>
            
            <!-- AI assistance indicator (subtle, modern) -->
            <circle cx="420" cy="100" r="5" fill="rgba(255,255,255,0.9)"/>
            <circle cx="425" cy="105" r="3" fill="rgba(255,255,255,0.7)"/>
            <circle cx="415" cy="105" r="3" fill="rgba(255,255,255,0.7)"/>
            <!-- Iteration/update symbol -->
            <path d="M 380 200 Q 400 195 420 200" stroke="rgba(52,199,89,0.8)" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-dasharray="3,3"/>
        </g>
        
        <!-- Arrow: Story generates slides -->
        <path d="M 500 255 L 600 255" stroke="rgba(255,255,255,0.9)" stroke-width="10" stroke-linecap="round"/>
        <path d="M 590 245 L 600 255 L 590 265" stroke="rgba(255,255,255,0.9)" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        
        <!-- Right: Dynamic Output - Slides generated from story -->
        <g opacity="0.95">
            <!-- Slides flowing out (dynamic, varied) -->
            <rect x="650" y="100" width="80" height="60" rx="6" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" transform="rotate(-8 690 130)"/>
            <rect x="670" y="180" width="80" height="60" rx="6" fill="rgba(255,255,255,0.3)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <rect x="650" y="260" width="80" height="60" rx="6" fill="rgba(255,255,255,0.25)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5" transform="rotate(8 690 290)"/>
            
            <!-- Dynamic content (varied, showing AI generation) -->
            <!-- Slide 1: Chart/data -->
            <rect x="665" y="115" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <rect x="665" y="125" width="50" height="6" rx="3" fill="rgba(255,255,255,0.6)"/>
            <rect x="670" y="135" width="20" height="15" rx="2" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1"/>
            <rect x="695" y="140" width="20" height="10" rx="2" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1"/>
            
            <!-- Slide 2: Text/story -->
            <rect x="685" y="195" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <rect x="685" y="205" width="55" height="6" rx="3" fill="rgba(255,255,255,0.6)"/>
            <rect x="685" y="215" width="45" height="6" rx="3" fill="rgba(255,255,255,0.5)"/>
            <rect x="685" y="225" width="50" height="6" rx="3" fill="rgba(255,255,255,0.5)"/>
            
            <!-- Slide 3: Visual/infographic -->
            <rect x="665" y="275" width="60" height="6" rx="3" fill="rgba(255,255,255,0.7)"/>
            <circle cx="680" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            <circle cx="700" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            <circle cx="720" cy="295" r="8" fill="rgba(255,255,255,0.5)" stroke="rgba(255,255,255,0.8)" stroke-width="1.5"/>
            
            <!-- Flow lines showing generation from story -->
            <path d="M 500 255 Q 550 200 650 130" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            <path d="M 500 255 Q 575 255 670 210" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            <path d="M 500 255 Q 550 310 650 290" stroke="rgba(255,255,255,0.5)" stroke-width="2.5" fill="none" stroke-dasharray="5,5" opacity="0.7"/>
            
            <!-- Update/iteration indicator (showing dynamic nature) -->
            <circle cx="750" cy="120" r="12" fill="rgba(52,199,89,0.4)" stroke="rgba(255,255,255,0.9)" stroke-width="2.5"/>
            <path d="M 745 120 L 750 128 L 755 115" stroke="rgba(255,255,255,0.9)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
        
        <!-- Labels - Emotionally resonant, not corporate -->
        <text x="100" y="310" font-family="-apple-system" font-size="20" font-weight="600" fill="rgba(255,255,255,0.85)" text-anchor="middle">The Tension</text>
        <text x="100" y="330" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.65)" text-anchor="middle">Perfect slides, last-minute changes</text>
        
        <text x="400" y="85" font-family="-apple-system" font-size="22" font-weight="700" fill="rgba(255,255,255,0.95)" text-anchor="middle">Your Story</text>
        <text x="400" y="105" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.75)" text-anchor="middle">Narrative + AI assistance</text>
        
        <text x="700" y="310" font-family="-apple-system" font-size="20" font-weight="600" fill="rgba(255,255,255,0.85)" text-anchor="middle">Dynamic Output</text>
        <text x="700" y="330" font-family="-apple-system" font-size="15" font-weight="500" fill="rgba(255,255,255,0.65)" text-anchor="middle">Slides that evolve with your story</text>
    </svg>"""
    
    # Generate evolution timeline HTML
    evolution_html = ''
    for i, stage in enumerate(evolution_data):
        is_last = i == len(evolution_data) - 1
        evolution_html += f"""
            <div class="evolution-stage">
                <div class="evolution-icon">{stage.get('icon', '•')}</div>
                <div class="evolution-era">{stage['era']}</div>
                <div class="evolution-label">{stage['label']}</div>
            </div>"""
        if not is_last:
            evolution_html += '<div class="evolution-arrow">→</div>'
    
    css_content = f"""
        body {{
            padding: 0 !important;
            margin: 0;
            background: linear-gradient(135deg, #F9F0FF 0%, #F3E5F5 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .story-slide-container {{
            max-width: 1800px;
            width: 100%;
            background: #FFFFFF;
            border-radius: 0;
            padding: 0;
            box-shadow: 0 40px 80px rgba(130, 67, 181, 0.3), 0 16px 32px rgba(0, 0, 0, 0.12);
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section {{
            background: linear-gradient(135deg, #AF52DE 0%, #8243B5 100%);
            padding: 100px 80px 80px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero-section::before {{
            content: '';
            position: absolute;
            top: -40%;
            right: -8%;
            width: 700px;
            height: 700px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 50%;
        }}
        
        .hero-section::after {{
            content: '';
            position: absolute;
            bottom: -25%;
            left: -3%;
            width: 500px;
            height: 500px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 50%;
        }}
        
        .hero-headline {{
            font-size: 112px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 20px;
            letter-spacing: -0.06em;
            line-height: 1.0;
            position: relative;
            z-index: 1;
        }}
        
        .hero-subheadline {{
            font-size: 40px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.95);
            letter-spacing: -0.03em;
            line-height: 1.2;
            margin-bottom: 60px;
            position: relative;
            z-index: 1;
        }}
        
        .hero-visual {{
            margin-top: 40px;
            position: relative;
            z-index: 1;
        }}
        
        .transformation-icon {{
            width: 100%;
            max-width: 800px;
            height: auto;
            margin: 0 auto;
        }}
        
        .transformation-icon svg {{
            width: 100%;
            height: auto;
        }}
        
        .story-framework-section {{
            padding: 80px 100px;
            background: #FFFFFF;
        }}
        
        .story-framework {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 48px;
            margin-bottom: 60px;
        }}
        
        .story-element {{
            background: linear-gradient(135deg, #F9F0FF 0%, #F3E5F5 100%);
            border-radius: 24px;
            padding: 48px 40px;
            border: 2px solid rgba(130, 67, 181, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
        }}
        
        .story-element:hover {{
            transform: translateY(-8px);
            box-shadow: 0 16px 40px rgba(130, 67, 181, 0.3);
        }}
        
        .story-element:nth-child(1) {{
            background: linear-gradient(135deg, #EBF5FF 0%, #E3F2FD 100%);
            border-color: rgba(11, 100, 208, 0.2);
        }}
        
        .story-element:nth-child(2) {{
            background: linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%);
            border-color: rgba(58, 58, 60, 0.15);
        }}
        
        .story-element:nth-child(3) {{
            background: linear-gradient(135deg, #F0F9F4 0%, #E8F5E9 100%);
            border-color: rgba(27, 122, 78, 0.2);
        }}
        
        .story-icon {{
            width: 80px;
            height: 80px;
            margin: 0 auto 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .story-icon svg {{
            width: 100%;
            height: 100%;
        }}
        
        .story-label {{
            font-size: 12px;
            font-weight: 600;
            color: #8243B5;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 20px;
            text-align: center;
        }}
        
        .story-element:nth-child(1) .story-label {{
            color: #0B64D0;
        }}
        
        .story-element:nth-child(3) .story-label {{
            color: #1B7A4E;
        }}
        
        .story-value {{
            font-size: 32px;
            font-weight: 700;
            color: #1D1D1F;
            letter-spacing: -0.03em;
            line-height: 1.3;
            text-align: center;
        }}
        
        .evolution-section {{
            padding: 60px 100px;
            background: linear-gradient(135deg, #F5F5F7 0%, #F5F5F7 100%);
        }}
        
        .evolution-timeline {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 32px;
            flex-wrap: wrap;
        }}
        
        .evolution-stage {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            min-width: 140px;
        }}
        
        .evolution-icon {{
            font-size: 48px;
            line-height: 1;
        }}
        
        .evolution-era {{
            font-size: 20px;
            font-weight: 700;
            color: #8243B5;
            letter-spacing: -0.02em;
        }}
        
        .evolution-label {{
            font-size: 16px;
            font-weight: 500;
            color: #8E8E93;
            text-align: center;
        }}
        
        .evolution-arrow {{
            color: #8243B5;
            font-size: 36px;
            font-weight: 600;
            opacity: 0.6;
        }}
        
        .insight-section {{
            background: linear-gradient(135deg, #AF52DE 0%, #8243B5 100%);
            padding: 80px 100px;
            position: relative;
            overflow: hidden;
        }}
        
        .insight-section::before {{
            content: '';
            position: absolute;
            top: -40%;
            right: -5%;
            width: 500px;
            height: 500px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
        }}
        
        .insight-label {{
            font-size: 13px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.9);
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 24px;
            text-align: center;
        }}
        
        .insight-text {{
            font-size: 42px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.03em;
            line-height: 1.4;
            text-align: center;
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        {ATTRIBUTION_STYLES}
        """
    
    # Generate SVG icons for story elements - avoiding clichés, forward-looking
    what_changed_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Transformation: Input/Output flip -->
        <rect x="15" y="20" width="20" height="15" rx="2" fill="#007AFF" opacity="0.2" stroke="#007AFF" stroke-width="2"/>
        <rect x="15" y="40" width="20" height="15" rx="2" fill="#007AFF" opacity="0.2" stroke="#007AFF" stroke-width="2"/>
        <path d="M 45 27 L 55 27" stroke="#8243B5" stroke-width="3" stroke-linecap="round"/>
        <path d="M 50 22 L 55 27 L 50 32" stroke="#8243B5" stroke-width="3" fill="none" stroke-linecap="round"/>
        <!-- Output (story arc) -->
        <path d="M 60 20 Q 70 15 75 20 Q 70 25 60 30" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.15)" stroke-linecap="round"/>
        <path d="M 60 40 Q 70 35 75 40 Q 70 45 60 50" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.15)" stroke-linecap="round"/>
    </svg>"""
    
    time_period_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Modern timeline indicator -->
        <line x1="20" y1="40" x2="60" y2="40" stroke="#8E8E93" stroke-width="3" stroke-linecap="round"/>
        <circle cx="20" cy="40" r="5" fill="#8E8E93"/>
        <circle cx="40" cy="40" r="5" fill="#8E8E93"/>
        <circle cx="60" cy="40" r="8" fill="#8243B5" stroke="#8243B5" stroke-width="2"/>
        <circle cx="60" cy="40" r="4" fill="#FFFFFF"/>
        <!-- 2024 label -->
        <text x="60" y="65" font-family="-apple-system" font-size="13" font-weight="700" fill="#8243B5" text-anchor="middle">2024</text>
    </svg>"""
    
    what_it_means_icon = """<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <!-- Forward-looking: Focus shift visualization -->
        <rect x="20" y="25" width="25" height="18" rx="3" fill="#8E8E93" opacity="0.2" stroke="#8E8E93" stroke-width="2"/>
        <path d="M 50 34 L 60 34" stroke="#8243B5" stroke-width="3" stroke-linecap="round"/>
        <path d="M 55 29 L 60 34 L 55 39" stroke="#8243B5" stroke-width="3" fill="none" stroke-linecap="round"/>
        <!-- Narrative focus (story arc) -->
        <path d="M 60 20 Q 70 15 75 25 Q 70 35 60 40 Q 65 30 60 20" stroke="#8243B5" stroke-width="3.5" fill="rgba(130,67,181,0.2)" stroke-linecap="round"/>
        <!-- Forward arrow -->
        <path d="M 65 45 L 70 50 L 65 55" stroke="#1B7A4E" stroke-width="3" fill="none" stroke-linecap="round"/>
    </svg>"""
    
    html_content = f"""
    <div class="story-slide-container">
        <div class="hero-section">
            <div class="hero-headline">{title}</div>
            <div class="hero-subheadline">Start Building Stories</div>
            <div class="hero-visual">
                <div class="transformation-icon">
                    {hero_visual}
                </div>
            </div>
        </div>
        
        <div class="story-framework-section">
            <div class="story-framework">
                <div class="story-element">
                    <div class="story-icon">{what_changed_icon}</div>
                    <div class="story-label">What Changed</div>
                    <div class="story-value">{what_changed}</div>
                </div>
                <div class="story-element">
                    <div class="story-icon">{time_period_icon}</div>
                    <div class="story-label">Time Period</div>
                    <div class="story-value">{time_period}</div>
                </div>
                <div class="story-element">
                    <div class="story-icon">{what_it_means_icon}</div>
                    <div class="story-label">What It Means</div>
                    <div class="story-value">{what_it_means}</div>
                </div>
            </div>
            
            <div class="evolution-section">
                <div class="evolution-timeline">
{evolution_html}
                </div>
            </div>
        </div>
        
        <div class="insight-section">
            <div class="insight-label">The Core Insight</div>
            <div class="insight-text">{insight}</div>
        </div>
        
        {generator._generate_attribution_html()}
    </div>
        """
    
    return generator._wrap_html(html_content, css_content)
