def read_file(filename):
    with open(filename, 'r') as file:
        reference_sequence = [int(line.strip()) for line in file]
    return reference_sequence

def read_binary_file(file_path):
    with open(file_path, 'rb') as binary_file:
        return binary_file.read()

def find_optimal_page_to_replace(remaining_pages, page_table):
    for page_num in range(len(page_table.table)):
        if page_table.table[page_num] is not None and page_num not in remaining_pages:
            return page_num

    # Traverse the page_table
    max_index = 0
    visited = set()
    for i in range(len(remaining_pages)):
        page_num = remaining_pages[i]
        if page_num not in visited:
            visited.add(page_num)
            max_index = max(max_index, i)
    # print(f"optimal page: {remaining[max_index]}")
    return remaining_pages[max_index]

