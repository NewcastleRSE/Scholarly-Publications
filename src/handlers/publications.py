import logging
import jsonpickle
import sys
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()

from azure.storage.blob import BlobClient
from scholarly import scholarly
import azure.functions as func

# get author list from environment variable
raw_author_list = os.getenv('AUTHOR_IDS')
author_list = raw_author_list.split()

def isAvailable(publication, pub_attribute):
    try:
        publication[pub_attribute]
        return publication[pub_attribute]
    except:
        return "Unavailable" 

def isAvailableInBib(publication, pub_attribute):
    try:
        publication['bib'][pub_attribute]
        return publication['bib'][pub_attribute]
    except:
        return "Unavailable" 

def inAuthor(author, attribute):
    try:
        author[attribute]
        return author[attribute]
    except:
        return "Unavailable" 


# function run by serverless timer every 24 hours
def main(context, myTimer):

    # loop through the author list
    for each_author in author_list:

        authorID = each_author
        logging.info(authorID)
        
        if authorID:
            author = scholarly.search_author_id(authorID)
            author = scholarly.fill(author, sections=['publications'])

            # Uncomment below to get full publication data - hits scholarly harder and can cause IP to be blocked
            publications = []

            for publication in author['publications']:
                try:
                    publications.append(scholarly.fill(publication))
                    logging.info('Added publication to list')
                except: # catch all exceptions
                    e = sys.exc_info()[0]
                    logging.error(f' error doing query{e}')
                    
        
            a_name = inAuthor(author, 'name')
            a_affiliation = inAuthor(author, 'affiliation')
            a_authorID = inAuthor(author, 'scholar_id')
            a_publications = inAuthor(author, 'publications')

            pubs_list = []
           
            try:
                a_publications

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
                complete_fn = filename + "_" + a_authorID + ".json" 
            
                try:

                    output = json.dumps(author_dict)

                    # Create a blob client using the local file name as the name for the blob
                    blob = BlobClient.from_connection_string(conn_str=os.getenv('CONNECTION_STRING'), container_name=os.getenv('CONTAINER_NAME'), blob_name=complete_fn)
                  
                    print("\nUploading to Azure Storage as blob:\n\t" + complete_fn)
                    blob.upload_blob(output, overwrite=True)    
                
                except: 
                    e = sys.exc_info()[0]
                    logging.error(f' error writing to file{e}')     

            except:
                logging.error(f'publications error')

        
    time.sleep(1)

   
            

