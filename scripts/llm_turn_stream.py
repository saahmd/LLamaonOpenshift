#!/usr/bin/env python3
import requests
import sys
import json

agent_id = sys.argv[1]
session_id = sys.argv[2]
message = sys.argv[3]

url = f"https://llamastack-server-llama-serve.apps.cluster-bgzcw.bgzcw.sandbox942.opentlc.com/v1/agents/{agent_id}/session/{session_id}/turn"
headers = {"Content-Type": "application/json", "Accept": "application/json"}
payload = {
    "messages": [{"role": "user", "content": message, "context": "string"}],
    "stream": True,
    "tool_config": {"tool_choice": "auto"}
}

full_response = []

with requests.post(url, headers=headers, json=payload, stream=True) as r:
    r.raise_for_status()
    for line in r.iter_lines():
        if line:
            decoded = line.decode()
            print(decoded)
            full_response.append(decoded)

# Merge chunks and save to file
with open("/tmp/llm_turn_response.txt", "w") as f:
    f.write("\n".join(full_response))