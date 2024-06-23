from django.db import models

class SpGoodsPics(models.Model):
    pics_id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField(blank=True, null=True)
    # 写上upload_to，后面指定一个路径，那么将来上传的文件会直接生成到配置文件中的那个medias文件夹中的img文件夹中，
    # 不需要我们自己写读取文件内容写入本地文件的操作，django内部帮我们自动处理了
    img = models.ImageField(upload_to='upload',null=True)
    is_temp = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'sp_goods_pics'

class SpGoodsCats(models.Model):
    cat_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    cat_name = models.CharField(max_length=50)
    is_show = models.IntegerField()
    cat_sort = models.IntegerField()
    data_flag = models.IntegerField()
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sp_goods_cats'

class SpGoodsAttr(models.Model):
    goods_id = models.PositiveIntegerField()
    attr_id = models.PositiveSmallIntegerField()
    attr_value = models.TextField()
    add_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_goods_attr'

# Create your models here.
class SpGoods(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(unique=True, max_length=255)
    goods_price = models.DecimalField(max_digits=10, decimal_places=2)
    goods_number = models.PositiveIntegerField()
    goods_weight = models.PositiveSmallIntegerField()
    cat_id = models.PositiveSmallIntegerField()
    goods_introduce = models.TextField(blank=True, null=True)
    goods_big_logo = models.CharField(max_length=128)
    goods_small_logo = models.CharField(max_length=128)
    is_del = models.CharField(max_length=1)
    add_time = models.IntegerField()
    upd_time = models.IntegerField()
    delete_time = models.IntegerField(blank=True, null=True)
    cat_one_id = models.SmallIntegerField(blank=True, null=True)
    cat_two_id = models.SmallIntegerField(blank=True, null=True)
    cat_three_id = models.SmallIntegerField(blank=True, null=True)
    hot_mumber = models.PositiveIntegerField(blank=True, null=True)
    is_promote = models.SmallIntegerField(blank=True, null=True)
    goods_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_goods'


class SpGoodsCats(models.Model):
    cat_id = models.AutoField(primary_key=True)
    parent_id = models.IntegerField()
    cat_name = models.CharField(max_length=50)
    is_show = models.IntegerField()
    cat_sort = models.IntegerField()
    data_flag = models.IntegerField()
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sp_goods_cats'
class SpCategory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=255, blank=True, null=True)
    cat_pid = models.IntegerField(blank=True, null=True)
    cat_level = models.IntegerField(blank=True, null=True)
    cat_deleted = models.IntegerField(blank=True, null=True)
    cat_icon = models.CharField(max_length=255, blank=True, null=True)
    cat_src = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_category'

class RegisterUserinfo(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'register_userinfo'


class SpAttribute(models.Model):
    attr_id = models.PositiveSmallIntegerField(primary_key=True)
    attr_name = models.CharField(max_length=32)
    cat_id = models.PositiveSmallIntegerField()
    attr_sel = models.CharField(max_length=4)
    attr_write = models.CharField(max_length=6)
    attr_vals = models.TextField()
    delete_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sp_attribute'
