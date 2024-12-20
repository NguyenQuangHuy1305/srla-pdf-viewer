import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient
import os

app = func.FunctionApp()

@app.route(route="documents/{document_title}", auth_level=func.AuthLevel.FUNCTION)
def get_pdf(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Get document title from route parameter
        document_title = req.route_params.get('document_title')
        if not document_title:
            return func.HttpResponse(
                "Please provide a document title in the URL.",
                status_code=400
            )

        # Get blob storage connection string from environment variable
        connection_string = os.environ["AzureWebJobsStorage"]
        container_name = os.environ["FOO_CONTAINER_NAME"]

        # Initialize the blob service client
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(document_title)

        # Download the PDF
        pdf_content = blob_client.download_blob().readall()

        # Return the PDF with appropriate headers
        return func.HttpResponse(
            pdf_content,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={document_title}",
                "Access-Control-Allow-Origin": "*"  # Enable CORS
            }
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )