from django.db import models


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        abstract = True
    NO_SERIALIZE = []
    soft_deleted = models.BooleanField(default=False, blank=True, db_index=True, editable=False)
    enabled = models.BooleanField(default=True, blank=True, db_index=True, editable=False)
    created_date = models.DateTimeField(db_index=True, auto_now_add=True, editable=False, blank=True)
    update_time = models.DateTimeField(editable=False, auto_now=True, blank=True)

    def to_dict(self):
        from flight.utils import to_dict
        return to_dict(self, self.NO_SERIALIZE)
