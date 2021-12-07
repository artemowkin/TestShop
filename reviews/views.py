import simplejson as json

from django.views import View
from django.http import JsonResponse, Http404

from .services import CreateReviewService


class AddProductReviewView(View):

    def post(self, request, product_pk):
        self._check_is_request_ajax()
        service = CreateReviewService()
        json_request = json.loads(request.body)
        created_review = service.create(
            json_request['product'], json_request['user'],
            json_request['rating'], json_request['text']
        )
        serialized_review = self._serialize_review(created_review)
        return JsonResponse(serialized_review, status=201)

    def _check_is_request_ajax(self):
        request_content_type = self.request.headers.get('Content-Type')
        if request_content_type != 'application/json':
            raise Http404

    def _serialize_review(self, review):
        return {
            'user': self.request.user.username, 'rating': review.rating,
            'text': review.text
        }

