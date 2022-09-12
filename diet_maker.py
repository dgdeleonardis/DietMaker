import csv
import random
from fpdf import FPDF, HTMLMixin, HTML2FPDF

class PDF(FPDF, HTMLMixin):
    def write_html(self, text, image_map=None):
        h2p = HTML2FPDF(self, image_map)
        h2p.feed(text)

SOURCE_FILE_NAME = 'meal_frequency.csv'
class Day:
    def __init__(self):
        self.lunch = { 
            'carb_source': None,
            'protein_source': None
        }
        self.dinner = {
            'carb_source': None,
            'protein_source': None
        }
days = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']

def open_csv_file(filename):
    csv_file = open(filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=';')
    return csv_reader

def create_pdf(filename, data):
    pdf = PDF()
    print('ENTRO')
    pdf.add_page(orientation='l')
    pdf.set_font("Times", size=10)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / len(days)  # distribute content evenly
    for day in days:
        print(day)
        pdf.multi_cell(col_width, line_height, day, border=1,
            new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.ln(line_height)
    for d in data.values():
        print(type(d))
        pdf.multi_cell(col_width, line_height, d.lunch['carb_source'] + '\n' +  d.lunch['protein_source'], border=1,
            new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.ln(line_height)
    for d in data.values():
        pdf.multi_cell(col_width, line_height, d.dinner['carb_source'] + '\n' +  d.dinner['protein_source'], border=1,
            new_x='RIGHT', new_y='TOP', max_line_height=pdf.font_size)
    pdf.ln(line_height)
    
    pdf.output('weekly-diet.pdf')

def get_sources_from_type(filename, type):
    sources = {}

    csv_reader = open_csv_file(filename)
    for entry in csv_reader:
        if entry[1] == type:
            sources[entry[0]] = entry[2]
    return sources

def get_source(filename, type):
    source_dict = get_sources_from_type(filename, type)
    source_list = []
    for name, occurances in source_dict.items():
       source_list.extend([name for _ in range(int(occurances))])
    return source_list

if __name__ == '__main__':
    proteins = get_source(SOURCE_FILE_NAME, 'proteine')
    carbs = get_source(SOURCE_FILE_NAME, 'carboidrati')
    
    week = {}
    for x in days:
        week[x] = Day()
        week[x].lunch['carb_source'] = carbs.pop(random.choice(range(len(carbs))))
        week[x].lunch['protein_source'] = proteins.pop(random.choice(range(len(proteins))))
        choose = carbs.pop(random.choice(range(len(carbs))))
        while choose in ['riso', 'pasta']:
            carbs.append(choose)
            choose = carbs.pop(random.choice(range(len(carbs))))
        week[x].dinner['carb_source'] = choose
        choose = proteins.pop(random.choice(range(len(proteins))))
        while choose == week[x].lunch['protein_source']:
            proteins.append(choose)
            choose = proteins.pop(random.choice(range(len(proteins))))
        week[x].dinner['protein_source'] = choose
    
    for (y, cont) in week.items():
        print("Giorno: {}\n\tpranzo:\n\t\tcarboidrati: {}\n\t\tproteine: {}\ncena:\n\t\tcarboidrati: {}\n\t\tproteine: {}".format(
            y,
            cont.lunch['carb_source'],
            cont.lunch['protein_source'],
            cont.dinner['carb_source'],
            cont.dinner['protein_source']
        ))
    # check diet conditions
    create_pdf('settimana.pdf', week)



