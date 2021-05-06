from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User


class Custom_Group(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Access(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    group = models.ForeignKey(
        Custom_Group, on_delete=models.CASCADE, blank=False, null=False)
    is_staff = models.BooleanField(default=False, blank=False, null=False)
    is_admin = models.BooleanField(default=False, blank=False, null=False)
    is_developper = models.BooleanField(default=False, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Access"

    def __str__(self):
        return self.user.username + ' ' + self.group.name


class Status(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Status"

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)
    end_date = models.DateField(blank=False, null=False)
    priority = models.IntegerField(default=0, validators=[MinValueValidator(
        0), MaxValueValidator(10)], blank=False, null=False)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, blank=False, null=False)
    estimation = models.IntegerField(default=0, validators=[MinValueValidator(
        0), MaxValueValidator(10)], blank=False, null=False)
    parent_task = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    percentage = models.IntegerField(default=0, validators=[MinValueValidator(
        0), MaxValueValidator(100)], blank=False, null=False)
    group = models.ForeignKey(
        Custom_Group, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.name
