import sys

def backend(insx, titles, descps):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.neighbors import KNeighborsClassifier
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import wordnet
    import nltk

    nltk.download("wordnet")
    nltk.download("omw-1.4")

    def derive(texts):
        lem = WordNetLemmatizer() # this word lemmatizer function just gets the deriviatives of the word using the databases downloaded earlier
        devd = []
        for text in texts:
            words = text.split()
            combined = " ".join(
                lem.lemmatize(word.lower(), pos=wordnet.VERB) + " " + # for verbs
                lem.lemmatize(word.lower(), pos=wordnet.NOUN) # and nouns
                for word in words
            )
            devd.append(combined)
        return devd

    def search(inn):

        derive_descps = derive(descps) # using the derive function

        vec = TfidfVectorizer() # converting the words into numbers/vectors/tokens using an importance algorithm that conisders how many times a word is used, the uniqueness of the word, etc.
        vector_descps = vec.fit_transform(derive_descps) # fitting the vectors to the words

        main_m = KNeighborsClassifier(n_neighbors=1) # modified complex distance formula to find distance between vectors and choose the closest one
        main_m.fit(vector_descps, titles) # assign the vectorized descriptions to the titles


        def search_model(ina):
            d_ina = derive([ina])[0] # derive input nouns and verbs
            ina_vec = vec.transform([d_ina]) # vectorize derived input
            prediction = main_m.predict(ina_vec) # use the distance formula neighbor algorithm to find the closest matching titles based on descriptions
            return prediction[0]

        final = search_model(insx)
        return final

    return search(insx)

stuff = [  

    ["cancer", "unexplained weight loss, fatigue, night sweats, unusual lumps, prolonged pain"],
    ["flu", "high fever, severe headache, muscle aches, chills, sore throat, dry cough"],
    ["cold", "runny or stuffy nose, sneezing, mild sore throat, low-grade fever, mild cough"],
    ["migraine", "throbbing headache, nausea, vomiting, visual disturbances, light and sound sensitivity"],
    ["diabetes", "excessive thirst, frequent urination, unexplained weight loss, extreme hunger, blurry vision, slow-healing wounds"],
    ["allergy", "sneezing, nasal congestion, itchy or watery eyes, skin rash, hives, difficulty breathing"],
    ["covid-19", "high fever, dry cough, loss of taste or smell, extreme fatigue, difficulty breathing, chest pain"],
    ["pneumonia", "sharp chest pain, difficulty breathing, high fever, productive cough with phlegm, chills, rapid heartbeat"],
    ["anemia", "chronic fatigue, pale or yellowish skin, dizziness, shortness of breath, cold hands and feet"],
    ["depression", "sadness, loss of interest, sleep disturbances, worthlessness, difficulty concentrating"],
    ["asthma", "recurrent wheezing, breathlessness, chest tightness, cough"],
    ["hypertension", "frequent headaches, dizziness, blurred vision, chest pain, shortness of breath, nosebleeds"],
    ["bronchitis", "cough with mucus, chest discomfort, shortness of breath, mild fever, wheezing"],
    ["tuberculosis", "chronic cough with blood, night sweats, unintended weight loss, chest pain, prolonged fever"],
    ["heart disease", "chest pain, shortness of breath, fatigue, irregular heartbeat, dizziness, swelling in legs"],
    ["stroke", "sudden numbness or weakness, confusion, difficulty speaking, loss of coordination"],
    ["kidney disease", "swelling in ankles, fatigue, nausea, difficulty urinating, muscle cramps, shortness of breath"],
    ["liver disease", "yellowing of skin, abdominal pain, dark urine, nausea, fatigue, swollen legs"],
    ["arthritis", "joint pain, swelling, stiffness, reduced range of motion"],
    ["appendicitis", "severe abdominal pain, nausea, vomiting, fever, loss of appetite"],
    ["meningitis", "severe headache, stiff neck, high fever, sensitivity to light, confusion, seizures"],
    ["ulcer", "burning stomach pain, nausea, bloating, vomiting blood, unexplained weight loss"],
    ["gastroenteritis", "diarrhea, nausea, vomiting, stomach cramps, fever, dehydration"],
    ["multiple sclerosis", "numbness or tingling, vision problems, muscle weakness, balance issues, cognitive difficulties"],
    ["Parkinson’s disease", "tremors, slow movement, muscle stiffness, impaired balance, speech difficulties"],
    ["Alzheimer’s disease", "memory loss, confusion, difficulty recognizing people, mood changes, difficulty speaking or writing"],

]



cond = [i[0] for i in stuff] # spllitting the 2d array into the conditions i[0] the first option
symp = [i[1] for i in stuff] # and i[1] the second one with the descriptions for everything



def main():
    try:
        with open('user_input.txt', 'r') as input_file:
            user_input = input_file.readline().strip()

        with open('output.txt', 'w') as output_file:
            oop = backend(user_input, cond, symp)
            output_file.write(oop)

    except Exception as e:
        with open('output.txt', 'w') as output_file:
            output_file.write(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
