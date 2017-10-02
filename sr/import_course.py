import csv

from .models import Subject, Fact

def import_course_from_csv(file_name, subject_title):
    with open(file_name, 'rt', encoding="utf8") as csvfile:
        course = csv.reader(csvfile,delimiter=';')
        facts = list(course)
        facts = [[ field.strip() for field in fact ] for fact in facts]

    if Subject.objects.filter(title=subject_title).count()>0 : raise ValueError

    s = Subject.objects.create(title=subject_title)
    s.save()

    s.fact_set.all()

    for i,fact in enumerate(facts):
        f = s.fact_set.create(order=i, field1=fact[0], field2=fact[1])
        f.save()
        f.create_cards()
