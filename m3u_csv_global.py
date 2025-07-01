import pandas as pd
import re

def parse_m3u_to_df(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    entries = []
    for i in range(0, len(lines), 2):
        if lines[i].startswith('#EXTINF') and i + 1 < len(lines):
            meta = lines[i]
            url = lines[i + 1].strip()

            name_match = re.search(r',(.+)', meta)
            group_match = re.search(r'group-title="(.*?)"', meta)

            channel_name = name_match.group(1).strip() if name_match else "Unknown"
            group_title = group_match.group(1).strip() if group_match else "Undefined"

            entries.append({
                "channel_name": channel_name,
                "group_title": group_title,
                "url": url
            })

    return pd.DataFrame(entries)

# 🌍 전 세계 채널
m3u_file_global = "index.m3u"
df_global = parse_m3u_to_df(m3u_file_global)
df_global.to_csv("iptv_channels_global.csv", index=False)
print("✅ 전 세계 채널 저장 완료 → iptv_channels_global.csv")
