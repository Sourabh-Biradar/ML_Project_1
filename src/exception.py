import sys 

def error_message_details(error,error_detail):
    _,_,exc_tb = error_detail.exc_info()
    
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    return f"Error occurred in {file_name} at line {line_number}: {str(error)}"

class CustomException(Exception):
    def __init__(self, error, error_detail):
       
        super().__init__(error_message_details(error, error_detail))
        self.error_message = error_message_details(error, error_detail)

    def __str__(self):
        return self.error_message