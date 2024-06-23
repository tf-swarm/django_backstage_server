from django.db import models

# Create your models here.


class SpManager(models.Model):
    mg_id = models.AutoField(primary_key=True)
    mag_name = models.CharField(max_length=32)
    mg_pwd = models.CharField(max_length=128)
    mg_time = models.PositiveIntegerField()
    role_id = models.IntegerField()
    mg_mobile = models.CharField(max_length=32, blank=True, null=True)
    mg_email = models.CharField(max_length=64, blank=True, null=True)
    mg_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_manager'


class SpPermission(models.Model):
    ps_id = models.PositiveSmallIntegerField(primary_key=True)
    ps_name = models.CharField(max_length=20)
    ps_pid = models.PositiveSmallIntegerField()
    ps_c = models.CharField(max_length=32)
    ps_a = models.CharField(max_length=32)
    ps_level = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'sp_permission'


class SpPermissionApi(models.Model):
    ps = models.OneToOneField(SpPermission, models.CASCADE)
    ps_api_service = models.CharField(max_length=255, blank=True, null=True)
    ps_api_action = models.CharField(max_length=255, blank=True, null=True)
    ps_api_path = models.CharField(max_length=255, blank=True, null=True)
    ps_api_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_permission_api'


class SpRole(models.Model):
    role_id = models.PositiveSmallIntegerField(primary_key=True)
    role_name = models.CharField(max_length=20)
    ps_ids = models.CharField(max_length=512)
    ps_ca = models.TextField(blank=True, null=True)
    role_desc = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_role'

