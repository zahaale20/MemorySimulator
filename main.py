import sys
from collections import deque
from TLB import TLB
from PageTable import PageTable
from PhysicalMemory import PhysicalMemory
from Utils import read_file, read_binary_file, find_optimal_page_to_replace

def main():
    if not (2 <= len(sys.argv) <= 4):
        print("Usage: memSim <reference-sequence-file.txt> <FRAMES> <PRA>")
        sys.exit(1)

    num_frames = 256
    page_replacement_algo = "fifo"
    if len(sys.argv) >= 3:
        num_frames = int(sys.argv[2])
        if not (0 < num_frames <= 256):
            print("FRAMES is an integer <= 256 and > 0")
            sys.exit(1)

    if len(sys.argv) == 4:
        page_replacement_algo = sys.argv[3]
        if page_replacement_algo not in ["fifo", "lru", "opt"]:
            print("page_replacement_algo must be either 'fifo', 'lru', or 'opt'")
            sys.exit(1)

    replacement_queue = deque()
    if page_replacement_algo == "lru":
        replacement_queue = deque()

    page_size = frame_size = 256
    sequence_file = sys.argv[1]
    reference_addresses = read_file(sequence_file)
    backing_store_content = read_binary_file('BACKING_STORE.bin')
    physical_memory = PhysicalMemory(num_frames)
    tlb = TLB()
    page_table = PageTable()
    page_fault_count = tlb_hit_count = tlb_miss_count = 0

    current_index = 0
    for current_address in reference_addresses:
        page_number = current_address // page_size
        offset = current_address % page_size
        future_references = [(addr // page_size) for addr in reference_addresses[current_index + 1:]]

        physical_frame_number = tlb.get_frame(page_number)

        if physical_frame_number is not None:
            tlb_hit_count += 1
            byte_data = physical_memory.frames[physical_frame_number].content[offset:offset + 1]
            data_value = int.from_bytes(byte_data, byteorder='big', signed=True)
            page_data = backing_store_content[page_number * page_size: (page_number + 1) * page_size]

            if page_replacement_algo == "lru":
                replacement_queue.remove((page_number, physical_frame_number))
                replacement_queue.append((page_number, physical_frame_number))
        else:
            tlb_miss_count += 1
            frame_data = page_table.get_frame(page_number)
            if frame_data is None:
                page_fault_count += 1
                page_data = backing_store_content[page_number * page_size: (page_number + 1) * page_size]
                if physical_memory.is_full():
                    if page_replacement_algo == "fifo":
                        page_number_to_remove, physical_frame_number = replacement_queue.popleft()
                    elif page_replacement_algo == "lru":
                        page_number_to_remove, physical_frame_number = replacement_queue.popleft()
                    else:
                        optimal_page = find_optimal_page_to_replace(future_references, page_table)
                        page_number_to_remove, physical_frame_number = optimal_page, page_table.get_frame(optimal_page)[0]

                    page_table.update(page_number_to_remove, physical_frame_number, False)
                    tlb.remove_frame(page_number_to_remove)
                    physical_memory.frames[physical_frame_number].content = page_data
                else:
                    physical_frame_number = physical_memory.load_page_into_frame(page_data)

                page_table.add(page_number, physical_frame_number, True)
                byte_data = page_data[offset:offset + 1]
                data_value = int.from_bytes(byte_data, byteorder='big', signed=True)

                tlb.add_entry(page_number, physical_frame_number)
                replacement_queue.append((page_number, physical_frame_number))
            else:
                physical_frame_number, is_loaded = frame_data
                if is_loaded:
                    byte_data = physical_memory.frames[physical_frame_number].content[offset:offset + 1]
                    data_value = int.from_bytes(byte_data, byteorder='big', signed=True)
                    page_data = backing_store_content[page_number * page_size: (page_number + 1) * page_size]

                    if page_replacement_algo == "lru":
                        replacement_queue.remove((page_number, physical_frame_number))
                        replacement_queue.append((page_number, physical_frame_number))
                else:
                    page_fault_count += 1
                    page_data = backing_store_content[page_number * page_size: (page_number + 1) * page_size]
                    if physical_memory.is_full():
                        if page_replacement_algo == "fifo":
                            page_number_to_remove, physical_frame_number = replacement_queue.popleft()
                        elif page_replacement_algo == "lru":
                            page_number_to_remove, physical_frame_number = replacement_queue.popleft()
                        else:
                            optimal_page = find_optimal_page_to_replace(future_references, page_table)
                            page_number_to_remove, physical_frame_number = page_table.get_frame(optimal_page)

                        page_table.update(page_number_to_remove, physical_frame_number, False)
                        tlb.remove_frame(page_number_to_remove)
                        physical_memory.frames[physical_frame_number].content = page_data
                    else:
                        physical_frame_number = physical_memory.load_page_into_frame(page_data)

                page_table.add(page_number, physical_frame_number, True)
                byte_data = page_data[offset:offset + 1]
                data_value = int.from_bytes(byte_data, byteorder='big', signed=True)

                tlb.add_entry(page_number, physical_frame_number)
                replacement_queue.append((page_number, physical_frame_number))

        print(f"{current_address}, {data_value}, {physical_frame_number}, {page_data.hex().upper()}")

        current_index += 1

    print(f"Number of Translated Addresses = {len(reference_addresses)}")
    print(f"Page Faults = {page_fault_count}")
    print(f"Page Fault Rate = {(page_fault_count / len(reference_addresses)):.3f}")
    print(f"TLB Hits = {tlb_hit_count}")
    print(f"TLB Misses = {tlb_miss_count}")
    print(f"TLB Hit Rate = {(tlb_hit_count / len(reference_addresses)):.3f}\n")

if __name__ == "__main__":
    main()