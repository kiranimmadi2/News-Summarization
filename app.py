import streamlit as st
import requests
import pandas as pd
import os
from utils import text_to_hindi_speech

# Update this if your API runs on a different address or port
API_URL = "http://localhost:8000"

def fetch_analysis(company_name, days):
    """
    Fetch sentiment analysis from the API.
    """
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            json={"company_name": company_name, "days": days}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching analysis: {str(e)}")
        return None

def main():
    st.title("Company Sentiment Analysis")
    st.write("Analyze news sentiment for any company.")

    # User inputs
    company_name = st.text_input("Enter company name (e.g., 'Tesla')")
    days = st.slider("Number of days to analyze", 1, 30, 7)

    if st.button("Analyze"):
        if company_name:
            with st.spinner("Analyzing..."):
                report = fetch_analysis(company_name, days)

                # If the API returned a valid report
                if report and 'analysis' in report:
                    st.subheader("Analysis Summary")

                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    avg_polarity = report['analysis'].get('average_polarity', 0)
                    avg_subjectivity = report['analysis'].get('average_subjectivity', 0)
                    article_count = report['analysis'].get('article_count', 0)

                    with col1:
                        st.metric("Average Polarity", f"{avg_polarity:.2f}")
                    with col2:
                        st.metric("Average Subjectivity", f"{avg_subjectivity:.2f}")
                    with col3:
                        st.metric("Article Count", article_count)

                    # Display articles
                    if 'articles' in report and report['articles']:
                        st.subheader("News Articles")
                        df = pd.DataFrame(report['articles'])

                        # Display only certain columns if they exist
                        display_cols = []
                        for col in ["title", "date", "media"]:
                            if col in df.columns:
                                display_cols.append(col)

                        if not df.empty and display_cols:
                            st.dataframe(df[display_cols])
                        else:
                            st.info("No articles found or columns missing.")

                        # Generate and play Hindi summary
                        summary_text = (
                            f"कंपनी {company_name} के लिए {article_count} समाचार मिले हैं। "
                            f"औसत पोलैरिटी {avg_polarity:.2f}, औसत सब्जेक्टिविटी {avg_subjectivity:.2f}"
                        )
                        audio_file = text_to_hindi_speech(summary_text, "summary.mp3")

                        st.subheader("Hindi Audio Summary")
                        st.audio(audio_file)

                        # Optional: Cleanup the audio file after playing
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                    else:
                        st.warning("No articles found for the given company.")
                else:
                    st.error("Failed to get analysis results.")
        else:
            st.warning("Please enter a company name.")

if __name__ == "__main__":
    main()
