import os
import argparse
import sys
from tqdm import tqdm


def execute_folder(args):
    alphabet = create_alphabet(args.alphabet)

    # get all files
    all_files = []
    root_path = ''
    for root, _, files in os.walk(args.input_folder):
        root_path = root
        all_files.extend(files)
    all_files = filter(lambda x: '.txt' in x, all_files)

    # iterate and translate
    for file_path in tqdm(all_files, ncols=150):
        # translate
        translation = ''
        file_name, _ = os.path.splitext(file_path)
        file_name = f'{int(file_name):08}'
        with open(os.path.join(root_path, file_path), mode='r') as read_file:
            for line in read_file.readlines():
                translation += alphabet[int(line)]
        # save the file
        # remove starting and ending spaces
        translation = translation.strip()
        with open(os.path.join(args.output_folder, file_name + '.txt'), mode='w', encoding='utf-8') as write_file:
            write_file.write(translation)


def create_alphabet(alphabet_path):
    alphabet = ' '
    with open(alphabet_path, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            alphabet += line.strip()
    return alphabet


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--alphabet', required=True,
                        help='path to the alphabet')
    parser.add_argument('--input_folder', required=True,
                        help='Path to the folder with the txt files to translate')
    parser.add_argument('--output_folder', required=True,
                        help='Path to the output folder')

    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print('input folder not found')
        sys.exit(1)
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    execute_folder(args)
    print("Finished!")

