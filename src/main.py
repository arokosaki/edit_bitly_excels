from .input_output import EXCEL,get_input
from .edit_file import EditFile
from .exceptions import RUNNING_ERROR_STRING,APIKeyExpired
import logging

if __name__ == '__main__':
    input_data = get_input()
    logging.basicConfig(filename='log.log', level=logging.INFO,format='%(asctime)s %(levelname)s:%(message)s')
    excel_io = EXCEL(input_file_path=input_data.input_file,
                     output_folder=input_data.output_dir,
                     row_number=input_data.from_line)
    data_list = excel_io.get_data_in_list_form()
    try:
        edited_file = EditFile().execute(data_list,start_from=input_data.from_line)
    except APIKeyExpired as e:
        print(e)
        exit()
    if type(edited_file) == tuple:
        print(RUNNING_ERROR_STRING.format(edited_file[2].__class__.__name__,edited_file[2], edited_file[1]))
        excel_io.save_data_to_excel_wb(edited_file[0])
    else:
        excel_io.save_data_to_excel_wb(edited_file)

