from django.db import models


# Create your models here.

class DataInfo(models.Model):
    skuID = models.CharField(max_length=12, db_index=True)
    XGB_data = models.CharField(max_length=50, null=True)
    LGB_data = models.CharField(max_length=50, null=True)
    FLGB_data = models.CharField(max_length=50, null=True)
    FXGB_data = models.CharField(max_length=50, null=True)
    FLR_data = models.CharField(max_length=50, null=True)
    SVM_data = models.CharField(max_length=50, null=True)
    LR_data = models.CharField(max_length=50, null=True)
    real_data = models.CharField(max_length=50, null=True)


# class IDInfo(models.Model):
#     goods_id = models.CharField(max_length=12, db_index=True)
#     sku_id = models.CharField(max_length=50, db_index=True)
