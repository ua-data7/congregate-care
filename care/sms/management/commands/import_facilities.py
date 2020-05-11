from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook
from care.sms.models import Facility
from care.sms.models import get_uuid
# Facility Name, 0
# Facility Address, 1
# Contact phone, 2
# Contact Name, 3
# Contact Email, 4
# LTC, 5
# ALF, 6
# Apartments, 7
# Other, 8
# Facility Size, 9
# Liaison Name, 10
# Cluster/NC, 11
class Command(BaseCommand):
    help = 'Import Facilities from Facility Liason List Excel file.'
    def add_arguments(self, parser):
        parser.add_argument('path', type=str)
    def handle(self, *args, **options):
        Facility.objects.all().delete()
        wb = load_workbook(options['path'])
        ws1 = wb.active
        rows = 0
        for row in ws1:
            if rows > 0:
                # name
                # facility_size
                # cluster
                # address
                # liason_uuid
                # emails
                # phones
                # tags
                phones = ', '.join(row[2].value.split(';'))
                if row[4].value: emails = ', '.join(row[4].value.split(';'))
                else: emails = ''
                ltc = row[5].value.lower() == 'yes'
                alf = row[6].value.lower() == 'yes'
                apartments = row[7].value.lower() == 'yes'
                other = row[8].value.lower() == 'yes'
                cluster = row[11].value.lower() == 'cluster'
                liason_name = row[10].value
                uuid = get_uuid()
                facility = Facility.objects.create(
                    identity=uuid,
                    name=row[0].value,
                    address=row[1].value,
                    emails=emails,
                    phones=phones,
                    cluster=cluster,
                    liasons=liason_name,
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
            
            rows += 1