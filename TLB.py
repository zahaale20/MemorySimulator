class TLB:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.entries = []

    def _validate_page_number(self, page_num):
        if not (0 <= page_num <= 255):
            raise ValueError("Page number must be between 0 and 255 inclusive")

    def add_entry(self, page_num, frame_num):
        self._validate_page_number(page_num)
        if len(self.entries) >= self.capacity:
            self.entries.pop(0)
        self.entries.append((page_num, frame_num))

    def get_frame(self, page_num):
        """Retrieve the frame number associated with the given page number from the TLB."""
        self._validate_page_number(page_num)
        for page, frame in self.entries:
            if page == page_num:
                return frame
        return None

    def remove_frame(self, page_num):
        """Remove the TLB entry corresponding to the specified page number."""
        self._validate_page_page_number(page_num)
        self.entries = [(page, frame) for page, frame in self.entries if page != page_num]
