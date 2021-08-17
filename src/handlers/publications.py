import logging
import jsonpickle
import sys

from scholarly import scholarly
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    authorID = req.params.get('authorID')
    if not authorID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            authorID = req_body.get('authorID')

    if authorID:
        author = scholarly.search_author_id(authorID)
        author = scholarly.fill(author, sections=['publications'])

        # Uncomment below to get full publication data - hits scholarly harder and can cause IP to be blocked
        # publications = []

        # for publication in author['publications']:
        #     try:
        #         publications.append(scholarly.fill(publication))
        #         logging.info('Added publication to list')
        #     except: # catch all exceptions
        #         e = sys.exc_info()[0]
        #         logging.error(f' error doing query{e}')

        return func.HttpResponse(jsonpickle.encode(author))
    else:
        return func.HttpResponse(
             "Please pass a authorID on the query string or in the request body",
             status_code=400
        )
