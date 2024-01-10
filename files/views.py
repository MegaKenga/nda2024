from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def get_file(req, id):
    print('file id', id)
    # file = File.obkect.get()
    with open('/Users/vlkromm/code/trainingdjango/media/photo1704632221.jpeg', "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
#
#     return HttpReponse(
#         my_data,
#         headers={
#             "Content-Type": "application/vnd.ms-excel",
#             "Content-Disposition": 'attachment; filename="foo.xls"',
#         },
# )
