scenario_1 = {
    "platform": "Meta Ads",
    "industry": "E-commerce (Women's Fashion)",
    "objective": "Purchase Conversions",
    "period": "Last 7 days",
    
    "current_metrics": {
        "ad_spend": "$8,500",
        "impressions": "620,000",
        "reach": "245,000",
        "clicks": "7,440",
        "ctr": "1.20%",
        "cpc": "$1.14",
        "purchases": "156",
        "conversion_rate": "2.10%",
        "cpa": "$54.49",
        "revenue": "$14,820",
        "roas": "1.74x",
        "frequency": "2.53"
    },
    
    "previous_metrics": {
        "ctr": "1.85%",
        "cpa": "$38.20",
        "roas": "2.95x",
        "frequency": "1.80"
    },
    
    "targets": {
        "target_roas": "2.5x",
        "target_cpa": "$45"
    },
    
    "context": "Campaign running for 6 weeks. Using 4 ad creatives. Targeting women 25-45 interested in fashion."
}


# Scenario 2: Google Ads - Very Poor Performance (Needs Urgent Fix)
scenario_2 = {
    "platform": "Google Ads (Search)",
    "industry": "B2B SaaS (Project Management Software)",
    "objective": "Lead Generation (Demo Requests)",
    "period": "Last 14 days",
    
    "current_metrics": {
        "ad_spend": "$6,200",
        "impressions": "45,000",
        "clicks": "890",
        "ctr": "1.98%",
        "cpc": "$6.97",
        "landing_page_views": "845",
        "demo_requests": "12",
        "conversion_rate": "1.35%",
        "cost_per_lead": "$516.67",
        "search_impression_share": "34%",
        "top_of_page_rate": "62%"
    },
    
    "previous_metrics": {
        "ctr": "2.45%",
        "cpc": "$5.20",
        "conversion_rate": "2.80%",
        "cost_per_lead": "$185.71"
    },
    
    "targets": {
        "target_cpl": "$200",
        "target_conversion_rate": "3%"
    },
    
    "context": "Targeting keywords: project management software, team collaboration tool, best PM software. Main competitors: Monday.com, Asana, ClickUp."
}


# Scenario 3: Meta Ads - Good Performance (Model should recognize success)
scenario_3 = {
    "platform": "Meta Ads",
    "industry": "Local Service (Dental Clinic)",
    "objective": "Lead Generation (Appointment Bookings)",
    "period": "Last 30 days",
    
    "current_metrics": {
        "ad_spend": "$2,400",
        "impressions": "185,000",
        "reach": "62,000",
        "clicks": "2,960",
        "ctr": "1.60%",
        "cpc": "$0.81",
        "leads": "89",
        "conversion_rate": "3.01%",
        "cost_per_lead": "$26.97",
        "booked_appointments": "34",
        "lead_to_appointment_rate": "38%",
        "cost_per_appointment": "$70.59"
    },
    
    "previous_metrics": {
        "ctr": "1.52%",
        "cost_per_lead": "$29.50",
        "lead_to_appointment_rate": "35%"
    },
    
    "targets": {
        "target_cpl": "$35",
        "target_cost_per_appointment": "$80"
    },
    
    "context": "Targeting 15-mile radius around clinic. Ages 25-65. Promoting teeth whitening and general checkups. Using before/after image ads."
}


# Scenario 4: Google Ads - Scaling Problem (Was good, increased budget, now worse)
scenario_4 = {
    "platform": "Google Ads (Shopping + Search)",
    "industry": "E-commerce (Electronics)",
    "objective": "Online Sales",
    "period": "Last 7 days",
    
    "current_metrics": {
        "ad_spend": "$15,000",
        "impressions": "1,200,000",
        "clicks": "28,000",
        "ctr": "2.33%",
        "cpc": "$0.54",
        "transactions": "420",
        "conversion_rate": "1.50%",
        "cpa": "$35.71",
        "revenue": "$58,800",
        "roas": "3.92x",
        "search_impression_share": "45%"
    },
    
    "previous_metrics": {
        "ad_spend": "$8,000",
        "ctr": "2.85%",
        "conversion_rate": "1.95%",
        "cpa": "$28.57",
        "roas": "4.75x"
    },
    
    "targets": {
        "target_roas": "3.5x",
        "monthly_revenue_goal": "$300,000"
    },
    
    "context": "Attempting to scale from $8k to $15k weekly spend. Performance declined with increased budget. Selling smartphones, laptops, accessories."
}


# Scenario 5: Meta Ads - New Campaign (Limited data, needs direction)
scenario_5 = {
    "platform": "Meta Ads",
    "industry": "Mobile App (Fitness/Workout)",
    "objective": "App Installs + In-App Purchases",
    "period": "First 7 days of campaign",
    
    "current_metrics": {
        "ad_spend": "$3,500",
        "impressions": "520,000",
        "reach": "280,000",
        "clicks": "8,840",
        "ctr": "1.70%",
        "cpc": "$0.40",
        "app_installs": "1,240",
        "cost_per_install": "$2.82",
        "day_1_retention": "32%",
        "trial_starts": "186",
        "trial_rate": "15%",
        "purchases": "28",
        "purchase_rate": "2.26%",
        "revenue": "$840"
    },
    
    "previous_metrics": {
        "note": "New campaign - no previous data available"
    },
    
    "targets": {
        "target_cpi": "$2.50",
        "target_trial_rate": "20%",
        "target_d1_retention": "40%"
    },
    
    "context": "New fitness app launch. Subscription model: $9.99/month or $59.99/year. Targeting health-conscious users 18-45. Testing 6 different video ad creatives."
}


# Collect all scenarios into a list for easy processing
ALL_SCENARIOS = [
    scenario_1,
    scenario_2,
    scenario_3,
    scenario_4,
    scenario_5,
]