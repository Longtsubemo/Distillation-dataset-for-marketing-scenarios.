import json

# Load your training data
data = []
with open('outputs/training_data.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

# Convert to ShareGPT format (what we'll use for training)
converted = []
for item in data:
    converted.append({
        "conversations": [
            {"from": "system", "value": item['input']['system_prompt']},
            {"from": "human", "value": item['input']['user_prompt']},
            {"from": "gpt", "value": item['output']}
        ]
    })

# Save
with open('outputs/train_data_colab.jsonl', 'w') as f:
    for item in converted:
        f.write(json.dumps(item) + '\n')

print(f"Converted {len(converted)} examples")
print("Saved to: outputs/train_data_colab.jsonl")