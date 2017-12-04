from django.core.management.base import BaseCommand, CommandError
import csv
from catalog.models import Product
from urllib.request import urlopen
from django.core.files.images import ImageFile
from django.core.files.temp import NamedTemporaryFile


class ImportCSV:
    products = list()

    def __init__(self, file_path):
        self.file_path = file_path

    def set_products(self):
        for item in self.products:

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(item['image']).read())
            img_temp.flush()

            product = Product(
                title=item['name'],
                text=item['description'],
                image=ImageFile(img_temp),
            )
            product.save()

    def make_product_list(self):
        with open(self.file_path, 'r') as file:
            reader = csv.reader(file)
            loop = False
            for line in reader:
                if loop:
                    self.products.append({
                        'name': line[1],
                        'description': line[3],
                        'image': line[11],
                    })
                loop = True

    def start(self):
        try:
            open(self.file_path, 'r')
        except IOError as e:
            raise BaseException(e)

        self.make_product_list()
        self.set_products()


class Command(BaseCommand):
    help = 'Импорт товаров без категорий из файла экспорта prom.ua'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to file on this computer')

    def handle(self, *args, **option):
        new_import = ImportCSV(option['file_path'])
        new_import.start()
