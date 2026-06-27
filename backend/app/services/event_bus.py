import json

def publish_event(channel: str, data: dict):
    print(f"[EVENT] {channel} -> {data}")
