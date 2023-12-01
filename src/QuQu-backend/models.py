# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class QuquAttributes(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_attributes'


class QuquBrand(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    brands = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_brand'


class QuquCatAttr(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    attribute = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_cat_attr'


class QuquCatAttrEncoding(models.Model):
    row_name = models.TextField(blank=True, null=True)
    col_basic_black = models.TextField(blank=True, null=True)
    col_basic_gray = models.TextField(blank=True, null=True)
    col_basic_white = models.TextField(blank=True, null=True)
    col_dark_blue = models.TextField(blank=True, null=True)
    col_dark_green = models.TextField(blank=True, null=True)
    col_dark_orange = models.TextField(blank=True, null=True)
    col_dark_pink = models.TextField(blank=True, null=True)
    col_dark_purple = models.TextField(blank=True, null=True)
    col_dark_red = models.TextField(blank=True, null=True)
    col_dark_yellow = models.TextField(blank=True, null=True)
    col_grayish_blue = models.TextField(blank=True, null=True)
    col_grayish_green = models.TextField(blank=True, null=True)
    col_grayish_orange = models.TextField(blank=True, null=True)
    col_grayish_pink = models.TextField(blank=True, null=True)
    col_grayish_purple = models.TextField(blank=True, null=True)
    col_grayish_red = models.TextField(blank=True, null=True)
    col_grayish_yellow = models.TextField(blank=True, null=True)
    col_light_blue = models.TextField(blank=True, null=True)
    col_light_green = models.TextField(blank=True, null=True)
    col_light_orange = models.TextField(blank=True, null=True)
    col_light_pink = models.TextField(blank=True, null=True)
    col_light_purple = models.TextField(blank=True, null=True)
    col_light_red = models.TextField(blank=True, null=True)
    col_light_yellow = models.TextField(blank=True, null=True)
    col_vivid_blue = models.TextField(blank=True, null=True)
    col_vivid_green = models.TextField(blank=True, null=True)
    col_vivid_orange = models.TextField(blank=True, null=True)
    col_vivid_pink = models.TextField(blank=True, null=True)
    col_vivid_purple = models.TextField(blank=True, null=True)
    col_vivid_red = models.TextField(blank=True, null=True)
    col_vivid_yellow = models.TextField(blank=True, null=True)
    col_basic_tone = models.TextField(blank=True, null=True)
    col_dark_tone = models.TextField(blank=True, null=True)
    col_grayish_tone = models.TextField(blank=True, null=True)
    col_light_tone = models.TextField(blank=True, null=True)
    col_vivid_tone = models.TextField(blank=True, null=True)
    col_0_1 = models.TextField(blank=True, null=True)
    col_0_135 = models.TextField(blank=True, null=True)
    col_0_136 = models.TextField(blank=True, null=True)
    col_0_137 = models.TextField(blank=True, null=True)
    col_0_141 = models.TextField(blank=True, null=True)
    col_0_142 = models.TextField(blank=True, null=True)
    col_0_145 = models.TextField(blank=True, null=True)
    col_0_146 = models.TextField(blank=True, null=True)
    col_0_147 = models.TextField(blank=True, null=True)
    col_0_163 = models.TextField(blank=True, null=True)
    col_0_2 = models.TextField(blank=True, null=True)
    col_0_225 = models.TextField(blank=True, null=True)
    col_0_251 = models.TextField(blank=True, null=True)
    col_0_254 = models.TextField(blank=True, null=True)
    col_0_275 = models.TextField(blank=True, null=True)
    col_0_278 = models.TextField(blank=True, null=True)
    col_0_3 = models.TextField(blank=True, null=True)
    col_0_6 = models.TextField(blank=True, null=True)
    col_0_7 = models.TextField(blank=True, null=True)
    col_10_100 = models.TextField(blank=True, null=True)
    col_10_101 = models.TextField(blank=True, null=True)
    col_10_102 = models.TextField(blank=True, null=True)
    col_10_103 = models.TextField(blank=True, null=True)
    col_10_104 = models.TextField(blank=True, null=True)
    col_10_105 = models.TextField(blank=True, null=True)
    col_10_106 = models.TextField(blank=True, null=True)
    col_10_108 = models.TextField(blank=True, null=True)
    col_10_109 = models.TextField(blank=True, null=True)
    col_10_112 = models.TextField(blank=True, null=True)
    col_10_113 = models.TextField(blank=True, null=True)
    col_10_114 = models.TextField(blank=True, null=True)
    col_10_119 = models.TextField(blank=True, null=True)
    col_10_120 = models.TextField(blank=True, null=True)
    col_10_121 = models.TextField(blank=True, null=True)
    col_10_127 = models.TextField(blank=True, null=True)
    col_10_128 = models.TextField(blank=True, null=True)
    col_10_129 = models.TextField(blank=True, null=True)
    col_10_130 = models.TextField(blank=True, null=True)
    col_10_133 = models.TextField(blank=True, null=True)
    col_10_135 = models.TextField(blank=True, null=True)
    col_10_137 = models.TextField(blank=True, null=True)
    col_10_140 = models.TextField(blank=True, null=True)
    col_10_141 = models.TextField(blank=True, null=True)
    col_10_142 = models.TextField(blank=True, null=True)
    col_10_145 = models.TextField(blank=True, null=True)
    col_10_147 = models.TextField(blank=True, null=True)
    col_10_148 = models.TextField(blank=True, null=True)
    col_10_149 = models.TextField(blank=True, null=True)
    col_10_150 = models.TextField(blank=True, null=True)
    col_10_151 = models.TextField(blank=True, null=True)
    col_10_153 = models.TextField(blank=True, null=True)
    col_10_154 = models.TextField(blank=True, null=True)
    col_10_155 = models.TextField(blank=True, null=True)
    col_10_225 = models.TextField(blank=True, null=True)
    col_10_229 = models.TextField(blank=True, null=True)
    col_10_234 = models.TextField(blank=True, null=True)
    col_10_235 = models.TextField(blank=True, null=True)
    col_10_254 = models.TextField(blank=True, null=True)
    col_10_258 = models.TextField(blank=True, null=True)
    col_10_260 = models.TextField(blank=True, null=True)
    col_10_262 = models.TextField(blank=True, null=True)
    col_10_264 = models.TextField(blank=True, null=True)
    col_10_265 = models.TextField(blank=True, null=True)
    col_10_266 = models.TextField(blank=True, null=True)
    col_10_268 = models.TextField(blank=True, null=True)
    col_10_275 = models.TextField(blank=True, null=True)
    col_10_278 = models.TextField(blank=True, null=True)
    col_10_281 = models.TextField(blank=True, null=True)
    col_10_95 = models.TextField(blank=True, null=True)
    col_10_96 = models.TextField(blank=True, null=True)
    col_10_98 = models.TextField(blank=True, null=True)
    col_11_field = models.TextField(db_column='col_11_', blank=True, null=True)
    col_11_108 = models.TextField(blank=True, null=True)
    col_11_126 = models.TextField(blank=True, null=True)
    col_11_127 = models.TextField(blank=True, null=True)
    col_11_132 = models.TextField(blank=True, null=True)
    col_11_135 = models.TextField(blank=True, null=True)
    col_11_136 = models.TextField(blank=True, null=True)
    col_11_137 = models.TextField(blank=True, null=True)
    col_11_141 = models.TextField(blank=True, null=True)
    col_11_142 = models.TextField(blank=True, null=True)
    col_11_145 = models.TextField(blank=True, null=True)
    col_11_149 = models.TextField(blank=True, null=True)
    col_11_153 = models.TextField(blank=True, null=True)
    col_11_154 = models.TextField(blank=True, null=True)
    col_11_155 = models.TextField(blank=True, null=True)
    col_11_225 = models.TextField(blank=True, null=True)
    col_11_229 = models.TextField(blank=True, null=True)
    col_11_278 = models.TextField(blank=True, null=True)
    col_12_field = models.TextField(db_column='col_12_', blank=True, null=True)
    col_12_137 = models.TextField(blank=True, null=True)
    col_12_138 = models.TextField(blank=True, null=True)
    col_12_145 = models.TextField(blank=True, null=True)
    col_12_146 = models.TextField(blank=True, null=True)
    col_12_149 = models.TextField(blank=True, null=True)
    col_12_155 = models.TextField(blank=True, null=True)
    col_12_242 = models.TextField(blank=True, null=True)
    col_12_264 = models.TextField(blank=True, null=True)
    col_12_84 = models.TextField(blank=True, null=True)
    col_13_field = models.TextField(db_column='col_13_', blank=True, null=True)
    col_14_field = models.TextField(db_column='col_14_', blank=True, null=True)
    col_15_field = models.TextField(db_column='col_15_', blank=True, null=True)
    col_16_field = models.TextField(db_column='col_16_', blank=True, null=True)
    col_17_field = models.TextField(db_column='col_17_', blank=True, null=True)
    col_18_field = models.TextField(db_column='col_18_', blank=True, null=True)
    col_19_field = models.TextField(db_column='col_19_', blank=True, null=True)
    col_1_0 = models.TextField(blank=True, null=True)
    col_1_10 = models.TextField(blank=True, null=True)
    col_1_11 = models.TextField(blank=True, null=True)
    col_1_114 = models.TextField(blank=True, null=True)
    col_1_116 = models.TextField(blank=True, null=True)
    col_1_12 = models.TextField(blank=True, null=True)
    col_1_13 = models.TextField(blank=True, null=True)
    col_1_135 = models.TextField(blank=True, null=True)
    col_1_136 = models.TextField(blank=True, null=True)
    col_1_137 = models.TextField(blank=True, null=True)
    col_1_14 = models.TextField(blank=True, null=True)
    col_1_141 = models.TextField(blank=True, null=True)
    col_1_142 = models.TextField(blank=True, null=True)
    col_1_145 = models.TextField(blank=True, null=True)
    col_1_146 = models.TextField(blank=True, null=True)
    col_1_147 = models.TextField(blank=True, null=True)
    col_1_16 = models.TextField(blank=True, null=True)
    col_1_2 = models.TextField(blank=True, null=True)
    col_1_254 = models.TextField(blank=True, null=True)
    col_1_266 = models.TextField(blank=True, null=True)
    col_1_273 = models.TextField(blank=True, null=True)
    col_1_278 = models.TextField(blank=True, null=True)
    col_1_281 = models.TextField(blank=True, null=True)
    col_1_8 = models.TextField(blank=True, null=True)
    col_1_9 = models.TextField(blank=True, null=True)
    col_20_field = models.TextField(db_column='col_20_', blank=True, null=True)
    col_21_field = models.TextField(db_column='col_21_', blank=True, null=True)
    col_22_field = models.TextField(db_column='col_22_', blank=True, null=True)
    col_23_field = models.TextField(db_column='col_23_', blank=True, null=True)
    col_24_field = models.TextField(db_column='col_24_', blank=True, null=True)
    col_25_field = models.TextField(db_column='col_25_', blank=True, null=True)
    col_26_field = models.TextField(db_column='col_26_', blank=True, null=True)
    col_27_field = models.TextField(db_column='col_27_', blank=True, null=True)
    col_28_161 = models.TextField(blank=True, null=True)
    col_28_162 = models.TextField(blank=True, null=True)
    col_28_163 = models.TextField(blank=True, null=True)
    col_28_164 = models.TextField(blank=True, null=True)
    col_28_166 = models.TextField(blank=True, null=True)
    col_28_168 = models.TextField(blank=True, null=True)
    col_28_169 = models.TextField(blank=True, null=True)
    col_28_170 = models.TextField(blank=True, null=True)
    col_28_173 = models.TextField(blank=True, null=True)
    col_29_174 = models.TextField(blank=True, null=True)
    col_29_175 = models.TextField(blank=True, null=True)
    col_29_176 = models.TextField(blank=True, null=True)
    col_29_177 = models.TextField(blank=True, null=True)
    col_29_178 = models.TextField(blank=True, null=True)
    col_2_field = models.TextField(db_column='col_2_', blank=True, null=True)
    col_2_135 = models.TextField(blank=True, null=True)
    col_2_136 = models.TextField(blank=True, null=True)
    col_2_137 = models.TextField(blank=True, null=True)
    col_2_145 = models.TextField(blank=True, null=True)
    col_2_146 = models.TextField(blank=True, null=True)
    col_2_147 = models.TextField(blank=True, null=True)
    col_2_225 = models.TextField(blank=True, null=True)
    col_2_254 = models.TextField(blank=True, null=True)
    col_2_264 = models.TextField(blank=True, null=True)
    col_2_265 = models.TextField(blank=True, null=True)
    col_2_281 = models.TextField(blank=True, null=True)
    col_30_field = models.TextField(db_column='col_30_', blank=True, null=True)
    col_31_157 = models.TextField(blank=True, null=True)
    col_31_158 = models.TextField(blank=True, null=True)
    col_31_159 = models.TextField(blank=True, null=True)
    col_31_160 = models.TextField(blank=True, null=True)
    col_31_204 = models.TextField(blank=True, null=True)
    col_31_205 = models.TextField(blank=True, null=True)
    col_31_207 = models.TextField(blank=True, null=True)
    col_31_209 = models.TextField(blank=True, null=True)
    col_31_210 = models.TextField(blank=True, null=True)
    col_31_211 = models.TextField(blank=True, null=True)
    col_31_213 = models.TextField(blank=True, null=True)
    col_31_214 = models.TextField(blank=True, null=True)
    col_31_216 = models.TextField(blank=True, null=True)
    col_32_217 = models.TextField(blank=True, null=True)
    col_32_218 = models.TextField(blank=True, null=True)
    col_32_219 = models.TextField(blank=True, null=True)
    col_32_220 = models.TextField(blank=True, null=True)
    col_32_221 = models.TextField(blank=True, null=True)
    col_32_222 = models.TextField(blank=True, null=True)
    col_32_223 = models.TextField(blank=True, null=True)
    col_32_224 = models.TextField(blank=True, null=True)
    col_33_179 = models.TextField(blank=True, null=True)
    col_33_180 = models.TextField(blank=True, null=True)
    col_33_181 = models.TextField(blank=True, null=True)
    col_33_182 = models.TextField(blank=True, null=True)
    col_33_183 = models.TextField(blank=True, null=True)
    col_33_184 = models.TextField(blank=True, null=True)
    col_33_185 = models.TextField(blank=True, null=True)
    col_33_186 = models.TextField(blank=True, null=True)
    col_33_187 = models.TextField(blank=True, null=True)
    col_33_188 = models.TextField(blank=True, null=True)
    col_33_189 = models.TextField(blank=True, null=True)
    col_33_190 = models.TextField(blank=True, null=True)
    col_33_191 = models.TextField(blank=True, null=True)
    col_33_192 = models.TextField(blank=True, null=True)
    col_33_194 = models.TextField(blank=True, null=True)
    col_33_195 = models.TextField(blank=True, null=True)
    col_33_197 = models.TextField(blank=True, null=True)
    col_33_198 = models.TextField(blank=True, null=True)
    col_33_199 = models.TextField(blank=True, null=True)
    col_33_200 = models.TextField(blank=True, null=True)
    col_33_201 = models.TextField(blank=True, null=True)
    col_33_202 = models.TextField(blank=True, null=True)
    col_33_203 = models.TextField(blank=True, null=True)
    col_34_field = models.TextField(db_column='col_34_', blank=True, null=True)
    col_35_field = models.TextField(db_column='col_35_', blank=True, null=True)
    col_36_field = models.TextField(db_column='col_36_', blank=True, null=True)
    col_37_field = models.TextField(db_column='col_37_', blank=True, null=True)
    col_38_field = models.TextField(db_column='col_38_', blank=True, null=True)
    col_39_field = models.TextField(db_column='col_39_', blank=True, null=True)
    col_3_field = models.TextField(db_column='col_3_', blank=True, null=True)
    col_3_135 = models.TextField(blank=True, null=True)
    col_3_136 = models.TextField(blank=True, null=True)
    col_3_137 = models.TextField(blank=True, null=True)
    col_3_145 = models.TextField(blank=True, null=True)
    col_3_146 = models.TextField(blank=True, null=True)
    col_3_147 = models.TextField(blank=True, null=True)
    col_3_149 = models.TextField(blank=True, null=True)
    col_3_225 = models.TextField(blank=True, null=True)
    col_3_228 = models.TextField(blank=True, null=True)
    col_40_field = models.TextField(db_column='col_40_', blank=True, null=True)
    col_41_field = models.TextField(db_column='col_41_', blank=True, null=True)
    col_42_field = models.TextField(db_column='col_42_', blank=True, null=True)
    col_43_field = models.TextField(db_column='col_43_', blank=True, null=True)
    col_44_field = models.TextField(db_column='col_44_', blank=True, null=True)
    col_45_field = models.TextField(db_column='col_45_', blank=True, null=True)
    col_4_135 = models.TextField(blank=True, null=True)
    col_4_136 = models.TextField(blank=True, null=True)
    col_4_137 = models.TextField(blank=True, null=True)
    col_4_141 = models.TextField(blank=True, null=True)
    col_4_142 = models.TextField(blank=True, null=True)
    col_4_145 = models.TextField(blank=True, null=True)
    col_4_146 = models.TextField(blank=True, null=True)
    col_4_147 = models.TextField(blank=True, null=True)
    col_4_17 = models.TextField(blank=True, null=True)
    col_4_19 = models.TextField(blank=True, null=True)
    col_4_20 = models.TextField(blank=True, null=True)
    col_4_21 = models.TextField(blank=True, null=True)
    col_4_22 = models.TextField(blank=True, null=True)
    col_4_225 = models.TextField(blank=True, null=True)
    col_4_226 = models.TextField(blank=True, null=True)
    col_4_229 = models.TextField(blank=True, null=True)
    col_4_237 = models.TextField(blank=True, null=True)
    col_4_24 = models.TextField(blank=True, null=True)
    col_4_242 = models.TextField(blank=True, null=True)
    col_4_251 = models.TextField(blank=True, null=True)
    col_4_254 = models.TextField(blank=True, null=True)
    col_4_256 = models.TextField(blank=True, null=True)
    col_4_264 = models.TextField(blank=True, null=True)
    col_4_265 = models.TextField(blank=True, null=True)
    col_4_278 = models.TextField(blank=True, null=True)
    col_4_29 = models.TextField(blank=True, null=True)
    col_4_30 = models.TextField(blank=True, null=True)
    col_4_31 = models.TextField(blank=True, null=True)
    col_4_32 = models.TextField(blank=True, null=True)
    col_4_34 = models.TextField(blank=True, null=True)
    col_4_35 = models.TextField(blank=True, null=True)
    col_5_field = models.TextField(db_column='col_5_', blank=True, null=True)
    col_5_135 = models.TextField(blank=True, null=True)
    col_5_136 = models.TextField(blank=True, null=True)
    col_5_141 = models.TextField(blank=True, null=True)
    col_5_142 = models.TextField(blank=True, null=True)
    col_5_145 = models.TextField(blank=True, null=True)
    col_5_146 = models.TextField(blank=True, null=True)
    col_5_147 = models.TextField(blank=True, null=True)
    col_5_225 = models.TextField(blank=True, null=True)
    col_5_229 = models.TextField(blank=True, null=True)
    col_5_242 = models.TextField(blank=True, null=True)
    col_5_251 = models.TextField(blank=True, null=True)
    col_5_254 = models.TextField(blank=True, null=True)
    col_5_264 = models.TextField(blank=True, null=True)
    col_6_125 = models.TextField(blank=True, null=True)
    col_6_127 = models.TextField(blank=True, null=True)
    col_6_128 = models.TextField(blank=True, null=True)
    col_6_132 = models.TextField(blank=True, null=True)
    col_6_135 = models.TextField(blank=True, null=True)
    col_6_136 = models.TextField(blank=True, null=True)
    col_6_137 = models.TextField(blank=True, null=True)
    col_6_141 = models.TextField(blank=True, null=True)
    col_6_142 = models.TextField(blank=True, null=True)
    col_6_143 = models.TextField(blank=True, null=True)
    col_6_153 = models.TextField(blank=True, null=True)
    col_6_154 = models.TextField(blank=True, null=True)
    col_6_155 = models.TextField(blank=True, null=True)
    col_6_230 = models.TextField(blank=True, null=True)
    col_6_234 = models.TextField(blank=True, null=True)
    col_6_250 = models.TextField(blank=True, null=True)
    col_6_251 = models.TextField(blank=True, null=True)
    col_6_254 = models.TextField(blank=True, null=True)
    col_6_278 = models.TextField(blank=True, null=True)
    col_6_36 = models.TextField(blank=True, null=True)
    col_6_37 = models.TextField(blank=True, null=True)
    col_6_38 = models.TextField(blank=True, null=True)
    col_6_39 = models.TextField(blank=True, null=True)
    col_6_40 = models.TextField(blank=True, null=True)
    col_6_41 = models.TextField(blank=True, null=True)
    col_6_42 = models.TextField(blank=True, null=True)
    col_6_43 = models.TextField(blank=True, null=True)
    col_6_44 = models.TextField(blank=True, null=True)
    col_6_46 = models.TextField(blank=True, null=True)
    col_6_49 = models.TextField(blank=True, null=True)
    col_7_135 = models.TextField(blank=True, null=True)
    col_7_136 = models.TextField(blank=True, null=True)
    col_7_137 = models.TextField(blank=True, null=True)
    col_7_142 = models.TextField(blank=True, null=True)
    col_7_143 = models.TextField(blank=True, null=True)
    col_7_148 = models.TextField(blank=True, null=True)
    col_7_149 = models.TextField(blank=True, null=True)
    col_7_150 = models.TextField(blank=True, null=True)
    col_7_151 = models.TextField(blank=True, null=True)
    col_7_230 = models.TextField(blank=True, null=True)
    col_7_234 = models.TextField(blank=True, null=True)
    col_7_251 = models.TextField(blank=True, null=True)
    col_7_253 = models.TextField(blank=True, null=True)
    col_7_254 = models.TextField(blank=True, null=True)
    col_7_278 = models.TextField(blank=True, null=True)
    col_7_50 = models.TextField(blank=True, null=True)
    col_7_52 = models.TextField(blank=True, null=True)
    col_7_55 = models.TextField(blank=True, null=True)
    col_7_58 = models.TextField(blank=True, null=True)
    col_7_59 = models.TextField(blank=True, null=True)
    col_7_60 = models.TextField(blank=True, null=True)
    col_8_118 = models.TextField(blank=True, null=True)
    col_8_120 = models.TextField(blank=True, null=True)
    col_8_121 = models.TextField(blank=True, null=True)
    col_8_123 = models.TextField(blank=True, null=True)
    col_8_127 = models.TextField(blank=True, null=True)
    col_8_128 = models.TextField(blank=True, null=True)
    col_8_129 = models.TextField(blank=True, null=True)
    col_8_133 = models.TextField(blank=True, null=True)
    col_8_141 = models.TextField(blank=True, null=True)
    col_8_142 = models.TextField(blank=True, null=True)
    col_8_148 = models.TextField(blank=True, null=True)
    col_8_149 = models.TextField(blank=True, null=True)
    col_8_150 = models.TextField(blank=True, null=True)
    col_8_151 = models.TextField(blank=True, null=True)
    col_8_152 = models.TextField(blank=True, null=True)
    col_8_153 = models.TextField(blank=True, null=True)
    col_8_154 = models.TextField(blank=True, null=True)
    col_8_155 = models.TextField(blank=True, null=True)
    col_8_229 = models.TextField(blank=True, null=True)
    col_8_230 = models.TextField(blank=True, null=True)
    col_8_235 = models.TextField(blank=True, null=True)
    col_8_238 = models.TextField(blank=True, null=True)
    col_8_251 = models.TextField(blank=True, null=True)
    col_8_254 = models.TextField(blank=True, null=True)
    col_8_257 = models.TextField(blank=True, null=True)
    col_8_258 = models.TextField(blank=True, null=True)
    col_8_260 = models.TextField(blank=True, null=True)
    col_8_262 = models.TextField(blank=True, null=True)
    col_8_268 = models.TextField(blank=True, null=True)
    col_8_275 = models.TextField(blank=True, null=True)
    col_8_278 = models.TextField(blank=True, null=True)
    col_8_281 = models.TextField(blank=True, null=True)
    col_8_62 = models.TextField(blank=True, null=True)
    col_8_64 = models.TextField(blank=True, null=True)
    col_8_65 = models.TextField(blank=True, null=True)
    col_8_67 = models.TextField(blank=True, null=True)
    col_8_68 = models.TextField(blank=True, null=True)
    col_8_69 = models.TextField(blank=True, null=True)
    col_8_70 = models.TextField(blank=True, null=True)
    col_8_71 = models.TextField(blank=True, null=True)
    col_8_72 = models.TextField(blank=True, null=True)
    col_8_74 = models.TextField(blank=True, null=True)
    col_8_75 = models.TextField(blank=True, null=True)
    col_8_77 = models.TextField(blank=True, null=True)
    col_9_135 = models.TextField(blank=True, null=True)
    col_9_136 = models.TextField(blank=True, null=True)
    col_9_137 = models.TextField(blank=True, null=True)
    col_9_142 = models.TextField(blank=True, null=True)
    col_9_145 = models.TextField(blank=True, null=True)
    col_9_147 = models.TextField(blank=True, null=True)
    col_9_149 = models.TextField(blank=True, null=True)
    col_9_151 = models.TextField(blank=True, null=True)
    col_9_152 = models.TextField(blank=True, null=True)
    col_9_153 = models.TextField(blank=True, null=True)
    col_9_154 = models.TextField(blank=True, null=True)
    col_9_155 = models.TextField(blank=True, null=True)
    col_9_225 = models.TextField(blank=True, null=True)
    col_9_226 = models.TextField(blank=True, null=True)
    col_9_228 = models.TextField(blank=True, null=True)
    col_9_229 = models.TextField(blank=True, null=True)
    col_9_242 = models.TextField(blank=True, null=True)
    col_9_264 = models.TextField(blank=True, null=True)
    col_9_275 = models.TextField(blank=True, null=True)
    col_9_278 = models.TextField(blank=True, null=True)
    col_9_79 = models.TextField(blank=True, null=True)
    col_9_80 = models.TextField(blank=True, null=True)
    col_9_81 = models.TextField(blank=True, null=True)
    col_9_82 = models.TextField(blank=True, null=True)
    col_9_83 = models.TextField(blank=True, null=True)
    col_9_84 = models.TextField(blank=True, null=True)
    col_9_85 = models.TextField(blank=True, null=True)
    col_9_86 = models.TextField(blank=True, null=True)
    col_9_92 = models.TextField(blank=True, null=True)
    col_9_93 = models.TextField(blank=True, null=True)
    col_9_94 = models.TextField(blank=True, null=True)
    col_season = models.TextField(blank=True, null=True)
    col_year = models.TextField(blank=True, null=True)
    col_0_21 = models.TextField(blank=True, null=True)
    col_0_271 = models.TextField(blank=True, null=True)
    col_10_110 = models.TextField(blank=True, null=True)
    col_10_111 = models.TextField(blank=True, null=True)
    col_10_116 = models.TextField(blank=True, null=True)
    col_10_117 = models.TextField(blank=True, null=True)
    col_10_146 = models.TextField(blank=True, null=True)
    col_10_152 = models.TextField(blank=True, null=True)
    col_10_239 = models.TextField(blank=True, null=True)
    col_10_255 = models.TextField(blank=True, null=True)
    col_11_103 = models.TextField(blank=True, null=True)
    col_11_128 = models.TextField(blank=True, null=True)
    col_11_148 = models.TextField(blank=True, null=True)
    col_11_234 = models.TextField(blank=True, null=True)
    col_11_251 = models.TextField(blank=True, null=True)
    col_11_254 = models.TextField(blank=True, null=True)
    col_11_264 = models.TextField(blank=True, null=True)
    col_12_234 = models.TextField(blank=True, null=True)
    col_1_1 = models.TextField(blank=True, null=True)
    col_1_149 = models.TextField(blank=True, null=True)
    col_1_258 = models.TextField(blank=True, null=True)
    col_1_7 = models.TextField(blank=True, null=True)
    col_28_167 = models.TextField(blank=True, null=True)
    col_28_179 = models.TextField(blank=True, null=True)
    col_2_149 = models.TextField(blank=True, null=True)
    col_31_146 = models.TextField(blank=True, null=True)
    col_31_208 = models.TextField(blank=True, null=True)
    col_33_135 = models.TextField(blank=True, null=True)
    col_33_146 = models.TextField(blank=True, null=True)
    col_33_193 = models.TextField(blank=True, null=True)
    col_3_153 = models.TextField(blank=True, null=True)
    col_4_116 = models.TextField(blank=True, null=True)
    col_4_148 = models.TextField(blank=True, null=True)
    col_4_235 = models.TextField(blank=True, null=True)
    col_4_275 = models.TextField(blank=True, null=True)
    col_5_11 = models.TextField(blank=True, null=True)
    col_6_126 = models.TextField(blank=True, null=True)
    col_6_262 = models.TextField(blank=True, null=True)
    col_7_141 = models.TextField(blank=True, null=True)
    col_7_53 = models.TextField(blank=True, null=True)
    col_7_54 = models.TextField(blank=True, null=True)
    col_8_108 = models.TextField(blank=True, null=True)
    col_8_114 = models.TextField(blank=True, null=True)
    col_9_150 = models.TextField(blank=True, null=True)
    col_9_17 = models.TextField(blank=True, null=True)
    col_9_254 = models.TextField(blank=True, null=True)
    id = models.AutoField(primary_key=True, blank=True)
    class Meta:
        managed = False
        db_table = 'ququ_cat_attr_encoding'


class QuquCategory(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    id = models.IntegerField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_category'


class QuquCommonAttributes(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    attributes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_common_attributes'

class QuquTrendAttributes(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    attributes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_trend_attributes'

class QuquHue(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    hue_cluster = models.IntegerField(blank=True, null=True)
    top_index = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_hue'


class QuquTone(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    tone_cluster = models.IntegerField(blank=True, null=True)
    top_index = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_tone'


class QuquVogue(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    category = models.IntegerField(blank=True, null=True)
    attributes = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_vogue'

class UserLogs(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    selected_item = models.TextField(blank=True, null=True)
    attributepage = models.TextField(blank=True, null=True)
    attribute_datetime = models.DateTimeField(blank=True, null=True)
    clusterpage = models.TextField(blank=True, null=True)
    cluster_datetime = models.DateTimeField(blank=True, null=True)
    user_correlation = models.TextField(blank=True, null=True)
    correlation_datetime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'user_logs'

class UserStyles(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    image_name_score = models.TextField(blank=True, null=True)
    new_clusterlabel = models.TextField(blank=True, null=True)
    style_name = models.TextField(blank=True, null=True)
    style_datetime  = models.DateTimeField(blank=True, null=True)
    original_name  = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'user_styles'

class ColorLabel(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    RGB = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'color_label'

class ColorLabel2(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    personal_labeling = models.TextField(blank=True, null=True)
    filter_labeling = models.TextField(blank=True, null=True)
    HSV = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'color_label2'

class QuquBrandAtt(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    attribute = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_brand_att'

class QuQuPredefinedStyles(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    image_name_score = models.TextField(blank=True, null=True)
    original_name = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_predefined_styles'

class QuQuVectorEmbedding(models.Model):
    row_name = models.TextField(blank=True, null=True)
    col_0 = models.TextField(blank=True, null=True)
    col_1 = models.TextField(blank=True, null=True)
    col_2 = models.TextField(blank=True, null=True)
    col_3 = models.TextField(blank=True, null=True)
    col_4 = models.TextField(blank=True, null=True)
    col_5 = models.TextField(blank=True, null=True)
    col_6 = models.TextField(blank=True, null=True)
    col_7 = models.TextField(blank=True, null=True)
    col_8 = models.TextField(blank=True, null=True)
    col_9 = models.TextField(blank=True, null=True)
    col_10 = models.TextField(blank=True, null=True)
    col_11 = models.TextField(blank=True, null=True)
    col_12 = models.TextField(blank=True, null=True)
    col_13 = models.TextField(blank=True, null=True)
    col_14 = models.TextField(blank=True, null=True)
    col_15 = models.TextField(blank=True, null=True)
    col_16 = models.TextField(blank=True, null=True)
    col_17 = models.TextField(blank=True, null=True)
    col_18 = models.TextField(blank=True, null=True)
    col_19 = models.TextField(blank=True, null=True)
    col_20 = models.TextField(blank=True, null=True)
    col_21 = models.TextField(blank=True, null=True)
    col_22 = models.TextField(blank=True, null=True)
    col_23 = models.TextField(blank=True, null=True)
    col_24 = models.TextField(blank=True, null=True)
    col_25 = models.TextField(blank=True, null=True)
    col_26 = models.TextField(blank=True, null=True)
    col_27 = models.TextField(blank=True, null=True)
    col_28 = models.TextField(blank=True, null=True)
    col_29 = models.TextField(blank=True, null=True)
    col_30 = models.TextField(blank=True, null=True)
    col_31 = models.TextField(blank=True, null=True)
    col_32 = models.TextField(blank=True, null=True)
    col_33 = models.TextField(blank=True, null=True)
    col_34 = models.TextField(blank=True, null=True)
    col_35 = models.TextField(blank=True, null=True)
    col_36 = models.TextField(blank=True, null=True)
    col_37 = models.TextField(blank=True, null=True)
    col_38 = models.TextField(blank=True, null=True)
    col_39 = models.TextField(blank=True, null=True)
    col_40 = models.TextField(blank=True, null=True)
    col_41 = models.TextField(blank=True, null=True)
    col_42 = models.TextField(blank=True, null=True)
    col_43 = models.TextField(blank=True, null=True)
    col_44 = models.TextField(blank=True, null=True)
    col_45 = models.TextField(blank=True, null=True)
    col_46 = models.TextField(blank=True, null=True)
    col_47 = models.TextField(blank=True, null=True)
    col_48 = models.TextField(blank=True, null=True)
    col_49 = models.TextField(blank=True, null=True)
    col_50 = models.TextField(blank=True, null=True)
    col_51 = models.TextField(blank=True, null=True)
    col_52 = models.TextField(blank=True, null=True)
    col_53 = models.TextField(blank=True, null=True)
    col_54 = models.TextField(blank=True, null=True)
    col_55 = models.TextField(blank=True, null=True)
    col_56 = models.TextField(blank=True, null=True)
    col_57 = models.TextField(blank=True, null=True)
    col_58 = models.TextField(blank=True, null=True)
    col_59 = models.TextField(blank=True, null=True)
    col_60 = models.TextField(blank=True, null=True)
    col_61 = models.TextField(blank=True, null=True)
    col_62 = models.TextField(blank=True, null=True)
    col_63 = models.TextField(blank=True, null=True)
    col_64 = models.TextField(blank=True, null=True)
    col_65 = models.TextField(blank=True, null=True)
    col_66 = models.TextField(blank=True, null=True)
    col_67 = models.TextField(blank=True, null=True)
    col_68 = models.TextField(blank=True, null=True)
    col_69 = models.TextField(blank=True, null=True)
    col_70 = models.TextField(blank=True, null=True)
    col_71 = models.TextField(blank=True, null=True)
    col_72 = models.TextField(blank=True, null=True)
    col_73 = models.TextField(blank=True, null=True)
    col_74 = models.TextField(blank=True, null=True)
    col_75 = models.TextField(blank=True, null=True)
    col_76 = models.TextField(blank=True, null=True)
    col_77 = models.TextField(blank=True, null=True)
    col_78 = models.TextField(blank=True, null=True)
    col_79 = models.TextField(blank=True, null=True)
    col_80 = models.TextField(blank=True, null=True)
    col_81 = models.TextField(blank=True, null=True)
    col_82 = models.TextField(blank=True, null=True)
    col_83 = models.TextField(blank=True, null=True)
    col_84 = models.TextField(blank=True, null=True)
    col_85 = models.TextField(blank=True, null=True)
    col_86 = models.TextField(blank=True, null=True)
    col_87 = models.TextField(blank=True, null=True)
    col_88 = models.TextField(blank=True, null=True)
    col_89 = models.TextField(blank=True, null=True)
    col_90 = models.TextField(blank=True, null=True)
    col_91 = models.TextField(blank=True, null=True)
    col_92 = models.TextField(blank=True, null=True)
    col_93 = models.TextField(blank=True, null=True)
    col_94 = models.TextField(blank=True, null=True)
    col_95 = models.TextField(blank=True, null=True)
    col_96 = models.TextField(blank=True, null=True)
    col_97 = models.TextField(blank=True, null=True)
    col_98 = models.TextField(blank=True, null=True)
    col_99 = models.TextField(blank=True, null=True)
    col_100 = models.TextField(blank=True, null=True)
    col_101 = models.TextField(blank=True, null=True)
    col_102 = models.TextField(blank=True, null=True)
    col_103 = models.TextField(blank=True, null=True)
    col_104 = models.TextField(blank=True, null=True)
    col_105 = models.TextField(blank=True, null=True)
    col_106 = models.TextField(blank=True, null=True)
    col_107 = models.TextField(blank=True, null=True)
    col_108 = models.TextField(blank=True, null=True)
    col_109 = models.TextField(blank=True, null=True)
    col_110 = models.TextField(blank=True, null=True)
    col_111 = models.TextField(blank=True, null=True)
    col_112 = models.TextField(blank=True, null=True)
    col_113 = models.TextField(blank=True, null=True)
    col_114 = models.TextField(blank=True, null=True)
    col_115 = models.TextField(blank=True, null=True)
    col_116 = models.TextField(blank=True, null=True)
    col_117 = models.TextField(blank=True, null=True)
    col_118 = models.TextField(blank=True, null=True)
    col_119 = models.TextField(blank=True, null=True)
    col_120 = models.TextField(blank=True, null=True)
    col_121 = models.TextField(blank=True, null=True)
    col_122 = models.TextField(blank=True, null=True)
    col_123 = models.TextField(blank=True, null=True)
    col_124 = models.TextField(blank=True, null=True)
    col_125 = models.TextField(blank=True, null=True)
    col_126 = models.TextField(blank=True, null=True)
    col_127 = models.TextField(blank=True, null=True)
    col_score = models.TextField(blank=True, null=True)
    col_season = models.TextField(blank=True, null=True)
    col_year = models.TextField(blank=True, null=True)
    col_styles = models.TextField(blank=True, null=True)
    id = models.AutoField(primary_key=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_vector_embedding'

class QuquGeneration(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    option_type = models.TextField(blank=True, null=True)
    style_list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_generation'

class QuquLogs(models.Model):
    index = models.AutoField(primary_key=True, blank=True, null=True)
    user_name = models.TextField(blank=True, null=True)
    toggle = models.TextField(blank=True, null=True)
    season = models.TextField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ququ_logs'

