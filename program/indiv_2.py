#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import sys
from pathlib import Path


def print_tree(tree, level=0, levels=[]):
    """
    Отрисовка дерева каталогов в виде иерархической структуры.
    """
    if not tree:
        return

    for i, (node, child) in enumerate(tree.items()):
        if i == len(tree) - 1 and level != 0:
            levels[level - 1] = False
        branch = "".join("│   " if lev else "    " for lev in levels[:-1])
        branch += "└── " if i == len(tree) - 1 else "├── "
        if level == 0:
            print(str(node))
        else:
            print(branch + str(node))
        print_tree(child, level + 1, levels + [True])


def tree(directory, all_files):
    """
    Создание структуры дерева каталогов в виде словаря.
    """
    files = 0
    folders = 1
    folder_tree = {}
    for path in sorted(directory.rglob("*")):
        if (not all_files) and (
            any(part.startswith(".") for part in path.parts)
        ):
            continue
        relative_path = path.relative_to(directory)
        parts = relative_path.parts
        current_level = folder_tree

        for part in parts[:-1]:  # Обходим все части пути, кроме последней
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # Добавляем последнюю часть пути (файл или папку)
        if path.is_dir():
            current_level[parts[-1]] = current_level.get(parts[-1], {})
            folders += 1
        else:
            # Или используйте str(path) для хранения полного пути к файлу
            current_level[parts[-1]] = None
            files += 1

    print_tree({directory.name: folder_tree})
    print(f"{files} files, {folders} folders.")


def main(command_line=None):
    """
    Главная функция программы.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", action="store_true", help="All files are printed."
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

    tree(directory, args.a)


if __name__ == "__main__":
    main()
