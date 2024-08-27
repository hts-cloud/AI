# Detoxification Model

This repository contains a fine-tuned model for detoxification of language models, particularly designed to reduce the toxicity in generated text.

## Usage

You can use this model to detoxify text by running the following commands:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "your-huggingface-username/trustai"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

input_text = "Your toxic input text here"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))

