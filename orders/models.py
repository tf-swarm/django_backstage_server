from django.db import models

# Create your models here.
class SpOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField()
    order_number = models.CharField(unique=True, max_length=32)
    order_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_pay = models.CharField(max_length=1)
    is_send = models.CharField(max_length=1)
    trade_no = models.CharField(max_length=32)
    order_fapiao_title = models.CharField(max_length=2)
    order_fapiao_company = models.CharField(max_length=32)
    order_fapiao_content = models.CharField(max_length=32)
    consignee_addr = models.TextField()
    pay_status = models.CharField(max_length=1)
    create_time = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sp_order'


class SpOrderGoods(models.Model):
    order_id = models.PositiveIntegerField()
    goods_id = models.PositiveIntegerField()
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_number = models.IntegerField()
    goods_total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'sp_order_goods'


class SpReport1(models.Model):
    rp1_user_count = models.IntegerField(blank=True, null=True)
    rp1_area = models.CharField(max_length=128, blank=True, null=True)
    rp1_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_report_1'
