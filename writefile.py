import os


def get_content(filename):
    if os.path.isfile(f'./{filename}'):
        src_file = open(filename, 'r', encoding='utf-8')
        content = src_file.read().splitlines()
        src_file.close()
    else:
        src_file = open(filename, 'w', encoding='utf-8')
        print(f'Created file: {src_file}')
        content = []
        src_file.close()

    return content


def is_new_source(source, filename):
    new_source = False
    content = get_content(filename)

    if source not in content:
        new_source = True
        src_file = open(filename, 'a', encoding='utf-8')
        src_file.write(source)
        src_file.write('\n')
        src_file.close()

    return new_source


if __name__ == '__main__':
    print(is_new_source("one", "sources.txt"))
