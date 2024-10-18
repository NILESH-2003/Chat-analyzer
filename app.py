import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# Set font family for plots
rcParams['font.family'] = 'Arial'

# Custom CSS for styling
st.markdown("""
<style>
h1 {
    color: #4CAF50;
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
}
h2 {
    color: #007ACC;
    text-align: center;
    font-size: 2em;
    margin-top: 20px;
    margin-bottom: 10px;
}
h3 {
    color: #333;
    font-size: 1.5em;
    font-weight: bold;
}
h5 {
    color: black;
}
.sidebar .sidebar-content {
    background-color: #F7F7F7;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Whatsapp Chat Analyzer")

# File uploader for chat data
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")

        # Create four columns for stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>{num_messages}</h3>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>Total Messages</h5>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>{words}</h3>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>Total Words</h5>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>{num_media_messages}</h3>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>Media Shared</h5>", unsafe_allow_html=True)

        with col4:
            st.markdown(f"<h3 style='text-align: center; font-weight: bold;'>{num_links}</h3>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>Links Shared</h5>", unsafe_allow_html=True)

        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Most Busy Users
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                emoji_labels = emoji_df['Emoji'].head().apply(lambda x: str(x))
                ax.pie(emoji_df['Count'].head(), labels=emoji_labels, autopct="%0.2f%%")
                ax.axis('equal')
                st.pyplot(fig)
            else:
                st.write("No emojis found.")

