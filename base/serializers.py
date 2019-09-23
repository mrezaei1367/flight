import six
from rest_framework.serializers import SerializerMetaclass, BaseSerializer
from rest_framework.exceptions import ValidationError


@six.add_metaclass(SerializerMetaclass)
class ErrorHandlerSerializerMixin(BaseSerializer):
    UNCATEGORIZED_ERRORS = 0
    NON_FIELD_ERRORS = 1
    SPECIAL_FIELD_ERRORS = 2

    VALIDATION_ERRORS_STATUS_CODE = {
        'uncategorized_errors': UNCATEGORIZED_ERRORS,
        'non_field_errors': NON_FIELD_ERRORS,  # No related to special field value pattern or type
        'field_errors': SPECIAL_FIELD_ERRORS  # Error Related to Special Field
    }

    def normalize_errors(self, errors):
        detail = []
        for key, value in errors.detail.items():
            error_code = ""
            error_detail = value[0].__str__()
            detail.append({
                'error_status': self.VALIDATION_ERRORS_STATUS_CODE.get(key, self.UNCATEGORIZED_ERRORS),
                'error_code': error_code,
                'detail': error_detail
            })

            try:
                request = self.context['request']
                detail[-1]['source'] = {'pointer': '%s%s' % (request.get_host(), request.path)}
            except KeyError:
                pass

            if detail[-1]['error_status'] == self.UNCATEGORIZED_ERRORS and key in self.fields:
                detail[-1]['error_status'] = self.SPECIAL_FIELD_ERRORS
                source = detail[-1].get('source', {})
                source.update(related_field=key)
                detail[-1]['source'] = source
        return ValidationError({'errors': detail})

    def is_valid(self, raise_exception=False):
        try:
            res = super(ErrorHandlerSerializerMixin, self).is_valid(raise_exception)
            return res
        except ValidationError as e:
            raise self.normalize_errors(e)
        except AssertionError as e:
            if type(getattr(e, 'args')[0]) is ValidationError:
                raise self.normalize_errors(ValidationError({'': [e.args[0].args[0]]}))
            else:
                raise e


class BaseSerializer(ErrorHandlerSerializerMixin):
    pass
