from django.db import models

# Create your models here.

class User(models.Model):
	name=models.CharField(max_length=30,primary_key=True)
	def __unicode__(self):
		return self.name

class Data(models.Model):
	name= models.ForeignKey(User)
	item = models.CharField(max_length=30)
	e1=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e2=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e3=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e4=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e5=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e6=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e7=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e8=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e9=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e10=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e11=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e12=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e13=models.DecimalField(max_digits=14, decimal_places=8, null=True)
	e14=models.DecimalField(max_digits=14, decimal_places=8, null=True)
