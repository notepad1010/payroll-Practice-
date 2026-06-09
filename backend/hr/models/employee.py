from django.db import models
from .position import Position
from .department import Department

class Employee(models.Model):
     
     CIVIL_STATUS = [
            ('SINGLE','Single'),
            ('MARRIED','Married'),
            ('WIDOWED','Widowed'),
            ('SEPARATED','Separated'),
     ]

     EMPLOYEE_STATUS = [
          ('REGULAR', 'Regular'),
          ('CONTRACTUAL', 'Contractual'),
          ('PROBATIONARY', 'Probationary'),
          ('PART_TIME', 'Part_time')
     ]

     first_name = models.CharField(max_length=45)
     last_name = models.CharField(max_length=45)
     birth_date = models.DateField()
     address = models.CharField(max_length=255)

     civil_status = models.CharField(max_length=10,
                                     choices=CIVIL_STATUS,
                                     default='SINGLE')
     
     phone_number = models.CharField(max_length=15)
     personal_email = models.EmailField(max_length=255)
     employment_status = models.CharField(max_length=20,
                                         choices=EMPLOYEE_STATUS,
                                         default= 'PROBATIONARY')
     
     position = models.ForeignKey(Position,
                                   on_delete=models.SET_NULL,
                                     null= True,
                                     related_name= 'employees')
     
     department = models.ForeignKey(Department,
                                     on_delete=models.SET_NULL,
                                       null= True,
                                         related_name='employees')
     hire_date = models.DateField()
     supervisor = models.ForeignKey('self',
                                     on_delete=models.SET_NULL,
                                       null = True,
                                       blank=True,
                                       related_name='subordinates')
     is_active = models.BooleanField(default=True)
     photo_path = models.CharField(max_length=250,blank=True)
     create_at = models.DateTimeField(auto_now_add=True)
     update_at = models.DateTimeField(auto_now=True)

     def __str__(self):
           return f"{self.first_name} {self.last_name}"
     
     @property
     def full_name(self):
          return f"{self.first_name} {self.last_name}"

     class Meta:
        db_table = 'employee'