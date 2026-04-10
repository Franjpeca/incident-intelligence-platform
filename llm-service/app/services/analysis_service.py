import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import DO_SAMPLE, MAX_NEW_TOKENS, PROMPT_BASIC_FILE, TEMPERATURE, TOP_P, MODEL_ID
from app.core.model_loader import load_model
from app.core.output_parser import extract_json
from app.core.prompt_manager import build_prompt
from app.schemas.analysis_response import AnalysisResponse

_tokenizer = None
_model = None


def _load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="auto"
        )

    return _tokenizer, _model



def analyze_text(text: str) -> AnalysisResponse:
    _tokenizer, _model = load_model()

    print("[DEBUG] Analizando texto:", text)

    prompt = build_prompt(
        prompt_name=PROMPT_BASIC_FILE,
        text=text
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

    input_text = _tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = _tokenizer(input_text, return_tensors="pt").to(_model.device)

    outputs = _model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        do_sample=DO_SAMPLE
    )

    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
    output_text = _tokenizer.decode(generated_ids, skip_special_tokens=True)

    parsed = extract_json(output_text)

    return AnalysisResponse(
        summary=str(parsed["summary"]),
        category=str(parsed["category"]),
        priority=str(parsed["priority"]),
        confidence=int(parsed["confidence"])
    )