class Frame:
    def __init__(self):
        self.occupied = False
        self.content = None

class PhysicalMemory:
    def __init__(self, number_of_frames):
        self.frames = []
        for _ in range(number_of_frames):
            self.frames.append(Frame())
            
    def is_full(self):
        return all(frame.occupied for frame in self.frames)
    
    def load_page_into_frame(self, page_data):
        """Attempts to load a page into the first available frame and returns the frame number."""
        for i in range(len(self.frames)):
            if not self.frames[i].occupied:
                self.frames[i].occupied = True
                self.frames[i].content = page_data
                return i
        return None

