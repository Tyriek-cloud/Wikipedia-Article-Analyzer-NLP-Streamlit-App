# Wikipedia-Article-Analyzer-NLP-Streamlit-App
Wikipedia Article Analyzer: https://wikipedia-article-analyzer-nlp-app-app-ggh9suyycuva5j6wybe5pa.streamlit.app/

![image](https://github.com/Tyriek-cloud/Wikipedia-Article-Analyzer-NLP-Streamlit-App/assets/62261407/de187679-b57b-4faa-9928-f4e316a25652)

This project is designed to scrape articles from Wikipedia. By default, the Streamlit application will display the Wikipedia Statistics page (https://en.wikipedia.org/wiki/Statistics). The user will have the option to insert their own Wikipedia URLs. The end goal is to use Natural Language Processing to create a summary (with an emphasis on important and easily digestable details) from Wikipedia articles and display important images/pictures/graphics from each of the articles.

# Summary

The application generates a summary of 10+ sentences. The sentences are intended to pull crucial facts about the article. As opposed to reading an entire article, this can save a user time.

# Image URLs

This will pull in links to images from the Wikipedia article. These URLs are clickable and will generate a seperate webpage. The images can then be copied for personal use.

# IMPORTANT DISCLAIMERS

The structure of the Wikiepedia article may impact whether a summary is actually generated. Image URLs are always pulled in.

The base code for this app was written in Google Colab: https://colab.research.google.com/drive/1RDKGcidcVlpzs2kT-9SB0WKN2NaA4sft?usp=sharing. Mid-project, I realized that the "spacy" library would be compatible on Google Colab but not on Streamlit.io.

So I researched solutions to modify the tokenization and other features of the application.
