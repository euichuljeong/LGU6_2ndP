import pandas as pd
import re

# ✔️ M3U 파싱 함수 정의
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

# 🇰🇷 한국 전용 채널 파일 변환
m3u_file_kr = "kr.m3u"
df_korea = parse_m3u_to_df(m3u_file_kr)
df_korea.to_csv("iptv_channels_korea.csv", index=False)

print("✅ 한국 채널 CSV로 저장 완료 → iptv_channels_korea.csv")
