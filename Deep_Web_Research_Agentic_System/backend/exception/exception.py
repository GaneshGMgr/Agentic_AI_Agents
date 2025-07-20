import sys
import traceback
import logging

class CustomException(Exception):
    def __init__(self, error_message, error_details):
        super().__init__(error_message)
        _, _, exc_tb = error_details
        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.error_message = error_message

    def __str__(self):
        return (
            f"Error occurred in Python script [{self.file_name}] "
            f"line number [{self.lineno}] error message [{self.error_message}]"
        )

if __name__ == "__main__":
    try:
        a = 1 / 0  # Intentional error
    except Exception as e:
        exc_info = sys.exc_info()
        raise CustomException(str(e), exc_info)
