import os,csv,openpyxl,argparse

class InputOutput(object):

    def __init__(self,input_file_path='',output_folder=None,row_number=0):

        self.input_file_path = input_file_path
        self.file_name = os.path.basename(input_file_path).split('.')
        self.output_folder = output_folder or os.path.dirname(input_file_path)
        if row_number:
            self.output_file_name = self.file_name[0]+'_output_from_row_{}.'.format(row_number)+self.file_name[-1]
        else:
            self.output_file_name = self.file_name[0]+'_output.'+self.file_name[-1]
        self.output_file_path = os.path.join(self.output_folder, self.output_file_name)

    @classmethod
    def create_entire_folder_path(cls,path):
        if os.path.exists(path):
            return
        else:
            cls.create_entire_folder_path(os.path.dirname(path[:-1]))
            os.mkdir(path)


class CSV(InputOutput):

    def open_csv_file(self):

        with open(self.input_file_path,newline='', encoding='utf-8')as f:
            reader = csv.reader(f)
            data_list = list(reader)
        return data_list

    def write_row_csv(self,row):
        self.create_entire_folder_path(path=self.output_folder)
        with open(self.output_file_path, 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(row)

    def write_csv_file(self,data_list):
        self.create_entire_folder_path(path=self.output_folder)
        with open(self.output_file_path, 'w', newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            for row in data_list:
                csv_writer.writerow(row)

class EXCEL(InputOutput):

    def load_excel_file(self):
        wb = openpyxl.load_workbook(self.input_file_path)
        return wb
    def get_data_in_list_form(self):
        sheet = self.load_excel_file().active
        data_list = []
        for r in sheet.rows:
            row = []
            for cell in r:
                row.append(cell.value)
            data_list.append(row)
        return data_list
    def get_relevent_column(self,column):
        pass

    def save_data_to_excel_wb(self,data_list):
        self.create_entire_folder_path(path=self.output_folder)
        wb = openpyxl.Workbook(write_only=True)
        ws = wb.create_sheet()
        for row in data_list:
            ws.append(row)
        wb.save(self.output_file_path)


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',help="Add input file path in quotes")
    parser.add_argument('-o', '--output_dir',help='Output folder optional')
    parser.add_argument('-l', '--from_line', type=int, help='If former execution failed start from where it ended')
    args = parser.parse_args()
    if not os.path.isfile(args.input_file):
        print('Input file path is invalid')
        exit()
    else:
        return args