# backend/exception/exception.py

import sys

class CustomException(Exception):
    def __init__(self, error_message, error_details=None):
        super().__init__(error_message)

        self.file_name = None
        self.lineno = None

        if isinstance(error_details, tuple) and len(error_details) == 3:
            _, _, exc_tb = error_details
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.lineno = exc_tb.tb_lineno

        self.error_message = error_message

    def __str__(self):
        location = (
            f"File [{self.file_name}], line [{self.lineno}]"
            if self.file_name and self.lineno
            else "Location unknown"
        )
        return (
            f"Error occurred in Python script {location}, "
            f"error message [{self.error_message}]"
        )



if __name__ == "__main__":
    try:
        a = 1 / 0  # Intentional error
    except Exception as e:
        exc_info = sys.exc_info()
        raise CustomException(str(e), exc_info)
