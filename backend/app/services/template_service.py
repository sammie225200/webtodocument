class TemplateService:

    templates = {

        "modern": """
Modern SaaS design.
Glassmorphism.
Gradient backgrounds.
Responsive layout.
""",

        "corporate": """
Professional business website.
Conservative colors.
Corporate layout.
""",

        "startup": """
Startup landing page.
Bold typography.
Strong CTA.
""",

        "portfolio": """
Creative portfolio.
Project showcase.
Large imagery.
""",

        "minimal": """
Minimalist design.
Lots of whitespace.
Elegant typography.
"""
    }

    @classmethod
    def get_template(
        cls,
        template_name: str
    ):

        return cls.templates.get(
            template_name,
            cls.templates["modern"]
        )