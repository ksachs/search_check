from abc import ABC, abstractmethod
from structlog import get_logger

class SearchCheckDo(ABC):
    """
    Simple debugger for curation scripts
    https://github.com/inspirehep/curation-scripts
    """

    query = None

    def __init__(self):
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.state = {}
        self.run()


    def perform_test_search(self):
        """Pseudo-search: Read a record from file for testing"""
        import ast
        infile = open("example1.json")
        example = ast.literal_eval(infile.read())
        infile.close()
        result = []
        result.append(example)
        return result


    def perform_inspire_search(self, collection="literature"):
        """Perform the search query on INSPIRE.

        Args:
            collection (str): collection to search in

        Yields:
            the json response for every record.
        """

        import requests
        import time
        INSPIRE_API_ENDPOINT = "https://inspirehep.net/api"

        if self.query is None:
            self.logger.error("`query` needs to be set to a search query")
            return []

        self.logger.info("Searching records %s" % self.query)

        facets = {}
        succeeded = False
        wait = 2
        while not succeeded:
            try:
                response = requests.get(
                    "%s/%s" % (INSPIRE_API_ENDPOINT, collection), 
                    params={"q": self.query},
                    verify=False)

                response.raise_for_status()
                content = response.json()
                succeeded = True
            except:
                wait *= 2
                print('try again in %is...' % (wait))
                time.sleep(wait)


        for result in content["hits"]["hits"]:
            yield result

        while "next" in content.get("links", {}):
            try:
                response = requests.get(content["links"]["next"], verify=False)
                response.raise_for_status()
            except:
                print('try again in 10s...')
                time.sleep(10)
                response = requests.get(content["links"]["next"], verify=False)
                response.raise_for_status()
            content = response.json()

            for result in content["hits"]["hits"]:
                yield result


    def append_item_to_text(self, text, item):
        """Add text representation of an item to the text"""
        if type(item) == int:
            text += '[%s]' % item
        elif text:
            text += '.%s' % item
        else:
            text += '%s' % item
        return text
        
    
    def compare(self, old_record, record):
        """Compare 2 records.
        Return text for differences"""
        from dictdiffer import diff
        difftext = ""
        for update in diff(old_record, record):            
            field_text = ''
            if type(update[1]) == list:
                for item in update[1]:
                    field_text = self.append_item_to_text(field_text, item)
            else:
                field_text = self.append_item_to_text(field_text, update[1])
            if update[0] == 'change':
                difftext += "< %s:%s\n" % (field_text, update[2][0])
                difftext += "> %s:%s\n" % (field_text, update[2][1])
            else:
                if update[0] == 'add':
                    prefix = '+ '
                else:
                    prefix = '- '
                for item in update[2]:
                    difftext += "%s%s:%s\n" % \
                    (prefix,self.append_item_to_text(field_text, item[0]), item[1])
        return difftext


    @abstractmethod
    def check(self, record, logger, state):
        """Check whether the record should be acted upon."""
        pass


    @abstractmethod
    def do(self, record, logger, state):
        """Modify the record metadata."""
        pass


    def run(self):
        """
        Make changes to the records that need them.
        Run read-only
        Write report of changes to logfile
        """
        import copy
        counter = 0
        logfile_name = "my_search_check.log"
        logfile = open(logfile_name, mode='w')
        for result in self.perform_inspire_search():
            record = result['metadata']
            old_record = copy.deepcopy(record)
            recid = record.get('control_number', '000000')
            logfile.write("%4i  %s =============================================\n" % (counter, recid))
            self.logger.info("%4i  %s =============================================" % (counter, recid))
            if not self.check(record, self.logger, self.state):
                logfile.write("Skipped .....\n")
                continue
            self.do(record, self.logger, self.state)
            
            logfile.write(self.compare(old_record, record))
            counter += 1
            if counter > 5:
                break
        self.logger.info('Detailed log in %s' % logfile_name)
