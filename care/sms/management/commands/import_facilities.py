from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook
from care.sms.models import Facility
from care.sms.models import get_uuid
# Facility Name, 0
# Facility Address, 1
# Contact phone, 2
# Known SMS, 3
# Contact Name, 4
# Contact Email, 5
# LTC, 6
# ALF, 7
# Apartments, 8
# Other, 9
# Facility Size, 10
# Liaison Name, 11
# Cluster/NC, 12
class Command(BaseCommand):
    help = 'Import Facilities from Facility Liason List Excel file. THIS WILL DELETE ALL EXISTING FACILITIES.'
    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
    def handle(self, *args, **options):
        Facility.objects.all().delete()
        wb = load_workbook(options['path'])
        ws1 = wb.active
        rows = 0
        for row in ws1:
            if rows > 0:
                phones = ', '.join(row[2].value.split(';'))
                if row[5].value:
                    emails = ', '.join(row[5].value.split(';'))
                else:
                    emails = ''
                ltc = row[6].value.lower() == 'yes'
                alf = row[7].value.lower() == 'yes'
                apartments = row[8].value.lower() == 'yes'
                other = row[9].value.lower() == 'yes'
                cluster = row[12].value.lower() == 'cluster'
                size = row[10].value.strip()
                liaison_name = row[11].value.strip()
                uuid = get_uuid()
                facility = Facility.objects.create(
                    identity=uuid,
                    name=row[0].value.strip(),
                    address=row[1].value.strip(),
                    emails=emails,
                    phones=phones,
                    cluster=cluster,
                    facility_size=size,
                    liaisons=liaison_name,
                )
                if apartments:
                    facility.tags.add('Apartments')
                if ltc:
                    facility.tags.add('LTC')
                if alf:
                    facility.tags.add('ALF')
                if other:
                    facility.tags.add('Other')
                facility.save()
                sms_phones = row[3].value
                if sms_phones:
                    for phone in sms_phones.split(','):
                        addr = '+' + phone.strip()
                        Binding.objects.create(
                            address=addr,
                            facility=facility,
                        )
            rows += 1