"""
generate_data.py - Generate training data in batch

Usage: python3 generate_data.py
"""

import os
import json
import time
from datetime import datetime
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

from prompts import SYSTEM_PROMPT, create_user_prompt
from scenario_generator import generate_scenarios  # <-- Changed this line

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Configuration
CONFIG = {
    "model": "gpt-4o-mini",
    "max_tokens": 2500,
    "temperature": 0.7,
    "delay_between_calls": 1,
    "output_file": "outputs/training_data.jsonl",
    "checkpoint_file": "outputs/checkpoint.json",
    "num_scenarios": 100  # <-- Added this
}


def ensure_output_dir():
    """Create outputs directory if it doesn't exist."""
    os.makedirs("outputs", exist_ok=True)


def load_checkpoint() -> int:
    """Load checkpoint to resume from last position."""
    if os.path.exists(CONFIG["checkpoint_file"]):
        with open(CONFIG["checkpoint_file"], "r") as f:
            data = json.load(f)
            return data.get("last_completed", -1)
    return -1


def save_checkpoint(index: int):
    """Save current progress."""
    with open(CONFIG["checkpoint_file"], "w") as f:
        json.dump({"last_completed": index}, f)


def generate_example(scenario: dict, example_id: str) -> dict:
    """Generate a single training example."""
    
    user_prompt = create_user_prompt(scenario)
    
    response = client.chat.completions.create(
        model=CONFIG["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=CONFIG["max_tokens"],
        temperature=CONFIG["temperature"]
    )
    
    return {
        "id": example_id,
        "timestamp": datetime.now().isoformat(),
        "input": {
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": user_prompt,
            "scenario": scenario
        },
        "output": response.choices[0].message.content,
        "tokens": {
            "prompt": response.usage.prompt_tokens,
            "completion": response.usage.completion_tokens,
            "total": response.usage.total_tokens
        }
    }


def main():
    """Main generation loop."""
    
    ensure_output_dir()
    
    # Generate scenarios
    print(f"Generating {CONFIG['num_scenarios']} scenarios...")
    scenarios = generate_scenarios(CONFIG['num_scenarios'])
    total = len(scenarios)
    print(f"Generated {total} scenarios.\n")
    
    # Load checkpoint
    start_from = load_checkpoint() + 1
    
    if start_from > 0:
        print(f"Resuming from example {start_from + 1}/{total}")
    else:
        # Clear old output file if starting fresh
        if os.path.exists(CONFIG["output_file"]):
            os.remove(CONFIG["output_file"])
        print(f"Starting fresh. Generating {total} examples.")
    
    # Track totals
    total_tokens = 0
    total_cost = 0
    errors = []
    
    # Open output file in append mode
    with open(CONFIG["output_file"], "a") as f:
        
        # Progress bar
        for i in tqdm(range(start_from, total), initial=start_from, total=total, desc="Generating"):
            scenario = scenarios[i]
            example_id = f"train_{i:04d}"
            
            try:
                # Generate example
                result = generate_example(scenario, example_id)
                
                # Write to file (one JSON per line)
                f.write(json.dumps(result) + "\n")
                f.flush()
                
                # Update totals
                total_tokens += result["tokens"]["total"]
                
                # Calculate cost (gpt-4o-mini pricing)
                input_cost = (result["tokens"]["prompt"] / 1_000_000) * 0.15
                output_cost = (result["tokens"]["completion"] / 1_000_000) * 0.60
                total_cost += input_cost + output_cost
                
                # Save checkpoint
                save_checkpoint(i)
                
                # Delay to avoid rate limits
                time.sleep(CONFIG["delay_between_calls"])
                
            except Exception as e:
                errors.append({"index": i, "error": str(e)})
                print(f"\nError at example {i}: {e}")
                continue
    
    # Final summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"Examples generated: {total - start_from}")
    print(f"Total tokens used:  {total_tokens:,}")
    print(f"Total cost:         ${total_cost:.4f}")
    print(f"Output file:        {CONFIG['output_file']}")
    
    if errors:
        print(f"\nErrors encountered: {len(errors)}")
        for err in errors:
            print(f"  - Example {err['index']}: {err['error']}")


if __name__ == "__main__":
    main()