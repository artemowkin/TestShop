import simplejson as json
from simplejson.errors import JSONDecodeError

from django.views import View
from django.http import JsonResponse, Http404

from .services import CreateReviewService


class AddProductReviewView(View):

    def post(self, request, product_pk):
        service = CreateReviewService()
        try:
            json_request = json.loads(request.body)
        except JSONDecodeError:
            raise Http404

        created_review = service.create(
            product_pk, request.user,
            json_request['rating'], json_request['text']
        )
        serialized_review = self._serialize_review(created_review)
        return JsonResponse(serialized_review, status=201)

    def _serialize_review(self, review):
        return {
            'user': self.request.user.username, 'rating': review.rating,
            'text': review.text
        }

