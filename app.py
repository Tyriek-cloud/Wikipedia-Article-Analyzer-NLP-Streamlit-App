# Now to define the Streamlit app
import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from urllib.parse import urljoin
from nltk.corpus import stopwords
import heapq

# Download NLTK data
nltk.download('punkt')

# Summarize text
def summarize_text(text, num_sentences=10):
    sentences = nltk.sent_tokenize(text)
    summary = " ".join(sentences[:num_sentences])
    return summary

# Extract live URLs from the references section
def extract_live_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    references_section = soup.find("span", {"id": "References"})
    if references_section:
        references = references_section.find_next("ul")
        if references:
            urls = [a['href'] for a in references.find_all('a', href=True)]
            return urls

    return []

# Extracts images
def extract_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # All image tags are called 'img'
    img_tags = soup.find_all('img')

    # Extracts image URLs
    image_urls = [urljoin(url, img['src']) for img in img_tags]

    return image_urls

# Main function
def main():
    st.title("Wikipedia Article Analyzer")

    # Sidebar for user input (if any)
    st.sidebar.header("User Input")
    url_input = st.sidebar.text_input("Enter Wikipedia URL:", "https://en.wikipedia.org/wiki/Statistics")

    # Main content
    if st.button("Analyze"):
        # Extract and summarize the text
        response = requests.get(url_input)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find("div", class_="mw-parser-output")
        paragraphs = content.find_all("p")
        full_text = "\n".join([p.text for p in paragraphs])
        summary = summarize_text(full_text)

        # Display summary
        st.subheader("Summary:")
        st.write(summary)

        # Extract live URLs from the references section
        live_urls = extract_live_urls(url_input)
        st.subheader("Live URLs from References:")
        for url in live_urls:
            st.write(url)

        # Extract images
        image_urls = extract_images(url_input)
        st.subheader("Image URLs:")
        for idx, url in enumerate(image_urls, start=1):
            st.write(url)

if __name__ == "__main__":
    main()
