def check_title(work, row):
    titles = work.title.split('|')

    title_exists = False
    for title in titles:
        if title == row[0]:
            title_exists = True

    if not title_exists:
        work.title += '|' + row[0]
        work.save()