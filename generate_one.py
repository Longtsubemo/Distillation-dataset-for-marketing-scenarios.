import os
from openai import OpenAI
from dotenv import load_dotenv

from prompt import SYSTEM_PROMPT, create_user_prompt
from scenarios import scenario_1

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def generate_one_example(scenario: dict, model: str = "gpt-4o-mini") -> dict:
    """
    Generate a single training example from a scenario.
    
    Returns dict with input, output, and token usage.
    """
    
    # Create the user prompt from scenario
    user_prompt = create_user_prompt(scenario)
    
    # Call the API
    print(f"Calling {model}...")
    print("-" * 50)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=2500,
        temperature=0.7
    )
    
    # Extract the response
    output = response.choices[0].message.content
    
    # Get token usage
    tokens = {
        "prompt": response.usage.prompt_tokens,
        "completion": response.usage.completion_tokens,
        "total": response.usage.total_tokens
    }
    
    return {
        "input": {
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": user_prompt,
            "scenario": scenario
        },
        "output": output,
        "tokens": tokens
    }


if __name__ == "__main__":
    
    # Generate one example
    result = generate_one_example(scenario_1)
    
    # Print the output
    print("\n" + "=" * 60)
    print("TEACHER MODEL OUTPUT")
    print("=" * 60 + "\n")
    print(result["output"])
    
    # Print token usage
    print("\n" + "=" * 60)
    print("TOKEN USAGE")
    print("=" * 60)
    print(f"Prompt tokens:     {result['tokens']['prompt']}")
    print(f"Completion tokens: {result['tokens']['completion']}")
    print(f"Total tokens:      {result['tokens']['total']}")
    
    # Estimate cost (gpt-4o-mini pricing)
    # Input: $0.15 per 1M tokens, Output: $0.60 per 1M tokens
    input_cost = (result['tokens']['prompt'] / 1_000_000) * 0.15
    output_cost = (result['tokens']['completion'] / 1_000_000) * 0.60
    total_cost = input_cost + output_cost
    
    print(f"\nEstimated cost: ${total_cost:.4f}")
    print(f"Cost for 100 examples: ~${total_cost * 100:.2f}")

