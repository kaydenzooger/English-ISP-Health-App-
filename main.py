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
        lem = WordNetLemmatizer() 
        devd = []
        for text in texts:
            words = text.split()
            combined = " ".join(
                lem.lemmatize(word.lower(), pos=wordnet.VERB) + " " + 
                lem.lemmatize(word.lower(), pos=wordnet.NOUN) 
                for word in words
            )
            devd.append(combined)
        return devd

    def search(inn):

        derive_descps = derive(descps) 

        vec = TfidfVectorizer() 
        vector_descps = vec.fit_transform(derive_descps) 

        main_m = KNeighborsClassifier(n_neighbors=1) 
        main_m.fit(vector_descps, titles) 


        def search_model(ina):
            d_ina = derive([ina])[0] 
            ina_vec = vec.transform([d_ina]) 
            prediction = main_m.predict(ina_vec) 
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



cond = [i[0] for i in stuff] 
symp = [i[1] for i in stuff] 



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
