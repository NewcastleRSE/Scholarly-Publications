import logging
import jsonpickle
import sys
import json
import os
import time

from scholarly import scholarly
import azure.functions as func


author_list = ['GjSCPJ0AAAAJ', '_NdzLicAAAAJ', 'ujbju80AAAAJ', 'z6jaMRcAAAAJ', 'NVBSg9gAAAAJ', 'oAjiq3QAAAAJ', '5ydGTN0AAAAJ', 'UeMGAaAAAAAJ', 'WqH63QAAAAJ', 'dH4219oAAAAJ', '2Kcd0zoAAAAJ', '4zjd8H8AAAAJ', 'akdJAsEAAAAJ'] 

def isAvailable(publication, pub_attribute):
    try:
        publication[pub_attribute]
        publication = publication[pub_attribute]
        return publication
    except:
        return "Unavailable" 

def isAvailableInBib(publication, pub_attribute):
    try:
        publication['bib'][pub_attribute]
        publication = publication['bib'][pub_attribute]
        return publication
    except:
        return "Unavailable" 



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    local_path = "./data"

    # make directory if it doesn't exist
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # loop through the author list
    for each_author in author_list:

        authorID = each_author
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
            #publications = []

            #for publication in author['publications']:
                #try:
                    #publications.append(scholarly.fill(publication))
                    #logging.info('Added publication to list')
                #except: # catch all exceptions
                    #e = sys.exc_info()[0]
                    #logging.error(f' error doing query{e}')

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
            volume = ""
            number = ""
            pages = ""
            publisher = ""

            # loop through publications creating a dict each time, then add to pubs_list 
            for publication in a_publications:

                title = isAvailableInBib(publication, 'title')    
                author_pub_id = isAvailable(publication, 'author_pub_id')
                num_citations = isAvailable(publication, 'num_citations')
                pub_url = isAvailable(publication, 'pub_url')
                pub_year = isAvailableInBib(publication, 'pub_year')
                author = isAvailableInBib(publication, 'author')
                journal = isAvailableInBib(publication, 'journal')
                volume = isAvailableInBib(publication, 'volume')
                number = isAvailableInBib(publication, 'number')
                pages = isAvailableInBib(publication, 'pages')
                publisher = isAvailableInBib(publication, 'publisher')
                abstract = isAvailableInBib(publication, 'abstract')

                pub_dict = {
                    "title" : title,
                    "pub_year" : pub_year,
                    "author_pub_id" : author_pub_id,
                    "num_citations" : num_citations,
                    "pub_url" : pub_url, 
                    "author" : author,
                    "journal" : journal,
                    "volume" : volume,
                    "number" : number,
                    "pages" : pages,
                    "publisher" : publisher,
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
            authorfile = open("data/" + filename + "_" + a_authorID + ".json", "a") 

            try:
                authorfile.write(json.dumps(author_dict))
            
            except: 
                e = sys.exc_info()[0]
                logging.error(f' error writing to file{e}')

            finally:
                authorfile.close()

            #return func.HttpResponse(jsonpickle.encode(filename))
       # else:
           # return func.HttpResponse(
              #  "Please pass a authorID on the query string or in the request body",
              #  status_code=400
          #  )
    time.sleep(2)

    return func.HttpResponse( 
            "All authors complete",
            status_code=200
    )        
            

