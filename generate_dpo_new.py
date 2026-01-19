import json
import random

# Load your training data
data = []
with open('outputs/training_data.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

print(f"Loaded {len(data)} training examples")

# Different rejection strategies
def create_truncated(chosen):
    cut = len(chosen) * random.randint(25, 40) // 100
    last_period = chosen[:cut].rfind('.')
    if last_period > cut // 2:
        cut = last_period + 1
    return chosen[:cut] + "\n\n[Response incomplete]"

def create_vague(chosen):
    vague_responses = [
        """The campaign shows mixed results.

Recommendations:
1. Review the metrics
2. Make adjustments as needed
3. Continue monitoring

Let me know if you need anything else.""",
        
        """Looking at the data, there are some areas for improvement.

I suggest:
1. Optimize the campaigns
2. Test different approaches
3. Track performance

Hope this helps!""",
        
        """The performance could be better.

Action items:
1. Analyze what's working
2. Fix what's not
3. Keep testing

Feel free to ask follow-up questions.""",
    ]
    return random.choice(vague_responses)

def create_no_plan(chosen):
    if "## STRATEGIC PLAN" in chosen:
        return chosen.split("## STRATEGIC PLAN")[0].strip() + "\n\nI hope this analysis helps!"
    elif "STRATEGIC PLAN" in chosen:
        return chosen.split("STRATEGIC PLAN")[0].strip() + "\n\nI hope this analysis helps!"
    return chosen[:len(chosen)//2]

def create_no_analysis(chosen):
    if "## STRATEGIC PLAN" in chosen:
        idx = chosen.find("## STRATEGIC PLAN")
        return "The campaign needs some work.\n\n" + chosen[idx:]
    return "Here are my recommendations:\n" + chosen[len(chosen)//2:]

def create_wrong_focus(chosen, scenario):
    platform = scenario.get('platform', 'the platform')
    return f"""## PERFORMANCE ANALYSIS

Looking at the {platform} campaign, the impressions and reach look reasonable. The campaign is running and generating some activity.

## STRATEGIC PLAN FOR RESEARCH AGENT

1. **Continue Monitoring**: Keep watching the metrics daily.

2. **Maintain Current Strategy**: The campaign is running, so no major changes needed.

3. **Standard Optimization**: Apply general best practices.

4. **Regular Reporting**: Set up weekly reports.

The campaign should be fine with these standard optimizations."""

# Create DPO pairs - 2 rejection types per example = 200 pairs
dpo_data = []

for item in data:
    prompt = f"{item['input']['system_prompt']}\n\n{item['input']['user_prompt']}"
    chosen = item['output']
    scenario = item['input']['scenario']
    
    rejection_functions = [
        ('truncated', create_truncated),
        ('vague', create_vague),
        ('no_plan', create_no_plan),
        ('no_analysis', create_no_analysis),
        ('wrong_focus', lambda c: create_wrong_focus(c, scenario)),
    ]
    
    # Pick 2 different rejection types
    selected = random.sample(rejection_functions, 2)
    
    for rejection_type, rejection_fn in selected:
        rejected = rejection_fn(chosen)
        
        dpo_data.append({
            "prompt": prompt,
            "chosen": chosen,
            "rejected": rejected,
            "rejection_type": rejection_type
        })

random.shuffle(dpo_data)

# Save
with open('outputs/dpo_data_200.jsonl', 'w') as f:
    for item in dpo_data:
        save_item = {
            "prompt": item["prompt"],
            "chosen": item["chosen"],
            "rejected": item["rejected"]
        }
        f.write(json.dumps(save_item) + '\n')

# Print stats
print(f"\n✅ Created {len(dpo_data)} DPO pairs")
print(f"   Saved to: outputs/dpo_data_200.jsonl")

from collections import Counter
type_counts = Counter(item['rejection_type'] for item in dpo_data)
print(f"\n📊 Rejection types:")
for rtype, count in sorted(type_counts.items()):
    print(f"   {rtype}: {count}")