import logging
import jsonpickle
import sys
import json

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

        a_name = author['name']
        a_affiliation = author['affiliation'] 
        a_authorID = author['scholar_id']
        a_publications = author['publications']

        pubs_list = []
        title = ""
        author_pub_id = ""
        num_citations = ""
        pub_year = ""
        pub_url = ""
        author = ""
        journal = ""
        abstract = ""

        # loop through publications creating a dict each time, then add to pubs_list 
        for publication in a_publications:

            try:
                publication['bib']['title']
                title = publication['bib']['title']
            except:
                title = "Unavailable" 

            try:
                publication['author_pub_id']
                author_pub_id = publication['author_pub_id']
            except:
                title = "Unavailable"  
     
            try:
                publication['num_citations']
                num_citations = publication['num_citations']
            except:
                num_citations = "Unavailable"   

            try:
                publication['bib']['pub_year']
                pub_year = publication['bib']['pub_year']
            except:
                pub_year = "Unavailable" 

            try:
                publication['pub_url']
                pub_url = publication['pub_url']
            except:
                pub_url = "Unavailable" 

            try:
                publication['bib']['author']
                author = publication['bib']['author']
            except:
                author = "Unavailable"  

            try:
                publication['bib']['journal']
                journal = publication['bib']['journal']
            except:
                journal = "Unavailable"

            try:
                publication['bib']['abstract']
                abstract = publication['bib']['abstract']
            except:
                abstract = "Unavailable"       

            pub_dict = {
                "title" : title,
                "pub_year" : pub_year,
                "author_pub_id" : author_pub_id,
                "num_citations" : num_citations,
                "pub_url" : pub_url, 
                "author" : author,
                "journal" : journal,
                "abstract" : abstract
            }
            pubs_list.append(pub_dict.copy())

            
        # create another dict including the pubs_list
        author_dict = {
            "name" : a_name,
            "affiliation" : a_affiliation,
            "authorID" : a_authorID,
            "publications" : pubs_list
        }

        # create suitable author filename
        filename = a_name.replace(" ", "_").lower()
        authorfile = open(filename + ".json", "a") 

        try:
            authorfile.write(json.dumps(author_dict))
           
        except: 
            e = sys.exc_info()[0]
            logging.error(f' error writing to file{e}')

        finally:
            authorfile.close()

        #return func.HttpResponse(jsonpickle.encode(a_publications))
        return func.HttpResponse(jsonpickle.encode(filename))
    else:
        return func.HttpResponse(
             "Please pass a authorID on the query string or in the request body",
             status_code=400
        )

#def isAvailable(publication, pub_attribute):
    #  try:
    #    publication[pub_attribute]
    #    publication = publication[pub_attribute]
    #    return publication
    #  except:
    #    return "Unavailable"                
