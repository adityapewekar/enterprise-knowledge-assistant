import tiktoken

MAX_RESPONSE_TOKENS=500

def num_tokens_from_query(query,model):
    encoding    = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(query))
    print(f"Encoding for model {model}: {encoding.name} :{num_tokens}")
    return num_tokens

def validate_token_usage(query, model, max_tokens=4096):
    prompt_tokens = num_tokens_from_query(query, model)
    total_tokens = prompt_tokens + MAX_RESPONSE_TOKENS
    if total_tokens > max_tokens:
        raise ValueError(f"Token limit exceeded: {total_tokens} tokens used, but the maximum allowed is {max_tokens}.")



