from django.core.files.storage import FileSystemStorage

from nda.settings import TEMPORARY_UPLOAD_ROOT


temporary_storage = FileSystemStorage(location=TEMPORARY_UPLOAD_ROOT)
