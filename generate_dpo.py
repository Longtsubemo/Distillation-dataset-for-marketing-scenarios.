import json
import random

# Load your training data
data = []
with open('outputs/training_data.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

def create_rejected(chosen):
    """Create a bad version of the response"""
    methods = ['truncate', 'vague', 'no_plan']
    method = random.choice(methods)
    
    if method == 'truncate':
        # Cut off at 30-40%
        cut = len(chosen) * random.randint(30, 40) // 100
        return chosen[:cut] + "\n\n[Response incomplete]"
    
    elif method == 'vague':
        return """The campaign has some areas that could be improved.

I recommend:
1. Look at the metrics
2. Make some adjustments
3. Monitor results

Let me know if you need more help."""
    
    else:  # no_plan
        if "## STRATEGIC PLAN" in chosen:
            return chosen.split("## STRATEGIC PLAN")[0].strip()
        return chosen[:len(chosen)//2]

# Create DPO pairs
dpo_data = []
for item in data:
    prompt = f"{item['input']['system_prompt']}\n\n{item['input']['user_prompt']}"
    chosen = item['output']
    rejected = create_rejected(chosen)
    
    dpo_data.append({
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected
    })

# Save
with open('outputs/dpo_data.jsonl', 'w') as f:
    for item in dpo_data:
        f.write(json.dumps(item) + '\n')

print(f"Created {len(dpo_data)} DPO pairs")
print("Saved to: outputs/dpo_data.jsonl")