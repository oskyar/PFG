from vanilla import TemplateView
from django.core.exceptions import PermissionDenied
from django.shortcuts import (
    render_to_response
)
from django.template import RequestContext


class Error404(TemplateView):
    template_name = "404.html"


class Error403(TemplateView):
    template_name = "403.html"


class Error500(TemplateView):
    template_name = "500.html"


def permission_denied(request):
    response = render_to_response(
        '403.html',
        context_instance=RequestContext(request)
    )

    response.status_code = 403

    return response
