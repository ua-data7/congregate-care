import csv
from care.sms.models import Facility, Binding
from django.conf import settings
csv_in_f = '/file/to/import.csv'
fieldnames = [
    'Facility Name',
    'Facility Address',
    'Contact Phone',
    'Known SMS',
    'Contact Name',
    'Contact Email',
    'Liaison Email',
    'LTC',
    'ALF',
    'Apartments',
    'Other',
    'Behavioral Health',
    'Hospice',
    'Home Health',
    'Group Home',
    'Facility Size',
    'Liaison Name',
    'Cluster/NC',
    'UUID',
]
tag_keys = ['LTC','ALF','Apartments','Other','Behavioral Health','Hospice','Home Health','Group Home']
with open(csv_in_f, 'r+') as csv_f:
    csv_in = csv.DictReader(csv_f)
    for row in csv_in:
        uuid = row['UUID']
        tags = []
        for key in tag_keys:
            if row[key] == 'Yes':
                tags.append(key)
        if uuid.strip().lower() == 'new':
            # new facility
            cluster = row['Cluster/NC'] == 'Yes'
            facility = Facility.objects.create(
                name=row['Facility Name'],
                facility_size=row['Facility Size'],
                cluster=cluster,
                address=row['Facility Address'],
                liaisons=row['Liaison'],
                emails=row['Contact Email'],
                phones=row['Contact Phone'],
            )
            facility.tags.set(tags)
            sms_numbers = row['Known SMS'].strip()
            for num in sms_numbers:
                s_num = num
                if not s_num.startswith('+'):
                    s_num = '+' + s_num
                b = Binding.objects.create(address=s_num, facility=facility)
        else:
            facility = Facility.objects.get(identity=uuid)
            sms_numbers = row['Known SMS'].strip()
            for num in sms_numbers:
                s_num = num
                if not s_num.startswith('+'):
                    s_num = '+' + s_num
                binding = Binding.objects.filter(address=s_num)
                if binding.exists():
                    if binding[0].facility.identity == facility.identity:
                        # already set properly
                        pass
                    else:
                        binding[0].delete()
                        b = Binding.objects.create(address=s_num, facility=facility)
                else:
                    b = Binding.objects.create(address=s_num, facility=facility)
            facility.tags.set(tags, clear=True)
            facility.name = row['Facility Name']
            facility.facility_size = row['Facility Size']
            facility.cluster = row['Cluster/NC'] == 'Yes'
            facility.address = row['Facility Address']
            facility.liaisons = row['Liaison']
            facility.emails = row['Contact Email']
            facility.phones = row['Contact Phone']
            facility.save()
# export code:
# with open(csv_out_f, 'w+') as csv_f:
#     dict_writer = csv.DictWriter(csv_f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
#     dict_writer.writeheader()
#     for facility in Facility.objects.all():
#         all_tags = facility.tags.names()
#         ltc = 'Yes' if 'LTC' in all_tags else 'No'
#         alf = 'Yes' if 'ALF' in all_tags else 'No'
#         apartments = 'Yes' if 'Apartments' in all_tags else 'No'
#         other = 'Yes' if 'Other' in all_tags else 'No'
#         known_sms = ','.join(list(Binding.objects.filter(facility=facility).values_list('address', flat=True)))
#         if facility.liaisons in settings.LIAISON_EMAIL_MAP:
#             liaison_email = settings.LIAISON_EMAIL_MAP[facility.liaisons]
#             if type(liaison_email) is list:
#                 liaison_email = '; '.join(liaison_email)
#         else:
#             liaison_email = 'No email in email map for Liaison'
#         out_dict = {
#             'Facility Name': facility.name,
#             'Facility Address': facility.address,
#             'Contact Phone': facility.phones,
#             'Known SMS': known_sms,
#             'Contact Name': 'Not stored in DB - but we can! Let us know if you\'d like that change.',
#             'Contact Email': facility.emails,
#             'Liaison Email': liaison_email,
#             'LTC': ltc,
#             'ALF': alf,
#             'Apartments': apartments,
#             'Other': other,
#             'L': '',
#             'M': '',
#             'N': '',
#             'Facility Size': facility.facility_size,
#             'Liaison Name': facility.liaisons,
#             'Cluster/NC': 'Yes' if facility.cluster else 'No',
#             'UUID': facility.identity,
#         }
#         dict_writer.writerow(out_dict)
