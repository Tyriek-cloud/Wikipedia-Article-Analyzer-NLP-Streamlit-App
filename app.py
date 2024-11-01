import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from urllib.parse import urljoin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download NLTK data
nltk.download('punkt')

# Global variable to hold the article text
article_text = ""

# Simple FAQ dictionary
faq = {
    "what is statistics?": "Statistics is the study of data: how to collect, summarize and interpret it.",
    "what is machine learning?": "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to learn from data.",
}

# Summarize text
def summarize_text(text, num_sentences=10):
    sentences = nltk.sent_tokenize(text)
    summary = " ".join(sentences[:num_sentences])
    return summary

# Extract images
def extract_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    image_urls = [urljoin(url, img['src']) for img in img_tags if img.has_attr('src')]
    return image_urls

# This is the function that parses the article to answer the user's question
def search_article(question):
    global article_text
    if article_text:
        sentences = nltk.sent_tokenize(article_text)
        vectorizer = TfidfVectorizer().fit_transform(sentences + [question])
        vectors = vectorizer.toarray()
        cosine_similarities = cosine_similarity(vectors[-1], vectors[:-1])

        # Get the top N sentences
        top_n = 3  # Number of responses you want
        indices = cosine_similarities.argsort()[0][-top_n:][::-1]
        responses = []

        for index in indices:
            similarity_score = cosine_similarities[0][index]
            if similarity_score > 0.1:  # Adjust threshold as needed
                responses.append(f"From the article: '{sentences[index]}'")

        if responses:
            return "\n".join(responses)

    return "I'm sorry, but I couldn't find an answer in the article."

# Categorize the user's question
def categorize_question(question):
    factual_keywords = ["what", "who", "when", "where", "how many", "define", "which", "why"]
    general_keywords = ["opinion", "suggest", "recommend", "feel", "think", "believe"]

    question_lower = question.lower()
    
    if any(keyword in question_lower for keyword in factual_keywords):
        return "factual"
    elif any(keyword in question_lower for keyword in general_keywords):
        return "general"
    else:
        return "other"

# Handle user question
def handle_user_question(user_question):
    # Normalize the question to improve matching
    normalized_question = user_question.lower().strip()

    # Check if the question is in the FAQ
    if normalized_question in faq:
        return faq[normalized_question]

    # Proceed with the existing logic if not found in FAQ
    question_type = categorize_question(user_question)
    
    if question_type == "factual":
        return search_article(user_question)
    elif question_type == "general":
        # Replace this with your Wit.ai call if needed
        return "I'm currently unable to process general inquiries. Please ask a factual question."
    else:
        return "I couldn't categorize your question. Please ask something specific."

# Main function
def main():
    st.title("Wikipedia Article Analyzer")

    # Sidebar for user input (if any)
    st.sidebar.header("User Input")
    url_input = st.sidebar.text_input("Enter Wikipedia URL:", "https://en.wikipedia.org/wiki/Statistics")

    # Main content
    if st.button("Analyze"):
        global article_text
        try:
            response = requests.get(url_input)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find("div", class_="mw-parser-output")
            paragraphs = content.find_all("p")
            full_text = "\n".join([p.text for p in paragraphs])
            article_text = full_text
            summary = summarize_text(full_text)

            st.subheader("Summary:")
            st.write(summary)

            image_urls = extract_images(url_input)
            st.subheader("Image URLs:")
            for idx, url in enumerate(image_urls, start=1):
                st.image(url, caption=f"Image {idx}", use_column_width=True)
                st.write(url)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    # User's method to talk to the chatbot
    st.sidebar.header("Beep Boop: Talk with me")
    user_question = st.sidebar.text_input("Ask a question about the article:")

    if user_question:
        response = handle_user_question(user_question)
        st.sidebar.write("Bot:", response)

if __name__ == "__main__":
    main()
