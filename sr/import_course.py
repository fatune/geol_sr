import csv

from .models import Subject, Fact, create_cards_simple, create_cards_simple_with_similar_second_card

def import_course_from_csv(file_name, subject_title):
    if Subject.objects.filter(title=subject_title).count()>0 : raise ValueError

    facts = import_cards_from_csv(file_name)

    s = Subject.objects.create(title=subject_title)
    s.save()
    s.fact_set.all()

    for i,fact in enumerate(facts):
        f = s.fact_set.create(order=i, explanation= "%s -- %s" % (fact[0], fact[1]) )
        f.save()
        create_cards_simple(f, fact[0], fact[1])

def import_cards_from_csv(file_name):
    with open(file_name, 'rt', encoding="utf8") as csvfile:
        course = csv.reader(csvfile,delimiter=';')
        facts = list(course)
        facts = [[ field.strip() for field in fact ] for fact in facts]
    return facts

def import_course_from_csv_similar_second_card(file_name, subject_title):
    if Subject.objects.filter(title=subject_title).count()>0 : raise ValueError

    facts = import_cards_from_csv(file_name)

    s = Subject.objects.create(title=subject_title)
    s.save()
    s.fact_set.all()

    for i,fact in enumerate(facts):
        f = s.fact_set.create(order=i, explanation= "%s -- %s" % (fact[0], fact[1]) )
        f.save()
        create_cards_simple_with_similar_second_card(f, fact[0], fact[1], fact[2], fact[3])
