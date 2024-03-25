#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sys
from pathlib import Path

from colorama import Fore, Style


def print_tree(tree, lines, level=0, levels=[]):
    """
    Отрисовка дерева каталогов в виде иерархической структуры.
    """
    if not tree:
        return

    for i, (node, child) in enumerate(tree.items()):
        if i == len(tree) - 1 and level != 0:
            levels[level - 1] = False
        if not lines:
            branch = "".join("│   " if lev else "    " for lev in levels[:-1])
            branch += "└── " if i == len(tree) - 1 else "├── "
        else:
            branch = ""
        if level == 0:
            # Синий цвет для корневой папки
            print(Fore.BLUE + str(node) + Style.RESET_ALL)
        else:
            # Для файлов: зеленый цвет, для папок: желтый цвет
            color = Fore.GREEN if child is not None else Fore.YELLOW
            print(branch + color + str(node) + Style.RESET_ALL)

        print_tree(child, lines, level + 1, levels + [True])


def tree(directory, args):
    """
    Создание структуры дерева каталогов в виде словаря.
    """

    sw = False
    files = 0
    folders = 0
    folder_tree = {}

    path_list = sorted(
        [
            path
            for index, path in enumerate(directory.rglob("*"))
            if index < 1000
        ]
    )

    for path in path_list:
        if (not args.a) and (any(part.startswith(".") for part in path.parts)):
            continue
        relative_path = path.relative_to(directory)
        parts = relative_path.parts

        if args.f:
            path_work = relative_path
        else:
            path_work = Path(relative_path.name)
        current_level = folder_tree
        p = Path()
        for part in parts[:-1]:
            if args.f:
                p = p / part
            else:
                p = Path(part)
            current_level = current_level[p]

        if path.is_dir():
            current_level[path_work] = current_level.get(path_work, {})
            folders += 1
        elif not args.d:
            current_level[path_work] = None
            files += 1
        if folders + files >= 1000:
            sw = True
            break
    print_tree({directory.name: folder_tree}, args.i)
    if sw:
        print(Fore.RED, "Показаны только 1000 элементов.", Style.RESET_ALL)
    print(
        Fore.YELLOW,
        files,
        Style.RESET_ALL,
        "files, ",
        Fore.GREEN,
        folders,
        Style.RESET_ALL,
        "folders.",
    )


def main(command_line=None):
    """
    Главная функция программы.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", action="store_true", help="All files are printed."
    )
    parser.add_argument(
        "-d", action="store_true", help="Print directories only."
    )
    parser.add_argument("-f", action="store_true", help="Print relative path.")
    parser.add_argument(
        "-i",
        action="store_true",
        help="Tree does not print the indentation lines."
        " Useful when used in conjunction with the -f option.",
    )
    parser.add_argument(
        "directory", nargs="?", default=".", help="Directory to scan."
    )
    args = parser.parse_args(command_line)

    try:
        directory = Path(args.directory).resolve(strict=True)
    except FileNotFoundError:
        print(f"Directory '{Path(args.directory).resolve()}' does not exist.")
        sys.exit(1)

    tree(directory, args)


if __name__ == "__main__":
    main()
