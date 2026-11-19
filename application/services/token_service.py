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


def trim_conversation_history(history, query, model, max_tokens=4096):
    encoding = tiktoken.encoding_for_model(model)
    remaining = list(history)
    message_token_counts = [len(encoding.encode(message["content"])) for message in remaining]
    query_tokens = len(encoding.encode(query))
    available_history_tokens = max_tokens - query_tokens - MAX_RESPONSE_TOKENS - 256

    while remaining and sum(message_token_counts) > available_history_tokens:
        messages_to_remove = min(2, len(remaining))
        remaining = remaining[messages_to_remove:]
        message_token_counts = message_token_counts[messages_to_remove:]

    if available_history_tokens < 0:
        validate_token_usage(query, model, max_tokens=max_tokens - 256)

    return remaining



