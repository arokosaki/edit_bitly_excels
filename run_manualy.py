from facebook_stats.src.input_output import EXCEL,get_input
from facebook_stats.src.edit_file import EditFile
from facebook_stats.src.exceptions import RUNNING_ERROR_STRING,APIKeyExpired
from facebook_stats.src.log_and_interface import main_log_setup


INPUT_FILE = r'C:\fuck\bitly_output_until_row_13.xlsx'
OUTPUT_DIR = None
FROM_LINE = None


log = main_log_setup()

if __name__ == '__main__':

    # get input data from command line
    # input_data = get_input()

    # create input output object
    excel_io = EXCEL(input_file_path=INPUT_FILE,
                     output_folder=OUTPUT_DIR,
                     row_number=FROM_LINE)

    # read data from file
    data_list = excel_io.get_data_in_list_form()

    try:
        print('Starting processing:')

        # run main editing loop
        edited_file = EditFile().execute(data_list,start_from=FROM_LINE)
    except APIKeyExpired as e:
        print(e)
        exit()

    # if run stops in the middle do to internet connection or ctrl-c save file up until then
    if isinstance(edited_file,tuple):
        print(RUNNING_ERROR_STRING.format(edited_file.error.__class__.__name__, edited_file.line_number))
        log.error(RUNNING_ERROR_STRING.format(edited_file.error.__class__.__name__, edited_file.line_number))
        log.info('saving with error')
        excel_io.save_data_to_excel_wb(edited_file.result,error=True)

    # save edited file
    else:
        log.info('saving file run finished')
        excel_io.save_data_to_excel_wb(edited_file)
        print('Running ended')
