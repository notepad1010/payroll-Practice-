from django.db import models
from .department import Department


class Position(models.Model):
    position_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department,
                                    on_delete=models.CASCADE,
                                    related_name='positions')
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.position_name
    
    class Meta:
      db_table = 'position'