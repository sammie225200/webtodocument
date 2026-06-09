from openai import OpenAI
import os
from typing import Optional

class MistralService:
    def __init__(self):
        # IMPORTANT: Use environment variable in production!
        self.api_key = "YOUR_MISTRAL_API_KEY_HERE"  # Replace with your key
        self.client = OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=self.api_key
        )
    
    async def generate_website(self, document_text: str, style: str = "modern") -> dict:
        """Generate HTML/CSS/JS website from document text"""
        
        style_prompts = {
            "modern": "modern, clean, glassmorphism design with gradients and smooth animations",
            "minimal": "minimalist, clean whitespace, simple typography, no clutter",
            "corporate": "professional, business-like, trust colors (blue/gray), structured",
            "playful": "colorful, rounded corners, fun animations, vibrant palette",
            "dark": "dark theme, neon accents, futuristic, sleek"
        }
        
        style_description = style_prompts.get(style, style_prompts["modern"])
        
        system_prompt = f"""You are an expert web developer. Generate a complete, responsive website based on the document content.
        
Style requirements: {style_description}

Technical requirements:
- Use HTML5, CSS3, and vanilla JavaScript
- Must be fully responsive (mobile, tablet, desktop)
- Include a proper <!DOCTYPE html> structure
- Use CSS Grid or Flexbox for layouts
- Add smooth transitions and hover effects
- Include appropriate meta tags for viewport
- No external dependencies (no Tailwind, Bootstrap, etc.) - pure CSS only
- Make it visually appealing and professional
- Extract key information from the document to structure the content

Return ONLY the HTML code, no explanations, no markdown formatting.
"""

        try:
            response = self.client.chat.completions.create(
                model="codestral-latest",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a website from this document:\n\n{document_text[:20000]}"}
                ],
                max_tokens=32000,
                temperature=0.3
            )
            
            html_code = response.choices[0].message.content
            
            # Clean up markdown if present
            if html_code.startswith("```html"):
                html_code = html_code.replace("```html", "").replace("```", "")
            
            return {
                "success": True,
                "html": html_code,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }