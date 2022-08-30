from django.db import models
from django.contrib.auth.models import AbstractUser

from .utilities import get_timestamp_path

class Bb(models.Model):
	rubric = models.ForeignKey('SubRubric', on_delete=models.PROTECT, verbose_name='Рубрика')
	title = models.CharField(max_length=40, verbose_name='Товар')
	content = models.TextField(verbose_name='Описание')
	price = models.IntegerField(default=0, verbose_name='Цена')
	contacts = models.TextField(verbose_name='Контакты')
	image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')
	author = models.ForeignKey('AdvUser', on_delete=models.CASCADE, verbose_name='Автор')
	is_active = models.BooleanField(default=True, db_index=True, verbose_name='Выводить в списке?')
	created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Опубликовано')

	def delete(self, *args, **kwargs):
		for ai in self.additionalimage_set.all():
			ai.delete()
		super().delete(*args, **kwargs)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Объявление'
		verbose_name_plural = 'Объявления'
		ordering = ['-created_at']

class AdditionalImage(models.Model):
	bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
	image = models.ImageField(upload_to=get_timestamp_path)

	class Meta:
		verbose_name = 'Дополнительное изображение'
		verbose_name_plural = 'Дополнительные изображения'

class AdvUser(AbstractUser):
	is_activated = models.BooleanField(default=True,
									db_index=True,
									verbose_name='Прошёл активацию?'
									)
	send_messages = models.BooleanField(default=True,
										db_index=True,
										verbose_name='Отправлять сообщения')

	def delete(self, *args, **kwargs):
		for bb in self.bb_set.all():
			bb.delete()
		super().delete(*args, **kwargs)

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'

class Rubric(models.Model):
	name = models.CharField(max_length=20, db_index=True, verbose_name='Название', unique=True)
	order = models.IntegerField(default=0, db_index=True, verbose_name='Порядок')
	super_rubric = models.ForeignKey('SuperRubric',blank=True, on_delete=models.PROTECT, verbose_name='Надрубрика', null=True)

class SuperRubricManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
	objects = SuperRubricManager()

	def __str__(self):
		return self.name

	class Meta:
		proxy = True
		ordering = ('order', 'name')
		verbose_name = 'Надрубрика'
		verbose_name_plural = 'Надрубрики'

class SubRubricManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
	objects = SubRubricManager()

	def __str__(self):
		return f'{self.super_rubric.name} - {self.name}'
		# return '%s - %s' % (self.super_rubric.name, self.name)

	class Meta:
		proxy = True
		ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
		verbose_name = 'Подрубрика'
		verbose_name_plural = 'Подрубрики'

