from .models import Contributor, Source

# Helpful functionalities

def check_title(work, input_title):
    """
    :param work: Piece of work in which we add new titles
    :param input_title: title to check

    Checks if the input title is new for the work. In that case, it adds it to the titles attribute.
    """

    titles = work.title.split('|')

    title_exists = False
    for title in titles:
        if title == input_title:
            title_exists = True

    if not title_exists:
        work.title += '|' + input_title
        work.save()

def add_relations(work, input_contributors=None, input_source=None):
    """
        :param work: Piece of work in which we add new contributors and sources
        :input_contributors: contributors to check
        :input_: contributors to check
    """

    if input_contributors:
        ## Extracts contributors
        contributors = []

        # Reads each contributor, creates it if it does not exist
        for name in input_contributors.split('|'):
            contributor, contributor_created = Contributor.objects.get_or_create(
                name=name
            )

            contributors.append(contributor)

        # Refreshes song contributors if needed
        if len(contributors) > 0:
            work.contributors.add(*contributors)
    
    # Reads source and id_source, creates it if it does not exist
    source, source_created = Source.objects.get_or_create(
        name=input_source[0],
        id_source=int(input_source[1])
    )
    
    # Assigns song to source
    source.work = work
    source.save()