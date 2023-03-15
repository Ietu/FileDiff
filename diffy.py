import sys

def read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def print_diff(lines1, lines2):
    i = j = 0
    while i < len(lines1) and j < len(lines2):
        if lines1[i] == lines2[j]:
            i += 1
            j += 1
        else:
            print("- " + lines1[i].rstrip())
            print("+ " + lines2[j].rstrip())
            i += 1
            j += 1
    while i < len(lines1):
        print("- " + lines1[i].rstrip())
        i += 1
    while j < len(lines2):
        print("+ " + lines2[j].rstrip())
        j += 1

def generate_patch(lines1, lines2):
    i = j = 0
    patch = []
    while i < len(lines1) and j < len(lines2):
        if lines1[i] == lines2[j]:
            i += 1
            j += 1
        else:
            start_i = i
            start_j = j
            while i < len(lines1) and j < len(lines2) and lines1[i] != lines2[j]:
                j += 1
            end_j = j
            while i < len(lines1) and j < len(lines2) and lines1[i] != lines2[j]:
                i += 1
            end_i = i
            patch.append((start_i, end_i, start_j, end_j))
    return patch

def apply_patch(lines, patch):
    result = []
    i = j = 0
    for start_i, end_i, start_j, end_j in patch:
        result.extend(lines[i:start_i])
        result.extend(lines[start_j:end_j])
        i = end_i
        j = end_j
    result.extend(lines[i:])
    return result

if len(sys.argv) == 3:
    lines1 = read_file(sys.argv[1])
    lines2 = read_file(sys.argv[2])
    print_diff(lines1, lines2)
elif len(sys.argv) == 4 and sys.argv[1] == "diff":
    lines1 = read_file(sys.argv[2])
    lines2 = read_file(sys.argv[3])
    patch = generate_patch(lines1, lines2)
    for start_i, end_i, start_j, end_j in patch:
        print("{},{},{}".format(start_i + 1, end_i - start_i, ''.join(lines2[start_j:end_j])), end='')
elif len(sys.argv) == 4 and sys.argv[1] == "patch":
    lines = read_file(sys.argv[2])
    with open(sys.argv[3], 'r') as f:
        patch = f.readlines()
    patch = [(int(l.split(',')[0]) - 1, int(l.split(',')[0]) + int(l.split(',')[1]) - 1,
              len(l.split(',')[0]) + 1, len(l.rstrip())) for l in patch]
    result = apply_patch(lines, patch)
    print(''.join(result), end='')
else:
    print("Usage: python diffy.py file1 file2\n"
          "       python diffy.py diff file1 file2 > file.patch\n"
          "       python diffy.py patch file file.patch")
