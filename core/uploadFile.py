from . import ingest
from . import helper

class UploadFile:
    def __init__(self, file):
        self.helper = helper.helper.Helper()
        self.file = file
        self.contentType = "application/pdf"
        self.filePath = f"{'core/docs'}/{file}"
        self.fileProcessor = ingest.FileProcessor(self.filePath)

    def get_document_splits(self):
        files = []
        files = self.fileProcessor.process(self.contentType)
        return files

    def getTempFilePath(self, file):
        return self.helper.createFile(file)
