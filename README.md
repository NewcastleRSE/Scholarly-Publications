# Scholarly Publications

A Python script for fetching lists of publications by author using the [Scholarly](https://scholarly.readthedocs.io/en/stable/index.html) library. Deplyment to Azure is handled via the Serverless framework, refer to [Serverless Azure documentation](https://serverless.com/framework/docs/providers/azure/guide/intro/) for more information.

## Publications

The function is called via `/api/publications?authorID=XXXXXXXXX` providing a valid Google Scholar author ID as a required query parameter.

```bash
/api/publications?authorID=z6jaMRcAAAAJ
``` 

## Offline Testing

Ensure all dependencies are installed with using whatever Python setup you have such as `venv` or global installation.

```bash
serverless offline
```

Watch the logs for the URL for each function to be printed.

## Deployment

```bash
serverless deploy
```