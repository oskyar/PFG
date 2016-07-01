from django.utils.decorators import method_decorator
from django.views.generic import View
from guardian.decorators import permission_required


def cbv_permission_required(*args, **kwargs):
    def decorator(original_class):
        if not issubclass(original_class, View):
            raise TypeError('%(class)s is not a view class' % {
                'class': original_class
            })

        original_class.dispatch = method_decorator(
            permission_required(*args, **kwargs)
        )(original_class.dispatch)

        return original_class

    return decorator


def cbv_permission_required_or_403(*args, **kwargs):
    kwargs['return_403'] = True
    return cbv_permission_required(*args, **kwargs)
