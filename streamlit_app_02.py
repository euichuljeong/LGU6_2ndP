import streamlit as st
import pandas as pd
import altair as alt

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("연령대별_IPTV_채널_매핑.csv")
    return df

df = load_data()

# 연령대 선택
age_groups = df['age_group'].dropna().unique()
selected_age = st.selectbox("👤 연령대를 선택하세요", sorted(age_groups))

# 해당 연령대 필터링
df_age = df[df['age_group'] == selected_age]

# 장르 필터링 옵션
genres = df_age['genres'].dropna().unique()
selected_genres = st.multiselect("🎬 선호 장르를 선택하세요", sorted(genres), default=list(genres))

df_filtered = df_age[df_age['genres'].isin(selected_genres)]

# 시청횟수 상위 10개 채널 시각화
st.subheader(f"📈 [{selected_age}] 인기 IPTV 채널 (시청횟수 기준)")
top_channels = df_filtered.groupby('channel_name')['watch_count'].sum().nlargest(10).reset_index()

chart = alt.Chart(top_channels).mark_bar().encode(
    x=alt.X('watch_count:Q', title='시청 횟수'),
    y=alt.Y('channel_name:N', sort='-x', title='채널명'),
    tooltip=['channel_name', 'watch_count']
).properties(height=400)

st.altair_chart(chart, use_container_width=True)

# 영상 재생 기능
st.subheader("📺 채널 상세 리스트 및 영상 재생")
for idx, row in df_filtered[['channel_name', 'genres', 'avg_rating', 'url']].sort_values(by='avg_rating', ascending=False).iterrows():
    st.markdown(f"**{row['channel_name']}** | 장르: {row['genres']} | 평점: {row['avg_rating']:.2f}")
    if st.button(f"▶️ {row['channel_name']} 재생", key=row['url']):
        st.markdown(
            f"""
            <video width="100%" height="400" controls autoplay>
              <source src="{row['url']}" type="application/x-mpegURL">
              지원되지 않는 형식입니다.
            </video>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")
