from extractingAttributes import build_path, open_file, get_name, get_experience, get_organization, get_email, get_skills, get_phone_number
import spacy

if __name__ == '__main__':
    path_ = build_path()
    text_ = open_file(path_)

    nlp = spacy.load("model-best")
    doc = nlp(text_)
    for ents in doc.ents:
        print(ents)

    # print("FIO - ", get_name(text_))
    # print("Phone number - ", get_phone_number(text_))
    # print("Email - ", get_email(text_))
    # print("Organizations - ", get_organization(text_))
    # print("Experience - ", get_experience(text_))
    # print("Skills - ", get_skills(text_))
