class PageTable:
    def __init__(self):
        self.table = [None] * 256

    def _validate_page_number(self, page_num):
        if not (0 <= page_num <= 255):
            raise ValueError("Page number must be between 0 and 255 inclusive")

    def add(self, page_num, physical_frame_num, loaded):
        self._validate_page_number(page_num)
        self.table[page_num] = (physical_frame_num, loaded)

    def update_page_status(self, page_num, loaded):
        self._validate_page_number(page_num)
        current_frame = self.table[page_num]
        if current_frame is None:
            raise ValueError("Page is not in Page Table")
        self.table[page_num] = (current_frame[0], loaded)

    def remove(self, page_num):
        self._validate_page_number(page_num)
        self.table[page_num] = None

    def get_frame(self, page_num):
        self._validate_page_number(page_num)
        return self.table[page_num]

