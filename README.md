# Scholarly Publications

A Python script for fetching lists of publications by author using the [Scholarly](https://scholarly.readthedocs.io/en/stable/index.html) library. Deplyment to Azure is handled via the Serverless framework, refer to [Serverless Azure documentation](https://serverless.com/framework/docs/providers/azure/guide/intro/) for more information.

## Publications

The script will upload json files contaning publications data for given authors to a given storage account on Azure. The storage account should have a container with access level: anonymous blob read access. The script is timed to run at 3am BST.

## Set up

The script requires a credentials.json file at project root to hold environment variables. The AUTHOR_IDS string should contain a space separated list of valid Google Scholar author IDs. The container name can be changed to suit the Azure set up of the user.

```
 "CONNECTION_STRING" : "DefaultEndpointsProtocol=https;AccountName=xxxxxx;AccountKey=xxxxxx;EndpointSuffix=core.windows.net",
 "CONTAINER_NAME" :  "author-publications",
 "FUNCTIONS_WORKER_RUNTIME" : "python",
 "AUTHOR_IDS" : "xxxxxx xxxxxx xxxxxx"
```

Read the Azure function logs for queries to Google Scholar

## Deployment

```bash
serverless deploy
```