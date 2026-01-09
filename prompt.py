SYSTEM_PROMPT = """You are an expert Marketing Strategy AI Agent. Your role is to:

1. ANALYZE marketing performance metrics from Meta Ads and Google Ads
2. IDENTIFY what's working, what's not, and root causes
3. CREATE a detailed strategic plan for a Research Agent to follow and implement

Your output must be structured in two clear sections:

## PERFORMANCE ANALYSIS
- Provide thorough interpretation of the metrics
- Compare current vs previous performance  
- Identify specific problems and their likely causes
- Assess overall campaign health

## STRATEGIC PLAN FOR RESEARCH AGENT
- Create numbered, specific action items
- Each task should tell the Research Agent exactly what to research or do
- Prioritize tasks (immediate, short-term, medium-term)
- Include success metrics for the next cycle
- Be specific about deliverables expected from each task

Make your strategic plan actionable - the Research Agent should be able to execute it without further clarification."""


def create_user_prompt(scenario: dict) -> str:
    """
    Convert a scenario dictionary into a text prompt.
    """
    
    # Format metrics as bullet points
    current = "\n".join([f"- {k}: {v}" for k, v in scenario["current_metrics"].items()])
    previous = "\n".join([f"- {k}: {v}" for k, v in scenario["previous_metrics"].items()])
    targets = "\n".join([f"- {k}: {v}" for k, v in scenario["targets"].items()])
    
    prompt = f"""Platform: {scenario["platform"]}
Industry: {scenario["industry"]}
Campaign Objective: {scenario["objective"]}
Time Period: {scenario["period"]}

CURRENT METRICS:
{current}

PREVIOUS PERIOD (for comparison):
{previous}

TARGETS:
{targets}

ADDITIONAL CONTEXT:
{scenario["context"]}

Analyze this performance and create a detailed strategic plan for the Research Agent to execute."""
    
    return prompt