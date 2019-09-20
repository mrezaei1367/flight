import random
import string
from datetime import datetime
from django.db.models import Model
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


def to_dict(obj, except_fields=[]):
    result = {}
    for field in obj._meta.fields:
        name = field.name
        val = getattr(obj, name, None)
        if name not in except_fields and type(val) not in [ForwardManyToOneDescriptor]:
            if isinstance(val, Model):
                val = val.id
                name += '_id'
            elif type(val).__name__ == 'ImageFieldFile':
                try:
                    val = val.path
                except ValueError:
                    val = None
            elif type(val).__name__ == 'datetime':
                val = val.timestamp()
            elif type(val).__name__ == 'date':
                val = datetime(val.year, val.month, val.day).timestamp()
            elif type(val).__name__ == 'time':
                val = val.isoformat()
            result.update({name: val})
    return result

def random_string(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))