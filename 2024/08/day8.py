from typing import List

def parse_input(input: str) -> List[int]:
    return list(map(int, list(input.strip())))

def checksum(disk: List[int]) -> int:
    return sum(i * e if e != -1 else 0 for i,e in enumerate(disk))

def compact_disk_frag(disk: List[int]) -> List[int]:
    i, j = 0, len(disk) - 1
    while i < j:
        i_value, j_value = disk[i], disk[j]
        if i_value == -1 and j_value != -1:
            disk[i], disk[j] = disk[j], disk[i]
            i, j = i + 1, j - 1
        elif j_value == -1:j -= 1
        elif i_value != -1:i += 1
    return disk
            
def compact_disk_unify(disk: List[int]) -> List[int]:
    file_id, files, free_spans, i = 0, [], [], 0

    while i < len(disk):
        start = i
        while i < len(disk) and disk[i] == (disk[start] if disk[start] != -1 else -1):
            i += 1
        if disk[start] != -1:
            files.append((disk[start], start, i - start))
        else:
            free_spans.append((start, i - start))

    files.sort(reverse=True, key=lambda x: x[0])

    for file_id, file_start, file_length in files:
        for span_start, span_length in free_spans:
            if span_length >= file_length and span_start < file_start:
                disk[span_start:span_start + file_length] = [file_id] * file_length
                disk[file_start:file_start + file_length] = [-1] * file_length

                free_spans.append((file_start, file_length))
                free_spans.remove((span_start, span_length))
                if span_length > file_length:
                    free_spans.append((span_start + file_length, span_length - file_length))
                free_spans.sort() 
                break
    return disk

def main(disk_map: List[int]):
    disk = []
    id = 0
    for i, e in enumerate(disk_map):
        if i % 2 == 0:
            disk.extend([id] * e)
            id += 1
        else:
            disk.extend([-1] * e)
    
    return (checksum(compact_disk_frag(disk.copy())), checksum(compact_disk_unify(disk.copy())))
if __name__ == "__main__":
    with open("./input.txt", "r") as file:
        disk_map = parse_input(file.read())
        print(main(disk_map))        