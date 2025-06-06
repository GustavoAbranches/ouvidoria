from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

sentimento = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

result = sentimento("Every new day brings a chance to create joyful memories and embrace new opportunities.")
print(result)
