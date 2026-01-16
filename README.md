# Marketing Distillation

Synthetic dataset generation for fine-tuning smaller LLMs on marketing performance analysis.

Uses GPT-4o-mini as the teacher model to generate training data for distilling marketing analysis capabilities into smaller, deployable models.

## What It Does

Generates training examples where the model:
1. Analyzes marketing metrics (Meta Ads, Google Ads)
2. Identifies performance issues and root causes
3. Creates actionable strategic plans

## Project Structure

```
├── prompts.py              # System prompt & user prompt templates
├── scenarios.py            # Sample marketing scenarios
├── scenario_generator.py   # Random scenario generation
├── generate_one.py         # Generate single example (for testing)
├── generate_data.py        # Batch generation (100+ examples)
├── generate_dpo.py         # Create DPO preference pairs
├── convert_for_collab.py   # Convert to ShareGPT format for training
└── outputs/                # Generated datasets
```

## Setup

```bash
# Clone
git clone https://github.com/Longtsubemo/marketing_distillation.git
cd marketing_distillation

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Usage

**Test API connection:**
```bash
python test_api.py
```

**Generate single example:**
```bash
python generate_one.py
```

**Generate full dataset (100 examples):**
```bash
python generate_data.py
```

**Create DPO pairs:**
```bash
python generate_dpo.py
```

**Convert for fine-tuning:**
```bash
python convert_for_collab.py
```

## Output Formats

| File | Format | Use Case |
|------|--------|----------|
| `training_data.jsonl` | Raw with metadata | Analysis, debugging |
| `train_data_colab.jsonl` | ShareGPT format | SFT fine-tuning |
| `dpo_data.jsonl` | Prompt/chosen/rejected | DPO training |

## Example Scenario

```python
{
    "platform": "Meta Ads",
    "industry": "E-commerce (Women's Fashion)",
    "objective": "Purchase Conversions",
    "current_metrics": {
        "ad_spend": "$8,500",
        "roas": "1.74x",
        "cpa": "$54.49",
        ...
    },
    "targets": {
        "target_roas": "2.5x",
        "target_cpa": "$45"
    }
}
```

## Cost Estimate

Using GPT-4o-mini:
- ~$0.01-0.02 per example
- 100 examples ≈ $1-2

## License

MIT