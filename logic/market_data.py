"""
market_data.py
==============
Curated career intelligence dataset.

Sources simulated from:
- roadmap.sh community data (skills, paths)
- BLS & LinkedIn Workforce Reports (demand, salaries)
- Stack Overflow Developer Survey 2024/25
- Twitter/X tech hiring threads & LinkedIn job trend analysis
- Future Risk Analysis for AI substitution

Includes orthodox tech paths and 2026+ hybrid AI domains.
"""

ROLES = {
    # ── AI / ML ─────────────────────────────────────────────────────────
    "ai-engineer": {
        "slug": "ai-engineer",
        "title": "AI Engineer",
        "demand_score": 97,
        "yoy_growth": "+68%",
        "avg_salary": "$145k – $230k",
        "scope": "Explosive",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk (Building the tools)",
        "trending": True,
        "trending_reason": "Every company is hiring AI engineers to integrate LLMs. Demand doubled in 6 months.",
        "social_signal": 96,
        "top_hiring": ["OpenAI", "Anthropic", "Google DeepMind", "Microsoft", "Meta AI"],
        "tag": "Hottest Right Now",
        "roadmap_slug": "ai-engineer",
        "match_keywords": [
            "ai", "artificial intelligence", "llm", "gpt", "chatgpt", "openai",
            "generative", "ml", "deep learning", "neural", "language model",
            "build ai", "ai products", "ai apps"
        ],
    },
    "machine-learning": {
        "slug": "machine-learning",
        "title": "Machine Learning Engineer",
        "demand_score": 93,
        "yoy_growth": "+42%",
        "avg_salary": "$135k – $210k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "ML pipelines are core infrastructure. Demand for production ML engineers is outpacing supply.",
        "social_signal": 91,
        "top_hiring": ["Google", "Amazon", "Tesla", "Nvidia", "Hugging Face"],
        "tag": "High Growth",
        "roadmap_slug": "machine-learning",
        "match_keywords": [
            "machine learning", "ml", "data", "models", "training", "tensorflow",
            "pytorch", "scikit", "algorithms", "math", "statistics", "prediction"
        ],
    },
    "mlops": {
        "slug": "mlops",
        "title": "MLOps Engineer",
        "demand_score": 88,
        "yoy_growth": "+55%",
        "avg_salary": "$130k – $195k",
        "scope": "High",
        "lifetime": "Long-term (8+ yrs)",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "As ML moves to production, MLOps is the bottleneck. LinkedIn shows 3x listings YoY.",
        "social_signal": 85,
        "top_hiring": ["Netflix", "Uber", "Airbnb", "Databricks", "Scale AI"],
        "tag": "Fast Growing",
        "roadmap_slug": "mlops",
        "match_keywords": [
            "mlops", "devops ml", "model deployment", "pipeline", "kubernetes ml",
            "infrastructure", "ci cd", "docker", "cloud", "deploy models"
        ],
    },
    "ai-data-scientist": {
        "slug": "ai-data-scientist",
        "title": "AI Data Scientist",
        "demand_score": 90,
        "yoy_growth": "+38%",
        "avg_salary": "$125k – $190k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Medium Risk (Pure data science is shifting to AI)",
        "trending": True,
        "trending_reason": "Data science + AI fusion is the new standard. Companies want scientists who ship AI products.",
        "social_signal": 89,
        "top_hiring": ["Palantir", "Two Sigma", "Stripe", "LinkedIn", "Salesforce"],
        "tag": "High Growth",
        "roadmap_slug": "ai-data-scientist",
        "match_keywords": [
            "data science", "data scientist", "analytics", "statistics", "insights",
            "visualization", "jupyter", "pandas", "numpy", "research"
        ],
    },
    # ── Hybrid AI Roles (2026+ Era) ──────────────────────────────────────
    "ai-healthcare": {
        "slug": "ai-healthcare",
        "title": "HealthTech AI Specialist",
        "demand_score": 88,
        "yoy_growth": "+95%",
        "avg_salary": "$130k – $200k",
        "scope": "Emerging & Explosive",
        "lifetime": "Long-term (15+ yrs)",
        "risk_level": "Very Low Risk (High barrier to entry)",
        "trending": True,
        "trending_reason": "Bioinformatics and AI diagnostics are heavily trending on X/LinkedIn. Merging medicine with LLMs.",
        "social_signal": 93,
        "top_hiring": ["DeepMind Health", "Tempus", "Flatiron Health", "Johnson & Johnson", "Neuralink"],
        "tag": "Hybrid Discipline",
        "roadmap_slug": "ai-engineer", # Using AI engineer roadmap as base, assuming custom logic handles paths
        "match_keywords": [
            "health", "medicine", "medical", "bioinformatics", "biology", "healthcare",
            "diagnostics", "biotech", "ai doctor"
        ],
    },
    "ai-finance": {
        "slug": "ai-finance",
        "title": "AI Quantitative Analyst",
        "demand_score": 91,
        "yoy_growth": "+45%",
        "avg_salary": "$180k – $400k+",
        "scope": "Very High",
        "lifetime": "Long-term",
        "risk_level": "Medium Risk (Highly competitive)",
        "trending": True,
        "trending_reason": "Quant funds are moving to neural networks over traditional stats. Huge financial upside.",
        "social_signal": 87,
        "top_hiring": ["Citadel", "Jane Street", "Two Sigma", "Renaissance Technologies", "Bloomberg"],
        "tag": "High Pay Hybrid",
        "roadmap_slug": "machine-learning",
        "match_keywords": [
            "finance", "quantitative", "quant", "trading", "crypto", "trading bot",
            "stocks", "fintech", "market maker", "economics"
        ],
    },
    "ai-legal": {
        "slug": "ai-legal",
        "title": "Legal Tech AI Engineer",
        "demand_score": 84,
        "yoy_growth": "+110%",
        "avg_salary": "$120k – $185k",
        "scope": "Explosive Growth",
        "lifetime": "Medium-term",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "LLMs can pass the bar and write contracts. Massive demand for engineers in legal compliance tech.",
        "social_signal": 95,
        "top_hiring": ["Harvey AI", "Ironclad", "LexisNexis", "Top Law Firms", "LegalZoom"],
        "tag": "Trending Hybrid",
        "roadmap_slug": "prompt-engineering",
        "match_keywords": [
            "law", "legal", "contracts", "compliance", "lawyer", "attorney",
            "regulatory", "policy", "legaltech"
        ],
    },
    # ── Web Development ──────────────────────────────────────────────────
    "frontend": {
        "slug": "frontend",
        "title": "Frontend Developer",
        "demand_score": 82,
        "yoy_growth": "+18%",
        "avg_salary": "$95k – $155k",
        "scope": "High",
        "lifetime": "Medium-term (AI assisting code)",
        "risk_level": "High Risk (Highly susceptible to AI generation)",
        "trending": True,
        "trending_reason": "React 19, Next.js 15 & AI-powered UI tools are driving a hiring surge, but AI is speeding up output.",
        "social_signal": 84,
        "top_hiring": ["Vercel", "Shopify", "Stripe", "Figma", "Linear"],
        "tag": "Trending",
        "roadmap_slug": "frontend",
        "match_keywords": [
            "frontend", "web", "html", "css", "react", "vue", "angular", "javascript",
            "typescript", "ui", "interface", "design", "browser", "websites", "apps"
        ],
    },
    "backend": {
        "slug": "backend",
        "title": "Backend Developer",
        "demand_score": 84,
        "yoy_growth": "+22%",
        "avg_salary": "$100k – $165k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Medium Risk (Core logic remains critical)",
        "trending": False,
        "trending_reason": "APIs and backend systems power every product. Consistently among the most-listed roles on LinkedIn.",
        "social_signal": 80,
        "top_hiring": ["Amazon", "Twilio", "Cloudflare", "Notion", "Discord"],
        "tag": "Evergreen",
        "roadmap_slug": "backend",
        "match_keywords": [
            "backend", "server", "api", "database", "node", "python", "java", "go",
            "sql", "rest", "graphql", "microservices", "architecture", "systems"
        ],
    },
    "full-stack": {
        "slug": "full-stack",
        "title": "Full Stack Developer",
        "demand_score": 85,
        "yoy_growth": "+24%",
        "avg_salary": "$105k – $170k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Medium Risk",
        "trending": True,
        "trending_reason": "Startups prefer full-stack generalists. Demand from Series A/B companies up 40% on LinkedIn.",
        "social_signal": 83,
        "top_hiring": ["Stripe", "Notion", "Linear", "Vercel", "Y Combinator startups"],
        "tag": "High Demand",
        "roadmap_slug": "full-stack",
        "match_keywords": [
            "full stack", "fullstack", "both frontend backend", "startup", "product",
            "build things", "ship", "web app", "saas"
        ],
    },
    # ── Infrastructure / DevOps ──────────────────────────────────────────
    "devops": {
        "slug": "devops",
        "title": "DevOps Engineer",
        "demand_score": 87,
        "yoy_growth": "+30%",
        "avg_salary": "$110k – $175k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk (Hard for AI to touch infra safely)",
        "trending": True,
        "trending_reason": "Cloud-native adoption accelerating. Platform engineering is Twitter's most-discussed ops topic.",
        "social_signal": 82,
        "top_hiring": ["AWS", "HashiCorp", "GitLab", "Datadog", "PagerDuty"],
        "tag": "Fast Growing",
        "roadmap_slug": "devops",
        "match_keywords": [
            "devops", "infrastructure", "cloud", "aws", "gcp", "azure", "docker",
            "kubernetes", "ci/cd", "deployment", "automation", "terraform", "sre"
        ],
    },
    "cyber-security": {
        "slug": "cyber-security",
        "title": "Cybersecurity Engineer",
        "demand_score": 92,
        "yoy_growth": "+35%",
        "avg_salary": "$115k – $185k",
        "scope": "Explosive",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Very Low Risk",
        "trending": True,
        "trending_reason": "AI-powered cyberattacks surging. Every org needs security engineers. Global shortage of 3.5M+.",
        "social_signal": 88,
        "top_hiring": ["CrowdStrike", "Palo Alto Networks", "SentinelOne", "FBI", "Palantir"],
        "tag": "Critical Need",
        "roadmap_slug": "cyber-security",
        "match_keywords": [
            "security", "cybersecurity", "hacking", "penetration", "ethical hacking",
            "red team", "blue team", "soc", "malware", "vulnerabilities", "ctf"
        ],
    },
    "ai-red-teaming": {
        "slug": "ai-red-teaming",
        "title": "AI Red Team Engineer",
        "demand_score": 91,
        "yoy_growth": "+80%",
        "avg_salary": "$140k – $220k",
        "scope": "Explosive",
        "lifetime": "Long-term (8+ yrs)",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "Governments mandating AI safety. OpenAI, Anthropic, NIST all hiring red teamers urgently.",
        "social_signal": 94,
        "top_hiring": ["OpenAI", "Anthropic", "Google", "Microsoft", "NIST"],
        "tag": "Brand New Field",
        "roadmap_slug": "ai-red-teaming",
        "match_keywords": [
            "ai safety", "red team", "llm security", "prompt injection", "adversarial",
            "jailbreak", "model evaluation", "bias", "harm", "alignment"
        ],
    },
    # ── Data ────────────────────────────────────────────────────────────
    "data-engineer": {
        "slug": "data-engineer",
        "title": "Data Engineer",
        "demand_score": 89,
        "yoy_growth": "+40%",
        "avg_salary": "$120k – $185k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "Data pipelines are the foundation of AI. Every AI project needs data engineers upstream.",
        "social_signal": 85,
        "top_hiring": ["Snowflake", "Databricks", "Spotify", "Airbnb", "Netflix"],
        "tag": "High Growth",
        "roadmap_slug": "data-engineer",
        "match_keywords": [
            "data engineering", "data pipeline", "etl", "spark", "kafka", "snowflake",
            "dbt", "airflow", "warehouse", "big data", "data infrastructure"
        ],
    },
    # ── Prompt / Product ─────────────────────────────────────────────────
    "prompt-engineering": {
        "slug": "prompt-engineering",
        "title": "Prompt Engineer",
        "demand_score": 79,
        "yoy_growth": "+120%",
        "avg_salary": "$90k – $150k",
        "scope": "Growing",
        "lifetime": "Medium-term (3–5 yrs, evolving)",
        "risk_level": "High Risk (Skills might integrate into all roles)",
        "trending": True,
        "trending_reason": "Viral LinkedIn posts on $300k prompt engineer salaries. Growing faster than any tech role.",
        "social_signal": 92,
        "top_hiring": ["Anthropic", "Scale AI", "Inflection AI", "Character.ai", "Cohere"],
        "tag": "Viral Role",
        "roadmap_slug": "prompt-engineering",
        "match_keywords": [
            "prompt", "prompt engineering", "chatgpt", "claude", "llm", "language model",
            "no code", "ai tools", "workflow", "automation", "productivity"
        ],
    },
    "product-manager": {
        "slug": "product-manager",
        "title": "AI Product Manager",
        "demand_score": 83,
        "yoy_growth": "+29%",
        "avg_salary": "$120k – $190k",
        "scope": "High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk (Product vision is hard to automate)",
        "trending": True,
        "trending_reason": "PMs who understand AI are commanding 40% salary premiums. Most-wanted hybrid role per LinkedIn.",
        "social_signal": 86,
        "top_hiring": ["Google", "Apple", "Stripe", "Figma", "OpenAI"],
        "tag": "Premium Role",
        "roadmap_slug": "product-manager",
        "match_keywords": [
            "product", "product manager", "product management", "strategy",
            "roadmap planning", "user research", "business", "startup founder",
            "growth", "metrics", "go to market"
        ],
    },
    # ── Mobile ──────────────────────────────────────────────────────────
    "android": {
        "slug": "android",
        "title": "Android Developer",
        "demand_score": 78,
        "yoy_growth": "+15%",
        "avg_salary": "$100k – $155k",
        "scope": "Stable",
        "lifetime": "Long-term (8+ yrs)",
        "risk_level": "Medium Risk",
        "trending": False,
        "trending_reason": "Kotlin & Jetpack Compose modernising Android. Consistent demand across enterprises and startups.",
        "social_signal": 72,
        "top_hiring": ["Google", "Samsung", "Spotify", "Duolingo", "Grab"],
        "tag": "Stable Demand",
        "roadmap_slug": "android",
        "match_keywords": [
            "android", "mobile", "kotlin", "java android", "app development", "play store"
        ],
    },
    "ios": {
        "slug": "ios",
        "title": "iOS Developer",
        "demand_score": 80,
        "yoy_growth": "+16%",
        "avg_salary": "$105k – $165k",
        "scope": "Stable",
        "lifetime": "Long-term (8+ yrs)",
        "risk_level": "Medium Risk",
        "trending": False,
        "trending_reason": "Apple ecosystem expanding with visionOS. Swift developers consistently in demand.",
        "social_signal": 74,
        "top_hiring": ["Apple", "Airbnb", "Lyft", "Square", "Robinhood"],
        "tag": "Stable Demand",
        "roadmap_slug": "ios",
        "match_keywords": [
            "ios", "iphone", "swift", "apple", "app store", "swiftui", "mobile apple"
        ],
    },
    # ── Cloud ────────────────────────────────────────────────────────────
    "aws": {
        "slug": "aws",
        "title": "Cloud / AWS Engineer",
        "demand_score": 90,
        "yoy_growth": "+33%",
        "avg_salary": "$115k – $180k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Low Risk",
        "trending": True,
        "trending_reason": "AWS dominates 32% of cloud market. Certified engineers see immediate job placement.",
        "social_signal": 83,
        "top_hiring": ["AWS", "JPMorgan", "Accenture", "Deloitte", "FAANG"],
        "tag": "Always Hiring",
        "roadmap_slug": "aws",
        "match_keywords": [
            "cloud", "aws", "amazon web services", "azure", "gcp", "serverless",
            "infrastructure", "cloud computing", "s3", "ec2", "lambda"
        ],
    },
    # ── System Design ────────────────────────────────────────────────────
    "system-design": {
        "slug": "system-design",
        "title": "Software Architect",
        "demand_score": 88,
        "yoy_growth": "+25%",
        "avg_salary": "$140k – $220k",
        "scope": "Very High",
        "lifetime": "Long-term (10+ yrs)",
        "risk_level": "Very Low Risk (Strategy context over code generation)",
        "trending": False,
        "trending_reason": "Senior engineers who can design large-scale systems are the highest-paid individual contributors.",
        "social_signal": 80,
        "top_hiring": ["FAANG", "Bloomberg", "Citadel", "Goldman Sachs", "Cloudflare"],
        "tag": "Senior & High Pay",
        "roadmap_slug": "system-design",
        "match_keywords": [
            "architecture", "system design", "distributed systems", "scalability",
            "senior engineer", "staff engineer", "principal", "design patterns"
        ],
    },
}


def get_all_roles() -> list[dict]:
    return list(ROLES.values())


def get_role(slug: str) -> dict | None:
    return ROLES.get(slug)
