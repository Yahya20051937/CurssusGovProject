# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def get_random_hash():
    import string, random
    alphabet_symbols = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    numbers = list(string.digits)

    all_symbols_and_numbers = alphabet_symbols + numbers

    all_symbols_and_numbers = [t for t in all_symbols_and_numbers if t != '/']

    my_hash = ''
    for i in range(19):
        my_hash += all_symbols_and_numbers[random.randint(0, len(all_symbols_and_numbers) - 1)]
    return my_hash


def admin():
    from Main.models import University, Course
    universities_hashes = ["G4zg5ahz1CCZzOQQQxi", "y0VZKg20VoIOb8pTCeP"]
    fst_courses = ['MIP', 'BCG']
    fst_cities = ['FES', 'TANGER', 'MARRAKECH', 'MOHAMMADIA', 'STATT', 'HOCEIMA']
    est_cities = [
        "Casablanca",
        "Rabat",
        "Fes",
        "Marrakech",
        "Tangier",
        "Agadir",
        "Meknes",
        "Oujda",
        "Kenitra",
        "Nador",
        "Beni Mellal",
        "Tetouan",
        "Safi",
        "El Jadida",
        "Khouribga",
        "Settat",
        "Taza",
        "Mohammedia",
        "Khenifra",
        "Larache"
    ]
    est_courses = [
        "Génie Logiciel (Software Engineering)",
        "Informatique Industrielle (Industrial Computing)",
        "Réseaux et Télécommunications (Networks and Telecommunications)",
        "Conception de Systèmes Embarqués (Embedded Systems Design)",
        "Gestion de Projets Informatiques (Project Management in IT)",
        "Sécurité Informatique (Computer Security)",
        "Intelligence Artificielle (Artificial Intelligence)",
        "Ingénierie des Systèmes d'Information (Information Systems Engineering)",
        "Technologies Web Avancées (Advanced Web Technologies)",
        "Robotique et Automatisation (Robotics and Automation)"
    ]
    i = -1
    for uni in universities_hashes:
        i += 1
        uni_obj = University.objects.get(hash=uni)

        if i == 0:
            for city in fst_cities:
                for crs in fst_courses:
                    course = Course.objects.create(hash=get_random_hash(), city=city, subject=crs, university=uni_obj, seats=760)
                    course.save()
        elif i == 2:
            for city in est_cities:
                for crs in est_courses:
                    course = Course.objects.create(hash=get_random_hash(), city=city, subject=crs, university=uni_obj, seats=90)
                    course.save()
