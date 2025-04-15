from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

import joblib
import numpy as np
import pandas as pd
import nltk
import re
import pickle
import textstat
import string
import unicodedata


######## App Configuration and Setup #########
# Download necessary NLTK resources
nltk.download('punkt_tab')
# Load the pre-fitted models (adjust the file paths as needed)
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')
pca_model = joblib.load('pca_model.joblib')
rf_model = joblib.load('best_rf_model.pkl') # Update as needed per your project structure
##############################################
def setup_input_articles():
    
        
    title1 = "MICHELLE OBAMA Breaks Church Rules Wearing Revealing Top Into Siena Cathedral"
    text1 = """

    MOSCOW Reuters - The U.S. embassy in Moscow accused Russian authorities on Monday of barring diplomatic staff from a property on the outskirts of Moscow, after having earlier agreed to grant access until midday on Tuesday for them to retrieve belongings. A Russian foreign ministry official, quoted by state news agency RIA, said the U.S. embassy had sent in its trucks without first obtaining permits which, the official said, are required by law because the property is in a conservation area.  The property, in a picturesque spot on a bend in the Moskva river northwest of the capital, is leased by the U.S. embassy for its staff to use for recreation.  Moscow has said it is taking it back as part of retaliatory measures after Washington approved a fresh round of sanctions against Russia. A Reuters TV cameraman outside the country residence, known in Russian as a dacha, saw five vehicles with diplomatic license plates, including a truck, arrive at the site. He said they were denied entry. An embassy spokeswoman said In line with the Russian government notification, the U.S. Mission to Russia was supposed to have access to our dacha until noon on Aug. 1.  We have not had access all day today or yesterday, she said. We refer you to the Russian government to explain why not. The Russian foreign ministry official, who was not identified, said the Americans were to blame for failing to obtain the necessary permits. To accuse Russia of blocking access amounts to a pre-meditated provocation, RIA news agency cited the official as saying.  
    """
    title2 = "MICHELLE OBAMA Breaks Church Rules Wearing Revealing Top Into Siena Cathedral"
    text2 = """

    MOSCOW Reuters - The U.S. embassy in Moscow accused Russian authorities on Monday of barring diplomatic staff from a property on the outskirts of Moscow, after having earlier agreed to grant access until midday on Tuesday for them to retrieve belongings. A Russian foreign ministry official, quoted by state news agency RIA, said the U.S. embassy had sent in its trucks without first obtaining permits which, the official said, are required by law because the property is in a conservation area.  The property, in a picturesque spot on a bend in the Moskva river northwest of the capital, is leased by the U.S. embassy for its staff to use for recreation.  Moscow has said it is taking it back as part of retaliatory measures after Washington approved a fresh round of sanctions against Russia. A Reuters TV cameraman outside the country residence, known in Russian as a dacha, saw five vehicles with diplomatic license plates, including a truck, arrive at the site. He said they were denied entry. An embassy spokeswoman said In line with the Russian government notification, the U.S. Mission to Russia was supposed to have access to our dacha until noon on Aug. 1.  We have not had access all day today or yesterday, she said. We refer you to the Russian government to explain why not. The Russian foreign ministry official, who was not identified, said the Americans were to blame for failing to obtain the necessary permits. To accuse Russia of blocking access amounts to a pre-meditated provocation, RIA news agency cited the official as saying.  
    """
    title3 = "MICHELLE OBAMA Breaks Church Rules Wearing Revealing Top Into Siena Cathedral"
    text3 = """

    MOSCOW Reuters - The U.S. embassy in Moscow accused Russian authorities on Monday of barring diplomatic staff from a property on the outskirts of Moscow, after having earlier agreed to grant access until midday on Tuesday for them to retrieve belongings. A Russian foreign ministry official, quoted by state news agency RIA, said the U.S. embassy had sent in its trucks without first obtaining permits which, the official said, are required by law because the property is in a conservation area.  The property, in a picturesque spot on a bend in the Moskva river northwest of the capital, is leased by the U.S. embassy for its staff to use for recreation.  Moscow has said it is taking it back as part of retaliatory measures after Washington approved a fresh round of sanctions against Russia. A Reuters TV cameraman outside the country residence, known in Russian as a dacha, saw five vehicles with diplomatic license plates, including a truck, arrive at the site. He said they were denied entry. An embassy spokeswoman said In line with the Russian government notification, the U.S. Mission to Russia was supposed to have access to our dacha until noon on Aug. 1.  We have not had access all day today or yesterday, she said. We refer you to the Russian government to explain why not. The Russian foreign ministry official, who was not identified, said the Americans were to blame for failing to obtain the necessary permits. To accuse Russia of blocking access amounts to a pre-meditated provocation, RIA news agency cited the official as saying.  
    """

    title4 = "MICHELLE OBAMA Breaks Church Rules Wearing Revealing Top Into Siena Cathedral"
    text4 = """

    MOSCOW Reuters - The U.S. embassy in Moscow accused Russian authorities on Monday of barring diplomatic staff from a property on the outskirts of Moscow, after having earlier agreed to grant access until midday on Tuesday for them to retrieve belongings. A Russian foreign ministry official, quoted by state news agency RIA, said the U.S. embassy had sent in its trucks without first obtaining permits which, the official said, are required by law because the property is in a conservation area.  The property, in a picturesque spot on a bend in the Moskva river northwest of the capital, is leased by the U.S. embassy for its staff to use for recreation.  Moscow has said it is taking it back as part of retaliatory measures after Washington approved a fresh round of sanctions against Russia. A Reuters TV cameraman outside the country residence, known in Russian as a dacha, saw five vehicles with diplomatic license plates, including a truck, arrive at the site. He said they were denied entry. An embassy spokeswoman said In line with the Russian government notification, the U.S. Mission to Russia was supposed to have access to our dacha until noon on Aug. 1.  We have not had access all day today or yesterday, she said. We refer you to the Russian government to explain why not. The Russian foreign ministry official, who was not identified, said the Americans were to blame for failing to obtain the necessary permits. To accuse Russia of blocking access amounts to a pre-meditated provocation, RIA news agency cited the official as saying.  
    """
    d = {title1:text1,title2:text2,title3:text3,title4:text4}
    with open("article_text.pkl", "wb") as file:
        pickle.dump(d, file)
        
    return
    

# Define function to clean text
def clean_text(text, lower_text: bool = False, remove_whitespace: bool = False, fix_encoding: bool = True, tokenize: bool = False):
    
    if fix_encoding:
        # Normalize unicode characters (NFKC helps resolve many encoding issues)
        text = unicodedata.normalize('NFKC', text)
        
        # Fix common encoding artifacts
        replacements = {
            'â€˜': "'",
            'â€™': "'",
            'â€œ': '"',
            'â€': '"',
            'â€“': '-',
            'â€”': '-',
            'â€': '"'
        }
        for wrong, correct in replacements.items():
            text = text.replace(wrong, correct)
    else: pass

    if lower_text:
        # Convert to lowercase
        text = text.lower()
    else: pass

    if remove_whitespace:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
    else: pass
    
    if tokenize:
        # Use NLTK tokenizer to tokenize the text if needed
        tokens = word_tokenize(text)
    else: tokens = None

    return text, tokens


# Additional feature extraction functions

# NOTE - I don't think we'll want to use this functions as it will split on any whitespace which can lead to unexpected counts if there are
# extrac spaces or hidden characters. Additionally, this would count punctuation and numbers as words which is not what we want.
# def get_article_word_count(article):
#     return len(article.split())

def find_polarity(news_story):
    return TextBlob(news_story).sentiment.polarity

def find_subjectivity(news_story):
    return TextBlob(news_story).sentiment.subjectivity

def find_avg_polarity_sentences(news_story):
    news = TextBlob(news_story)
    polarities = [sentence.sentiment.polarity for sentence in news.sentences]
    return sum(polarities) / len(polarities) if polarities else 0

def find_avg_subjectivity_sentences(news_story):
    news = TextBlob(news_story)
    subjectivities = [sentence.sentiment.subjectivity for sentence in news.sentences]
    return sum(subjectivities) / len(subjectivities) if subjectivities else 0

def get_num_speech_attributes(text):
    text = text.lower()
    return text.count("said") + text.count("say") + text.count("told") + text.count("tell")

# Master function to extract all features from a user uploaded article
def extract_features_from_article(article_text):
    # 1. Clean the text and get tokens
    cleaned_text, tokens = clean_text(article_text, lower_text=True, remove_whitespace=True, fix_encoding=True, tokenize=True)
    
    # 2. Use the pre-fitted TF-IDF vectorizer and PCA model to extract 50 principal components
    tfidf_vec = tfidf_vectorizer.transform([cleaned_text])
    # Convert to dense array if needed
    pca_features = pca_model.transform(tfidf_vec.toarray())  # shape (1, 50)
    # Create a dictionary for the PCA features:
    pca_feature_dict = {f'pca_{i+1}': pca_features[0][i] for i in range(pca_features.shape[1])}
    
    
    # 3. Extract other features from the slightly cleaned original article text (to preserve punctuation/sentence structure)
    article_text_cleaned, _ = clean_text(article_text)
    reading_ease_score = textstat.flesch_reading_ease(article_text_cleaned)

    # Remove numbers and punctuation for word count
    words = [token for token in tokens if token not in string.punctuation]
    article_text_cleaned_word_count = len(words)

    overall_polarity = find_polarity(article_text_cleaned)
    overall_subjectivity = find_subjectivity(article_text_cleaned)
    avg_sentence_polarity = find_avg_polarity_sentences(article_text_cleaned)
    avg_sentence_subjectivity = find_avg_subjectivity_sentences(article_text_cleaned)
    num_speech_attributes = get_num_speech_attributes(article_text_cleaned)
    
    # 4. Combine all features into one dictionary
    features = {}
    features.update(pca_feature_dict)
    features["flesch_reading_ease"] = reading_ease_score
    features["word_count"] = article_text_cleaned_word_count
    features["overall_polarity"] = overall_polarity
    features["overall_subjectivity"] = overall_subjectivity
    features["avg_sentence_polarity"] = avg_sentence_polarity
    features["avg_sentence_subjectivity"] = avg_sentence_subjectivity
    features["num_speech_attributes"] = num_speech_attributes

    # 5. Prepare the feature vector for prediction in the same order as during training.
    # (Adjust the order here to exactly match the training feature order)
    feature_order = [f'pca_{i+1}' for i in range(50)] + [
        "flesch_reading_ease", "word_count", "overall_polarity",
        "overall_subjectivity", "avg_sentence_polarity", "avg_sentence_subjectivity",
        "num_speech_attributes"
    ]
    feature_vector = [features[col] for col in feature_order]
    feature_vector = np.array(feature_vector).reshape(1, -1)
    
    # Convert the TF-IDF vector to a dense array and get the vocabulary.
    tfidf_array = tfidf_vec.toarray()[0]
    vocab = tfidf_vectorizer.get_feature_names_out()
    
    # Zip the vocabulary and corresponding tfidf scores; filter out zero values.
    term_scores = [(term, score) for term, score in zip(vocab, tfidf_array) if score > 0]
    
    # Sort terms by descending tfidf value and take the top 10 (you can adjust this number).
    top_terms = sorted(term_scores, key=lambda x: x[1], reverse=True)[:10]
    
    # IMPORTANT: You must have computed these dictionaries beforehand.
    # For demonstration, we assume they are available as:
    # credible_tfidf_avg and noncredible_tfidf_avg, mapping each term to its average tfidf.
    tfidf_dumbbell_data = []
    for term, score in top_terms:
        avgCredible = credible_tfidf_avg.get(term, 0.0)
        avgNonCredible = noncredible_tfidf_avg.get(term, 0.0)
        tfidf_dumbbell_data.append({
            "term": term,
            "score": float(score),
            "avgCredible": float(avgCredible),
            "avgNonCredible": float(avgNonCredible)
        })
    
    
    # 6. Use the RF model to generate a prediction
    prediction = rf_model.predict_proba(feature_vector)
    
    return features, prediction[0,1], tfidf_dumbbell_data

# Example usage, uncomment and pass one of the articles to test the function:
# article = "This is an example article. It includes numbers like 123, punctuation, and multiple sentences."
# big_article_fake = """This story is about more than a massive cover-up for an elected officials who sexually assaulted innocent women, it s also about the media s lack of desire to report about crimes that have obviously been covered up in DC for a very long time. Perhaps the media s reluctance to report about the sexual abuse taking place in Washington DC, is because most, if not all, of the elected officials whose crimes are now being uncovered, are Democrats? So far, two of the most rabid anti-Trump Democrats in Washington, Senator Al Franken D-MI and now Representative John Conyers D-MI have been outed is it a coincidence, or could it be that one of the reasons Democrats are so adamantly opposed to Trump s presidency is because he is shaking things up in Washington, and in doing so, he s breaking up the good ole  boys network?Buzzfeed   Michigan Rep. John Conyers, a Democrat and the longest-serving member of the House of Representatives, settled a wrongful dismissal complaint in 2015 with a former employee who alleged she was fired because she would not  succumb to his sexual advances. Documents from the complaint obtained by BuzzFeed News from Mike Cernovich, include four signed affidavits, three of which are notarized, from former staff members who allege that Conyers, the ranking Democrat on the powerful House Judiciary Committee, repeatedly made sexual advances to female staff that included requests for sexual favors, contacting and transporting other women with whom they believed Conyers was having affairs, caressing their hands sexually, and rubbing their legs and backs in public. Four people involved with the case verified the documents are authentic.And the documents also reveal the secret mechanism by which Congress has kept an unknown number of sexual harassment allegations secret a grinding, closely held process that left the alleged victim feeling, she told BuzzFeed News, that she had no option other than to stay quiet and accept a settlement offered to her. I was basically blackballed. There was nowhere I could go,  she said in a phone interview. BuzzFeed News is withholding the woman s name at her request because she said she fears retribution.Last week the Washington Post reported that Congress s Office of Compliance paid out 17 million for 264 settlements with federal employees over 20 years for various violations, including sexual harassment. The Conyers documents, however, give a glimpse into the inner workings of the office, which has for decades concealed episodes of sexual abuse by powerful political figures.The woman who settled with Conyers launched the complaint with the Office of Compliance in 2014, alleging she was fired for refusing his sexual advances, and ended up facing a daunting process that ended with a confidentiality agreement in exchange for a settlement of more than 27,000. Her settlement, however, came from Conyers  office budget rather than the designated fund for settlements.Congress has no human resources department. Instead, congressional employees have 180 days to report a sexual harassment incident to the Office of Compliance, which then leads to a lengthy process that involves counseling and mediation, and requires the signing of a confidentiality agreement before a complaint can go forward.After this an employee can choose to take the matter to federal district court, but another avenue is available an administrative hearing, after which a negotiation and settlement may follow.In this case, one of Conyers  former employees was offered a settlement, in exchange for her silence, that would be paid out of Conyers  taxpayer-funded office budget. His office would  rehire  the woman as a  temporary employee  despite her being directed not to come into the office or do any actual work, according to the document. The complainant would receive a total payment of 27,111.75 over the three months, after which point she would be removed from the payroll, according to the document.The draft agreement viewed by BuzzFeed News was unsigned, but congressional employment records match the timing and amounts outlined in the document. The woman left the office and never went public with her story.The process was  disgusting,  said Matthew Peterson, who worked as a law clerk representing the complainant, and who listed as a signatory to some of the documents.Hillary Clinton and John Conyers have been longtime friends. What is it about Hillary that sexual predators find so endearing?  It is a designed cover-up,  said Peterson, who declined to discuss details of the case but agreed to characterize it in general terms.  You feel like they were betrayed by their government just for coming forward. It s like being abused twice. Two staffers alleged in their signed affidavits that Conyers used congressional resources to fly in women they believed he was having affairs with. Another said she was tasked with driving women to and from Conyers  apartment and hotel rooms.Rep. Conyers did not admit fault as part of the settlement. His office did not respond to multiple requests for comment on Monday.Citizen journalist Mike Cernovich admonishes  journalists  who are tasked with reporting the news for a living for ignoring how massive this cover up really isThe Conyers settlement was 1 out of 264How about you journalists stop hating on me and go find those other 263?  Mike Cernovich   Cernovich November 21, 2017The documents were first provided to BuzzFeed News by Mike Cernovich, the men s rights figure turned pro-Trump media activist who propagated a number of false conspiracy theories including the  Pizzagate  conspiracy. Cernovich said he gave the documents to BuzzFeed News for vetting and further reporting, and because he said if he published them himself, Democrats and congressional leaders would  try to discredit the story by attacking the messenger.  He provided them without conditions. BuzzFeed News independently confirmed the authenticity of the documents with four people directly involved with the case, including the accuser.Here s citizen journalist Mike Cernovich telling his massive Twitter audience that Speaker of the House Paul Ryan helped to cover up John Conyers disgusting sexual assaultsCongressman John Conyers is a sexual predator, and Paul Ryan covered it all up   Mike Cernovich   Cernovich November 21, 2017In her complaint, the former employee said Conyers repeatedly asked her for sexual favors and often asked her to join him in a hotel room. On one occasion, she alleges that Conyers asked her to work out of his room for the evening, but when she arrived the congressman started talking about his sexual desires. She alleged he then told her she needed to  touch it,  in reference to his penis, or find him a woman who would meet his sexual demands.She alleged Conyers made her work nights, evenings, and holidays to keep him company.In another incident, the former employee alleged the congressman insisted she stay in his room while they traveled together for a fundraising event. When she told him that she would not stay with him, she alleged he told her to  just cuddle up with me and caress me before you go. Rep. Conyers strongly postulated that the performing of personal service or favors would be looked upon favorably and lead to salary increases or promotions,  the former employee said in the documents.Three other staff members provided affidavits submitted to the Office Of Compliance that outlined a pattern of behavior from Conyers that included touching the woman in a sexual manner and growing angry when she brought her husband around.One affidavit from a former female employee states that she was tasked with flying in women for the congressman.  One of my duties while working for Rep. Conyers was to keep a list of women that I assumed he was having affairs with and call them at his request and, if necessary, have them flown in using Congressional resources,  said her affidavit. A second staffer alleged in an interview that Conyers used taxpayer resources to fly women to him.The employee said in her affidavit that Conyers also made sexual advances toward her  I was driving the Congressman in my personal car and was resting my hand on the stick shift. Rep. Conyers reached over and began to caress my hand in a sexual manner. The woman said she told Conyers she was married and not interested in pursuing a sexual relationship, according to the affidavit. She said she was told many times by constituents that it was well-known that Conyers had sexual relationships with his staff, and said she and other female staffers felt this undermined their credibility. I am personally aware of several women who have experienced the same or similar sexual advances made towards them by Rep. John Conyers,  she said in her affidavit.A male employee wrote that he witnessed Rep. Conyers rub the legs and other body parts of the complainant  in what appeared to be a sexual manner  and saw the congressman rub and touch other women  in an inappropriate manner.  The employee said he confronted Conyers about this behavior. Rep. Conyers said he needed to be  more careful  because bad publicity would not be helpful as he runs for re-election. He ended the conversation with me by saying he would  work on  his behavior,  the male staffer said in his affidavit.",this story is about more than a massive coverup for an elected officials who sexually assaulted innocent women it s also about the media s lack of desire to report about crimes that have obviously been covered up in dc for a very long time perhaps the media s reluctance to report about the sexual abuse taking place in washington dc is because most if not all of the elected officials whose crimes are now being uncovered are democrats so far two of the most rabid antitrump democrats in washington senator al franken dmi and now representative john conyers dmi have been outed is it a coincidence or could it be that one of the reasons democrats are so adamantly opposed to trump s presidency is because he is shaking things up in washington and in doing so he s breaking up the good ole boys networkbuzzfeed michigan rep john conyers a democrat and the longestserving member of the house of representatives settled a wrongful dismissal complaint in with a former employee who alleged she was fired because she would not succumb to his sexual advances documents from the complaint obtained by buzzfeed news from mike cernovich include four signed affidavits three of which are notarized from former staff members who allege that conyers the ranking democrat on the powerful house judiciary committee repeatedly made sexual advances to female staff that included requests for sexual favors contacting and transporting other women with whom they believed conyers was having affairs caressing their hands sexually and rubbing their legs and backs in public four people involved with the case verified the documents are authenticand the documents also reveal the secret mechanism by which congress has kept an unknown number of sexual harassment allegations secret a grinding closely held process that left the alleged victim feeling she told buzzfeed news that she had no option other than to stay quiet and accept a settlement offered to her i was basically blackballed there was nowhere i could go she said in a phone interview buzzfeed news is withholding the woman s name at her request because she said she fears retributionlast week the washington post reported that congress s office of compliance paid out million for settlements with federal employees over years for various violations including sexual harassment the conyers documents however give a glimpse into the inner workings of the office which has for decades concealed episodes of sexual abuse by powerful political figuresthe woman who settled with conyers launched the complaint with the office of compliance in alleging she was fired for refusing his sexual advances and ended up facing a daunting process that ended with a confidentiality agreement in exchange for a settlement of more than her settlement however came from conyers office budget rather than the designated fund for settlementscongress has no human resources department instead congressional employees have days to report a sexual harassment incident to the office of compliance which then leads to a lengthy process that involves counseling and mediation and requires the signing of a confidentiality agreement before a complaint can go forwardafter this an employee can choose to take the matter to federal district court but another avenue is available an administrative hearing after which a negotiation and settlement may followin this case one of conyers former employees was offered a settlement in exchange for her silence that would be paid out of conyers taxpayerfunded office budget his office would rehire the woman as a temporary employee despite her being directed not to come into the office or do any actual work according to the document the complainant would receive a total payment of over the three months after which point she would be removed from the payroll according to the documentthe draft agreement viewed by buzzfeed news was unsigned but congressional employment records match the timing and amounts outlined in the document the woman left the office and never went public with her storythe process was disgusting said matthew peterson who worked as a law clerk representing the complainant and who listed as a signatory to some of the documentshillary clinton and john conyers have been longtime friends what is it about hillary that sexual predators find so endearing it is a designed coverup said peterson who declined to discuss details of the case but agreed to characterize it in general terms you feel like they were betrayed by their government just for coming forward it s like being abused twice two staffers alleged in their signed affidavits that conyers used congressional resources to fly in women they believed he was having affairs with another said she was tasked with driving women to and from conyers apartment and hotel roomsrep conyers did not admit fault as part of the settlement his office did not respond to multiple requests for comment on mondaycitizen journalist mike cernovich admonishes journalists who are tasked with reporting the news for a living for ignoring how massive this cover up really isthe conyers settlement was out of how about you journalists stop hating on me and go find those other mike cernovich cernovich november the documents were first provided to buzzfeed news by mike cernovich the men s rights figure turned protrump media activist who propagated a number of false conspiracy theories including the pizzagate conspiracy cernovich said he gave the documents to buzzfeed news for vetting and further reporting and because he said if he published them himself democrats and congressional leaders would try to discredit the story by attacking the messenger he provided them without conditions buzzfeed news independently confirmed the authenticity of the documents with four people directly involved with the case including the accuserhere s citizen journalist mike cernovich telling his massive twitter audience that speaker of the house paul ryan helped to cover up john conyers disgusting sexual assaultscongressman john conyers is a sexual predator and paul ryan covered it all up mike cernovich cernovich november in her complaint the former employee said conyers repeatedly asked her for sexual favors and often asked her to join him in a hotel room on one occasion she alleges that conyers asked her to work out of his room for the evening but when she arrived the congressman started talking about his sexual desires she alleged he then told her she needed to touch it in reference to his penis or find him a woman who would meet his sexual demandsshe alleged conyers made her work nights evenings and holidays to keep him companyin another incident the former employee alleged the congressman insisted she stay in his room while they traveled together for a fundraising event when she told him that she would not stay with him she alleged he told her to just cuddle up with me and caress me before you go rep conyers strongly postulated that the performing of personal service or favors would be looked upon favorably and lead to salary increases or promotions the former employee said in the documentsthree other staff members provided affidavits submitted to the office of compliance that outlined a pattern of behavior from conyers that included touching the woman in a sexual manner and growing angry when she brought her husband aroundone affidavit from a former female employee states that she was tasked with flying in women for the congressman one of my duties while working for rep conyers was to keep a list of women that i assumed he was having affairs with and call them at his request and if necessary have them flown in using congressional resources said her affidavit a second staffer alleged in an interview that conyers used taxpayer resources to fly women to himthe employee said in her affidavit that conyers also made sexual advances toward her i was driving the congressman in my personal car and was resting my hand on the stick shift rep conyers reached over and began to caress my hand in a sexual manner the woman said she told conyers she was married and not interested in pursuing a sexual relationship according to the affidavit she said she was told many times by constituents that it was wellknown that conyers had sexual relationships with his staff and said she and other female staffers felt this undermined their credibility i am personally aware of several women who have experienced the same or similar sexual advances made towards them by rep john conyers she said in her affidavita male employee wrote that he witnessed rep conyers rub the legs and other body parts of the complainant in what appeared to be a sexual manner and saw the congressman rub and touch other women in an inappropriate manner the employee said he confronted conyers about this behavior rep conyers said he needed to be more careful because bad publicity would not be helpful as he runs for reelection he ended the conversation with me by saying he would work on his behavior the male staffer said in his affidavit"""
# features, prediction = extract_features_from_article(big_article_fake)
# print(features, prediction)