#from inspirehep.curation.search_check_do import SearchCheckDo
from my_search_check_do import SearchCheckDo

class MyCustomAction(SearchCheckDo):
    """Explain what this does."""

    # Literature is default, ``search_class`` needs to be set for other
    # collections
    # search_class = LiteratureSearch

    # a custom query, like "t electron"
    query = "recid 1896542"


    @staticmethod
    def check(record, logger, state):
        # Use ``record`` to check if it needs to be modified, return True if
        # so. Optionally use ``logger`` to log additional info and ``state`` to
        # transmit some data to the ``do`` step.

        state['author_position'] = []
        for na, author in enumerate(record.get('authors', [])):
            logger.info('Checking author %s' % author.get('full_name', 'NN'))
            for aff in author.get('affiliations', []):
                if aff.get('value', "") == "Saga U., Japan":
                    state['author_position'].append(na)
                    logger.info('Will delete author # %s:  %s' % \
                        (na, author.get('full_name', 'NN')))

        if state['author_position']:
            return True

        return False


    @staticmethod
    def do(record, logger, state):
        # Mutate ``record`` to make modifications.
        # Optionally use ``logger`` to log additional info and ``state`` to
        # retrieve some data to the ``do`` step.

        position_list = state['author_position']
        position_list.reverse()
        for na in position_list:
            record['authors'].pop(na)

        if 'report_numbers' in record:
            record['report_numbers'].append({'value':'DESY-1234', 'source':'curator'})

        try:
            record['references'][5]['reference']['publication_info']['journal_title'] = 'JHEP'
        except:
            logger.info('No reference to replace')


MyCustomAction()
