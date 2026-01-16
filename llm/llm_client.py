# llm/llm_client.py

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class HuggingFaceLLMWrapper:
    def __init__(self, model_name="google/flan-t5-small"):
        print(f"Loading HF model: {model_name} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.device = torch.device("cpu")
        self.model.to(self.device)
        self.model.eval()

    def generate(self, prompt, max_new_tokens=100):
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


# ------------------------
# LLM utility function
# ------------------------
hf_model = HuggingFaceLLMWrapper(model_name="google/flan-t5-small")

def parse_user_intent(user_text: str) -> dict:
    """
    Uses LLM to parse user input and extract:
    - suggested domain: news | movies | products
    - keywords for semantic search
    Returns dict: {"domain": str, "keywords": str}
    """
    prompt = (
        "Extract the content type and main keywords from this user request. "
        "Return JSON like {\"domain\": \"news/movies/products\", \"keywords\": \"...\"}.\n"
        f"User request: {user_text}"
    )
    response = hf_model.generate(prompt, max_new_tokens=100)
    
    # Attempt to parse response as JSON
    import json
    try:
        parsed = json.loads(response)
        # Basic validation
        domain = parsed.get("domain", "news").lower()
        if domain not in ["news", "movies", "products"]:
            domain = "news"
        keywords = parsed.get("keywords", user_text)
        return {"domain": domain, "keywords": keywords}
    except:
        # Fallback if LLM fails
        return {"domain": "news", "keywords": user_text}


if __name__ == "__main__":
    print("LLM Client Demo")
    while True:
        user_input = input("\nEnter text: ")
        if user_input.lower() == "exit":
            break
        print(parse_user_intent(user_input))
