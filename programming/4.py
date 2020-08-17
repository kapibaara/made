import re

n = int(input())


def is_closed_tag(tag):
    return tag.find('/') != -1


def remove_non_chars_from_str(s):
    return ''.join([i for i in s if i.isalpha()])


def is_same_tag(tag1, tag2):
    return remove_non_chars_from_str(tag1) == remove_non_chars_from_str(tag2)


def print_almost(tag):
    return print('ALMOST {}'.format(tag.upper()))


def is_correct(tags):
    stack = []

    if len(tags) == 1:
        return print_almost(tags[0])

    unnecessary_tag = None

    for tag in tags:
        if not is_closed_tag(tag):
            stack.append(tag)
            continue

        # обрабатываем закрывающий тег
        if len(stack) < 1:
            if unnecessary_tag is None:
                unnecessary_tag = tag
                continue
            return print('INCORRECT')

        # непустой стек
        last_open_tag = stack.pop()
        # совпадают - убираем последний, открывающий
        if is_same_tag(tag, last_open_tag):
            continue

        # не совпадают и один уже удаляли
        if unnecessary_tag is not None:
            return print('INCORRECT')

        # нужно удалить открывающий если перед ним совпадает с текущим закрывающим
        if len(stack) > 0 and is_same_tag(stack[-1], tag):
            stack.pop()
            unnecessary_tag = last_open_tag
            continue

        stack.append(last_open_tag)
        unnecessary_tag = tag

    if len(stack) == 0:
        if unnecessary_tag is None:
            return print('CORRECT')
        return print_almost(unnecessary_tag)

    if len(stack) == 1 and unnecessary_tag is None:
        return print_almost(stack.pop())

    return print('INCORRECT')


def unique_values(g):
    s = set()
    for x in g:
        if x in s: return False
        s.add(x)
    return True


def is_incorrect_tag(tag):
    if re.search(r'<[^/>][^>]*>', tag) or re.search(r'</[^>]+>', tag):
        return 1
    return 0


def is_incorrect_tags(tags):
    incorrect_tags = list(filter(is_incorrect_tag, tags))

    return len(incorrect_tags) == 0


for i in range(0, n):
    n = int(input())
    tags = []

    for j in range(0, n):
        tags.append(input())

    tags = list(map(lambda s: s.lower(), tags))

    if unique_values(tags):
        is_correct(tags)
