import os


def is_new_source(source, filename):
    new_source = False

    if os.path.isfile(f'./{filename}'):
        src_file = open(filename, 'r', encoding='utf-8')
        content = src_file.read().splitlines()
        # print(content)
        src_file.close()
    else:
        src_file = open(filename, 'w', encoding='utf-8')
        print(f'Created file1 {src_file}')
        content = []
        src_file.close()

    if source not in content:
        new_source = True
        src_file = open(filename, 'a', encoding='utf-8')
        src_file.write(source)
        src_file.write('\n')
        src_file.close()

    return new_source


def reset_sources(filename):
    os.remove(filename)
    print("Successfully resetted my memory")


if __name__ == '__main__':
    print(is_new_source("one", "sources.txt"))
