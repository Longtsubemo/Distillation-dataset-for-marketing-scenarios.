"""
scenario_generator.py - Auto-generate diverse marketing scenarios (FIXED)

Generates realistic scenarios by combining:
- Platforms (Meta, Google)
- Industries (10 types)
- Performance levels (excellent, good, declining, poor, mixed)
- Realistic metrics based on industry benchmarks
"""

import random
from typing import List, Dict

# ============================================================
# CONFIGURATION: Industries and their typical metrics
# ============================================================

INDUSTRIES = {
    "ecommerce_fashion": {
        "name": "E-commerce (Fashion)",
        "objectives": ["Purchase Conversions", "Online Sales"],
        "avg_order_value": (45, 120),
        "typical_ctr": (1.2, 2.0),
        "typical_cvr": (1.5, 3.5),
        "typical_cpc_meta": (0.50, 1.20),
        "typical_cpc_google": (0.60, 1.50),
        "weekly_spend_range": (5000, 15000),
        "context_templates": [
            "Selling women's clothing and accessories. Targeting ages {age_range}.",
            "Men's fashion brand. Focus on {season} collection.",
            "Fast fashion retailer targeting young adults {age_range}.",
        ]
    },
    "ecommerce_electronics": {
        "name": "E-commerce (Electronics)",
        "objectives": ["Online Sales", "Purchase Conversions"],
        "avg_order_value": (80, 400),
        "typical_ctr": (1.8, 3.0),
        "typical_cvr": (1.2, 2.5),
        "typical_cpc_meta": (0.35, 0.80),
        "typical_cpc_google": (0.40, 0.90),
        "weekly_spend_range": (8000, 20000),
        "context_templates": [
            "Selling smartphones, laptops, and accessories.",
            "Consumer electronics retailer. Competing with major brands.",
            "Tech gadgets and accessories store targeting tech enthusiasts.",
        ]
    },
    "ecommerce_home": {
        "name": "E-commerce (Home & Garden)",
        "objectives": ["Purchase Conversions", "Online Sales"],
        "avg_order_value": (60, 200),
        "typical_ctr": (1.0, 1.8),
        "typical_cvr": (1.5, 3.0),
        "typical_cpc_meta": (0.45, 1.00),
        "typical_cpc_google": (0.50, 1.20),
        "weekly_spend_range": (4000, 12000),
        "context_templates": [
            "Home decor and furniture. Targeting homeowners {age_range}.",
            "Garden supplies and outdoor furniture.",
            "Kitchen and home organization products.",
        ]
    },
    "b2b_saas": {
        "name": "B2B SaaS",
        "objectives": ["Lead Generation (Demo Requests)", "Lead Generation (Free Trial Signups)"],
        "avg_order_value": (0, 0),
        "typical_ctr": (2.0, 4.0),
        "typical_cvr": (2.0, 5.0),
        "typical_cpc_meta": (1.50, 4.00),
        "typical_cpc_google": (3.00, 8.00),
        "weekly_spend_range": (3000, 12000),
        "context_templates": [
            "Project management software. Competing with {competitors}.",
            "CRM platform targeting small businesses.",
            "HR software solution for mid-market companies.",
            "Marketing automation tool for agencies.",
        ]
    },
    "local_healthcare": {
        "name": "Local Service (Healthcare)",
        "objectives": ["Lead Generation (Appointment Bookings)", "Lead Generation"],
        "avg_order_value": (100, 300),
        "typical_ctr": (1.4, 2.5),
        "typical_cvr": (3.0, 6.0),
        "typical_cpc_meta": (0.60, 1.50),
        "typical_cpc_google": (1.50, 4.00),
        "weekly_spend_range": (1500, 5000),
        "context_templates": [
            "Dental clinic. Targeting {radius}-mile radius. Ages {age_range}.",
            "Medical spa offering cosmetic treatments.",
            "Physical therapy clinic targeting active adults.",
            "Optometry practice promoting eye exams and glasses.",
        ]
    },
    "local_home_services": {
        "name": "Local Service (Home Services)",
        "objectives": ["Lead Generation", "Lead Generation (Quote Requests)"],
        "avg_order_value": (150, 500),
        "typical_ctr": (1.5, 3.0),
        "typical_cvr": (3.0, 7.0),
        "typical_cpc_meta": (0.80, 2.00),
        "typical_cpc_google": (2.00, 6.00),
        "weekly_spend_range": (2000, 6000),
        "context_templates": [
            "HVAC services. Targeting homeowners within {radius} miles.",
            "Plumbing company serving local area.",
            "Roofing contractor targeting {radius}-mile radius.",
            "House cleaning service for busy professionals.",
        ]
    },
    "mobile_app_fitness": {
        "name": "Mobile App (Fitness)",
        "objectives": ["App Installs", "App Installs + In-App Purchases"],
        "avg_order_value": (10, 60),
        "typical_ctr": (1.5, 2.5),
        "typical_cvr": (12, 18),  # Install rate from clicks (higher for apps)
        "typical_cpc_meta": (0.25, 0.60),
        "typical_cpc_google": (0.40, 0.80),
        "weekly_spend_range": (2000, 8000),
        "context_templates": [
            "Fitness app with subscription model. ${price}/month.",
            "Workout tracking app targeting health-conscious users {age_range}.",
            "Yoga and meditation app. Freemium model.",
        ]
    },
    "mobile_app_finance": {
        "name": "Mobile App (Finance)",
        "objectives": ["App Installs", "App Installs + Account Signups"],
        "avg_order_value": (0, 0),
        "typical_ctr": (1.2, 2.0),
        "typical_cvr": (8, 14),
        "typical_cpc_meta": (0.60, 1.50),
        "typical_cpc_google": (0.80, 2.00),
        "weekly_spend_range": (3000, 10000),
        "context_templates": [
            "Personal finance app. Free with premium features.",
            "Investment app targeting young professionals {age_range}.",
            "Budgeting app with subscription model.",
        ]
    },
    "education": {
        "name": "Education (Online Courses)",
        "objectives": ["Lead Generation (Course Signups)", "Purchase Conversions"],
        "avg_order_value": (50, 500),
        "typical_ctr": (1.5, 2.5),
        "typical_cvr": (2.0, 5.0),
        "typical_cpc_meta": (0.70, 1.80),
        "typical_cpc_google": (1.00, 3.00),
        "weekly_spend_range": (2000, 8000),
        "context_templates": [
            "Online course platform. Courses priced ${price_range}.",
            "Professional certification programs.",
            "Language learning courses targeting adults.",
            "Coding bootcamp promoting career change programs.",
        ]
    },
    "food_restaurant": {
        "name": "Food & Restaurant",
        "objectives": ["Store Visits", "Online Orders", "Lead Generation (Reservations)"],
        "avg_order_value": (25, 60),
        "typical_ctr": (1.8, 3.0),
        "typical_cvr": (4.0, 8.0),
        "typical_cpc_meta": (0.30, 0.80),
        "typical_cpc_google": (0.50, 1.20),
        "weekly_spend_range": (1500, 6000),
        "context_templates": [
            "Restaurant chain with {num_locations} locations.",
            "Food delivery service targeting urban areas.",
            "Fast casual restaurant promoting new menu items.",
            "Fine dining restaurant targeting special occasions.",
        ]
    }
}

# ============================================================
# PLATFORM CONFIGURATIONS
# ============================================================

PLATFORMS = {
    "meta": {
        "name": "Meta Ads",
        "cpc_key": "typical_cpc_meta",
        "has_reach": True,
        "has_frequency": True,
        "has_impression_share": False,
    },
    "google_search": {
        "name": "Google Ads (Search)",
        "cpc_key": "typical_cpc_google",
        "has_reach": False,
        "has_frequency": False,
        "has_impression_share": True,
        "has_top_of_page": True,
    },
    "google_shopping": {
        "name": "Google Ads (Shopping)",
        "cpc_key": "typical_cpc_google",
        "has_reach": False,
        "has_frequency": False,
        "has_impression_share": True,
        "has_top_of_page": False,
    }
}

# ============================================================
# PERFORMANCE LEVEL MULTIPLIERS
# ============================================================

PERFORMANCE_LEVELS = {
    "excellent": {
        "description": "Exceeding all targets",
        "ctr_mult": (1.15, 1.35),
        "cvr_mult": (1.20, 1.45),
        "cpc_mult": (0.85, 1.00),  # Lower CPC is better
    },
    "good": {
        "description": "Meeting targets",
        "ctr_mult": (0.95, 1.10),
        "cvr_mult": (0.95, 1.10),
        "cpc_mult": (0.95, 1.10),
    },
    "declining": {
        "description": "Was good, getting worse",
        "ctr_mult": (0.75, 0.90),
        "cvr_mult": (0.70, 0.85),
        "cpc_mult": (1.10, 1.30),
    },
    "poor": {
        "description": "Below targets",
        "ctr_mult": (0.55, 0.75),
        "cvr_mult": (0.45, 0.65),
        "cpc_mult": (1.20, 1.50),
    },
    "mixed": {
        "description": "High variance, inconsistent",
        "ctr_mult": (0.70, 1.20),
        "cvr_mult": (0.60, 1.15),
        "cpc_mult": (0.90, 1.25),
    }
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def rand_range(range_tuple: tuple) -> float:
    """Generate random float within range."""
    return random.uniform(range_tuple[0], range_tuple[1])


def format_currency(value: float) -> str:
    """Format number as currency string."""
    if value >= 1000:
        return f"${value:,.0f}"
    elif value >= 100:
        return f"${value:.0f}"
    else:
        return f"${value:.2f}"


def format_percent(value: float) -> str:
    """Format number as percentage string."""
    return f"{value:.2f}%"


def format_number(value: int) -> str:
    """Format large numbers with commas."""
    return f"{value:,}"


# ============================================================
# SCENARIO GENERATOR (FIXED LOGIC)
# ============================================================

def generate_single_scenario(
    industry_key: str = None,
    platform_key: str = None,
    performance_level: str = None
) -> Dict:
    """
    Generate a single realistic marketing scenario.
    """
    
    # Select random if not specified
    if industry_key is None:
        industry_key = random.choice(list(INDUSTRIES.keys()))
    if platform_key is None:
        platform_key = random.choice(list(PLATFORMS.keys()))
    if performance_level is None:
        performance_level = random.choice(list(PERFORMANCE_LEVELS.keys()))
    
    industry = INDUSTRIES[industry_key]
    platform = PLATFORMS[platform_key]
    perf = PERFORMANCE_LEVELS[performance_level]
    
    # ============================================================
    # STEP 1: Generate base metrics from industry benchmarks
    # ============================================================
    base_ctr = rand_range(industry["typical_ctr"])
    base_cvr = rand_range(industry["typical_cvr"])
    base_cpc = rand_range(industry[platform["cpc_key"]])
    
    # ============================================================
    # STEP 2: Apply performance multipliers
    # ============================================================
    current_ctr = base_ctr * rand_range(perf["ctr_mult"])
    current_cvr = base_cvr * rand_range(perf["cvr_mult"])
    current_cpc = base_cpc * rand_range(perf["cpc_mult"])
    
    # ============================================================
    # STEP 3: Generate ad spend
    # ============================================================
    ad_spend = random.randint(
        industry["weekly_spend_range"][0],
        industry["weekly_spend_range"][1]
    )
    
    # ============================================================
    # STEP 4: Calculate derived metrics (CORRECT FORMULAS)
    # ============================================================
    # Formula: ad_spend = clicks * CPC
    # So: clicks = ad_spend / CPC
    clicks = int(ad_spend / current_cpc)
    
    # Formula: CTR = clicks / impressions * 100
    # So: impressions = clicks / (CTR / 100)
    impressions = int(clicks / (current_ctr / 100))
    
    # Formula: CVR = conversions / clicks * 100
    # So: conversions = clicks * (CVR / 100)
    conversions = int(clicks * (current_cvr / 100))
    
    # Ensure minimum conversions
    conversions = max(conversions, 8)
    
    # ============================================================
    # STEP 5: Recalculate actual rates from whole numbers
    # ============================================================
    actual_ctr = (clicks / impressions * 100) if impressions > 0 else 0
    actual_cvr = (conversions / clicks * 100) if clicks > 0 else 0
    actual_cpc = ad_spend / clicks if clicks > 0 else 0
    actual_cpa = ad_spend / conversions if conversions > 0 else 0
    
    # ============================================================
    # STEP 6: Calculate revenue and ROAS for e-commerce
    # ============================================================
    if industry["avg_order_value"][1] > 0:
        aov = rand_range(industry["avg_order_value"])
        revenue = conversions * aov
        roas = revenue / ad_spend if ad_spend > 0 else 0
    else:
        revenue = None
        roas = None
    
    # ============================================================
    # STEP 7: Build current metrics dictionary
    # ============================================================
    current_metrics = {
        "ad_spend": format_currency(ad_spend),
        "impressions": format_number(impressions),
        "clicks": format_number(clicks),
        "ctr": format_percent(actual_ctr),
        "cpc": format_currency(actual_cpc),
    }
    
    # Add Meta-specific metrics
    if platform["has_reach"]:
        reach_ratio = random.uniform(0.35, 0.50)
        reach = int(impressions * reach_ratio)
        frequency = round(impressions / reach, 2) if reach > 0 else 1
        current_metrics["reach"] = format_number(reach)
        current_metrics["frequency"] = f"{frequency:.2f}"
    
    # Add Google-specific metrics
    if platform.get("has_impression_share"):
        impression_share = random.uniform(28, 55)
        current_metrics["search_impression_share"] = format_percent(impression_share)
    
    if platform.get("has_top_of_page"):
        top_of_page = random.uniform(55, 82)
        current_metrics["top_of_page_rate"] = format_percent(top_of_page)
    
    # Add conversion metrics with appropriate label
    if "app" in industry_key:
        conversion_label = "app_installs"
    elif "ecommerce" in industry_key or "food" in industry_key:
        conversion_label = "transactions"
    else:
        conversion_label = "leads"
    
    current_metrics[conversion_label] = format_number(conversions)
    current_metrics["conversion_rate"] = format_percent(actual_cvr)
    current_metrics["cpa"] = format_currency(actual_cpa)
    
    # Add revenue/ROAS for applicable industries
    if revenue is not None:
        current_metrics["revenue"] = format_currency(revenue)
        current_metrics["roas"] = f"{roas:.2f}x"
    
    # ============================================================
    # STEP 8: Generate previous period metrics
    # ============================================================
    if performance_level == "declining":
        # Previous was significantly better
        prev_ctr_mult = random.uniform(1.25, 1.50)
        prev_cvr_mult = random.uniform(1.30, 1.55)
        prev_cpa_mult = random.uniform(0.60, 0.75)
        prev_roas_mult = random.uniform(1.30, 1.60)
    elif performance_level == "excellent":
        # Previous was slightly worse (we improved)
        prev_ctr_mult = random.uniform(0.88, 0.95)
        prev_cvr_mult = random.uniform(0.85, 0.95)
        prev_cpa_mult = random.uniform(1.08, 1.18)
        prev_roas_mult = random.uniform(0.85, 0.92)
    elif performance_level == "poor":
        # Previous was also poor or similar
        prev_ctr_mult = random.uniform(0.95, 1.15)
        prev_cvr_mult = random.uniform(0.90, 1.10)
        prev_cpa_mult = random.uniform(0.90, 1.10)
        prev_roas_mult = random.uniform(0.90, 1.10)
    else:
        # Random variation
        prev_ctr_mult = random.uniform(0.85, 1.15)
        prev_cvr_mult = random.uniform(0.85, 1.15)
        prev_cpa_mult = random.uniform(0.85, 1.15)
        prev_roas_mult = random.uniform(0.85, 1.15)
    
    previous_metrics = {
        "ctr": format_percent(actual_ctr * prev_ctr_mult),
        "conversion_rate": format_percent(actual_cvr * prev_cvr_mult),
        "cpa": format_currency(actual_cpa * prev_cpa_mult),
    }
    
    if roas is not None:
        previous_metrics["roas"] = f"{roas * prev_roas_mult:.2f}x"
    
    # ============================================================
    # STEP 9: Generate targets
    # ============================================================
    targets = {}
    
    # Target CPA (want lower)
    if performance_level in ["poor", "declining"]:
        target_cpa = actual_cpa * random.uniform(0.65, 0.80)
    else:
        target_cpa = actual_cpa * random.uniform(0.90, 1.05)
    targets["target_cpa"] = format_currency(target_cpa)
    
    # Target ROAS (want higher)
    if roas is not None:
        if performance_level in ["poor", "declining"]:
            target_roas = max(2.0, roas * random.uniform(1.30, 1.50))
        else:
            target_roas = roas * random.uniform(0.95, 1.05)
        targets["target_roas"] = f"{target_roas:.1f}x"
    
    # ============================================================
    # STEP 10: Generate context
    # ============================================================
    context_template = random.choice(industry["context_templates"])
    context = context_template.format(
        age_range=random.choice(["18-35", "25-45", "30-55", "25-54"]),
        radius=random.choice([10, 15, 20, 25]),
        season=random.choice(["spring", "summer", "fall", "winter"]),
        competitors=random.choice(["Monday.com, Asana", "HubSpot, Salesforce", "Mailchimp, Klaviyo"]),
        price=random.choice(["9.99", "14.99", "19.99"]),
        price_range="$50-$500",
        num_locations=random.choice([5, 12, 25, 50])
    )
    
    # Add performance context
    if performance_level == "declining":
        context += " Performance has declined over the past 2 weeks."
    elif performance_level == "poor":
        context += " Campaign struggling to meet targets."
    elif performance_level == "excellent":
        context += " Campaign exceeding expectations."
    
    # Select time period
    period = random.choice(["Last 7 days", "Last 14 days", "Last 30 days"])
    
    return {
        "platform": platform["name"],
        "industry": industry["name"],
        "objective": random.choice(industry["objectives"]),
        "period": period,
        "current_metrics": current_metrics,
        "previous_metrics": previous_metrics,
        "targets": targets,
        "context": context,
        "_metadata": {
            "industry_key": industry_key,
            "platform_key": platform_key,
            "performance_level": performance_level
        }
    }


def generate_scenarios(count: int = 100, balanced: bool = True) -> List[Dict]:
    """
    Generate multiple diverse scenarios.
    """
    scenarios = []
    
    if balanced:
        industries = list(INDUSTRIES.keys())
        platforms = list(PLATFORMS.keys())
        performance_levels = list(PERFORMANCE_LEVELS.keys())
        
        for i in range(count):
            industry = industries[i % len(industries)]
            platform = platforms[i % len(platforms)]
            performance = performance_levels[i % len(performance_levels)]
            
            scenario = generate_single_scenario(industry, platform, performance)
            scenarios.append(scenario)
    else:
        for _ in range(count):
            scenarios.append(generate_single_scenario())
    
    return scenarios


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("Generating 5 test scenarios...\n")
    
    test_scenarios = generate_scenarios(5)
    
    for i, scenario in enumerate(test_scenarios):
        print(f"{'='*60}")
        print(f"Scenario {i+1}: {scenario['_metadata']['performance_level'].upper()}")
        print(f"{'='*60}")
        print(f"Platform: {scenario['platform']}")
        print(f"Industry: {scenario['industry']}")
        print(f"Objective: {scenario['objective']}")
        print(f"\nCurrent Metrics:")
        for k, v in scenario['current_metrics'].items():
            print(f"  {k}: {v}")
        print(f"\nPrevious Metrics:")
        for k, v in scenario['previous_metrics'].items():
            print(f"  {k}: {v}")
        print(f"\nTargets:")
        for k, v in scenario['targets'].items():
            print(f"  {k}: {v}")
        print(f"\nContext: {scenario['context']}")
        print()