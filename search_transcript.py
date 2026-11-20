import json

transcript_path = r'C:\Users\AkashDeep\.gemini\antigravity\brain\9cc2b58b-563a-426d-91ff-76790ac91454\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        content = data.get('content', '')
        for phrase in ['vertical', 'black box', 'black boxes', 'unwanted', 'incorrect text']:
            if phrase in content.lower():
                print(f'Line {i} ({data.get("type")}): matched {phrase} -> {content[:100]}...')
                break
