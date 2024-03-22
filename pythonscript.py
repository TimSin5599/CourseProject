from extractingAttributes import (
    build_path,
    open_file,
    get_name,
    get_experience,
    get_organization,
    get_email,
    get_phone_number,
    get_attributes_from_model)

if __name__ == '__main__':
    path_ = build_path()
    text_ = open_file(path_)

    skills, edu, org, languages, self_summary, speciality, faculty = get_attributes_from_model(text_)
    print("FIO - ", get_name(text_))
    print("Phone number - ", get_phone_number(text_))
    print("Email - ", get_email(text_))
    print("Organizations - ", get_organization(text_))
    print("ORG - ", org)
    print("LANGUAGES - ", languages)
    print("EDU - ", edu)
    print("SPECIALTY - ", speciality)
    print("FACULTY - ", faculty)
    # print("Experience - ", get_experience(text_))
    print("Skills - ", skills)
    print("Self summary - ", self_summary)
