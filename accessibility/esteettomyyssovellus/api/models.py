# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete`
#   set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create,
#   modify, and delete the table
# Feel free to rename the models, but don't rename db_table values
#   or field names.
from django.db import models


class ArBackendCopyableEntrance(models.Model):
    entrance_id = models.BigIntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    copyable_entrance_id = models.BigIntegerField(blank=True, null=True)
    copyable_servicepoint_name = models.CharField(
        max_length=500, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_copyable_entrance'


class ArBackendEntranceAnswer(models.Model):
    technical_id = models.CharField(max_length=500, null=False,
                                    primary_key=True)
    log_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    form_submitted = models.CharField(null=True, max_length=1)
    question_block_id = models.IntegerField(blank=True, null=True)
    question_id = models.BigIntegerField(blank=True, null=True)
    question_choice_id = models.BigIntegerField(blank=True, null=True)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)
    comment_fi = models.CharField(max_length=500, blank=True, null=True)
    comment_sv = models.CharField(max_length=500, blank=True, null=True)
    comment_en = models.CharField(max_length=500, blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    photo_text_fi = models.CharField(max_length=500, blank=True, null=True)
    photo_text_sv = models.CharField(max_length=500, blank=True, null=True)
    photo_text_en = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_entrance_answer'


class ArBackendEntrancePhoto(models.Model):
    technical_id = models.CharField(max_length=500, null=False,
                                    primary_key=True)
    log_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    form_submitted = models.CharField(null=True, max_length=1)
    question_id = models.BigIntegerField(blank=True, null=True)
    photo_number = models.BigIntegerField(blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    photo_text_fi = models.CharField(max_length=500, blank=True, null=True)
    photo_text_sv = models.CharField(max_length=500, blank=True, null=True)
    photo_text_en = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_entrance_photo'


class ArBackendForm(models.Model):
    form_id = models.IntegerField(blank=True, null=True)
    language_id = models.BigIntegerField(blank=True, null=True)
    text = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    guide_title = models.CharField(max_length=200, blank=True, null=True)
    guide_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_form'


class ArBackendQuestion(models.Model):
    technical_id = models.TextField(primary_key=True)
    form_id = models.IntegerField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    question_id = models.IntegerField(blank=True, null=True)
    question_code = models.CharField(max_length=20, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    visible_if_question_choice = models.CharField(
        max_length=100, blank=True, null=True)
    question_level = models.SmallIntegerField(blank=True, null=True)
    question_order_text = models.CharField(
        max_length=99, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    photo_text = models.CharField(max_length=2000, blank=True, null=True)
    yes_no_question = models.CharField(max_length=1, blank=True, null=True)
    can_add_location = models.CharField(max_length=1, blank=True, null=True)
    can_add_photo_max_count = models.IntegerField(blank=True, null=True)
    can_add_comment = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_question'


class ArBackendQuestionBlock(models.Model):
    technical_id = models.TextField(primary_key=True)
    form_id = models.IntegerField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    question_block_code = models.CharField(max_length=1, blank=True, null=True)
    text = models.CharField(max_length=1, blank=True, null=True)
    visible_if_question_choice = models.TextField(blank=True, null=True)
    question_block_order_text = models.CharField(
        max_length=99, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    photo_text = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_question_block'


class ArBackendQuestionChoice(models.Model):
    technical_id = models.TextField(primary_key=True)
    form_id = models.IntegerField(blank=True, null=True)
    language_id = models.IntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    question_id = models.IntegerField(blank=True, null=True)
    question_choice_id = models.BigIntegerField(blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    choice_order_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_backend_question_choice'


class ArEntrance(models.Model):
    entrance_id = models.BigAutoField(primary_key=True)
    name_fi = models.CharField(max_length=500, blank=True, null=True)
    name_sv = models.CharField(max_length=500, blank=True, null=True)
    name_en = models.CharField(max_length=500, blank=True, null=True)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    streetview_url = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField()
    created_by = models.CharField(max_length=50)
    modified = models.DateTimeField()
    modified_by = models.CharField(max_length=50)
    is_main_entrance = models.CharField(max_length=1)
    servicepoint = models.ForeignKey('ArServicepoint', models.DO_NOTHING)
    form = models.ForeignKey('ArForm', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ar_entrance'


class ArExternalServicepoint(models.Model):
    external_servicepoint_id = models.CharField(max_length=100)
    system = models.ForeignKey('ArSystem', models.DO_NOTHING)
    servicepoint = models.ForeignKey('ArServicepoint', models.DO_NOTHING)
    created = models.DateTimeField()
    id = models.BigAutoField(primary_key=True)
    created_by = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ar_external_servicepoint'
        unique_together = (('external_servicepoint_id', 'system'),
                           ('servicepoint', 'system'),)


class ArForm(models.Model):
    form_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ar_form'


class ArFormLanguage(models.Model):
    form_language_id = models.BigAutoField(primary_key=True)
    form = models.ForeignKey(ArForm, models.DO_NOTHING)
    language = models.ForeignKey('ArLanguage', models.DO_NOTHING)
    main_topic = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    guide_title = models.CharField(max_length=200, blank=True, null=True)
    guide_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_form_language'


class ArFormText(models.Model):
    form = models.OneToOneField(ArForm, models.DO_NOTHING, primary_key=True)
    language = models.ForeignKey('ArLanguage', models.DO_NOTHING)
    title = models.CharField(max_length=100)
    info = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'ar_form_text'
        unique_together = (('form', 'language'),)


class ArLanguage(models.Model):
    language_id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ar_language'


class ArRest01AccessVariable(models.Model):
    variable_id = models.IntegerField(blank=True, null=False, primary_key=True)
    variable_name = models.CharField(max_length=99, blank=True, null=True)
    values_data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_access_variable'


class ArRest01AccessViewpoint(models.Model):
    viewpoint_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=False,
        primary_key=True)
    name_fi = models.TextField(blank=True, null=True)
    name_sv = models.TextField(blank=True, null=True)
    name_en = models.TextField(blank=True, null=True)
    values_data = models.TextField(blank=True, null=True)
    viewpoint_order = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_access_viewpoint'


class ArRest01Entrance(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    is_main_entrance = models.CharField(max_length=1, blank=True, null=True)
    name_fi = models.CharField(max_length=500, blank=True, null=True)
    name_sv = models.CharField(max_length=500, blank=True, null=True)
    name_en = models.CharField(max_length=500, blank=True, null=True)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)
    photo_url = models.CharField(max_length=500, blank=True, null=True)
    streetview_url = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    sentences_created = models.DateTimeField(blank=True, null=True)
    sentences_created_by = models.TextField(blank=True, null=True)
    sentences_modified = models.DateTimeField(blank=True, null=True)
    sentences_modified_by = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_entrance'


class ArRest01EntranceAccessibility(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)
    variable_name = models.CharField(max_length=99, blank=True, null=True)
    value_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    rest_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_entrance_accessibility'


class ArRest01Reportshortage(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    viewpoint_id = models.IntegerField(blank=True, null=True)
    is_indoor_servicepoint = models.CharField(
        max_length=1, blank=True, null=True)
    evaluation_zone = models.TextField(blank=True, null=True)
    easy_to_fix = models.TextField(blank=True, null=True)
    requirement_id = models.IntegerField(blank=True, null=True)
    requirement_text = models.CharField(max_length=1000, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=1000, blank=True, null=True)
    shortage_fi = models.CharField(max_length=1000, blank=True, null=True)
    shortage_sv = models.CharField(max_length=1000, blank=True, null=True)
    shortage_en = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_reportshortage'


class ArRest01Reportsummary(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    is_accessible = models.TextField(blank=True, null=True)
    shortage_count = models.BigIntegerField(blank=True, null=True)
    shortage_count_easy_to_fix = models.BigIntegerField(blank=True, null=True)
    wheel_is_accessible = models.TextField(blank=True, null=True)
    wheel_shortage_count = models.BigIntegerField(
        blank=True, null=True)
    wheel_shortage_count_easy_to_fix = models.BigIntegerField(
        blank=True, null=True)
    wheel_shortage_count_outside = models.BigIntegerField(
        blank=True, null=True)
    wheel_shortage_count_entrance = models.BigIntegerField(
        blank=True, null=True)
    wheel_shortage_count_inside = models.BigIntegerField(blank=True, null=True)
    visual_is_accessible = models.TextField(blank=True, null=True)
    visual_shortage_count = models.BigIntegerField(
        blank=True, null=True)
    visual_shortage_count_easy_to_fix = models.BigIntegerField(
        blank=True, null=True)
    visual_shortage_count_outside = models.BigIntegerField(
        blank=True, null=True)
    visual_shortage_count_entrance = models.BigIntegerField(
        blank=True, null=True)
    visual_shortage_count_inside = models.BigIntegerField(
        blank=True, null=True)
    hearing_is_accessible = models.TextField(blank=True, null=True)
    toilet_is_accessible = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_reportsummary'


class ArRest01Requirement(models.Model):
    requirement_id = models.IntegerField(blank=True, null=False,
                                         primary_key=True)
    requirement_text = models.TextField(blank=True, null=True)
    is_indoor_requirement = models.TextField(blank=True, null=True)
    evaluation_zone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_requirement'


class ArRest01Sentence(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    log_id = models.BigIntegerField(blank=True, null=True)
    sentence_group_id = models.SmallIntegerField(blank=True, null=True)
    sentence_group_fi = models.CharField(max_length=255, blank=True, null=True)
    sentence_group_sv = models.CharField(max_length=255, blank=True, null=True)
    sentence_group_en = models.CharField(max_length=255, blank=True, null=True)
    sentence_id = models.IntegerField(blank=True, null=True)
    sentence_order_text = models.TextField(blank=True, null=True)
    sentence_fi = models.CharField(max_length=4000, blank=True, null=True)
    sentence_sv = models.CharField(max_length=4000, blank=True, null=True)
    sentence_en = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_sentence'


class ArRest01Servicepoint(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    servicepoint_name = models.CharField(
        max_length=500, blank=True, null=True)
    address_street_name = models.CharField(
        max_length=100, blank=True, null=True)
    address_no = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=100, blank=True, null=True)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)
    accessibility_phone = models.CharField(
        max_length=250, blank=True, null=True)
    accessibility_email = models.CharField(
        max_length=250, blank=True, null=True)
    accessibility_www = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=50, blank=True, null=True)
    entrances = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_servicepoint'


class ArRest01ServicepointAccessibility(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)
    variable_name = models.CharField(max_length=99, blank=True, null=True)
    value_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    rest_value = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_servicepoint_accessibility'


class ArRest01Shortage(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    viewpoint_id = models.IntegerField(blank=True, null=True)
    requirement_id = models.IntegerField(blank=True, null=True)
    shortage_fi = models.CharField(max_length=1000, blank=True, null=True)
    shortage_sv = models.CharField(max_length=1000, blank=True, null=True)
    shortage_en = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_shortage'


class ArRest01Summary(models.Model):
    system_id = models.UUIDField(blank=True, null=True)
    external_servicepoint_id = models.CharField(
        max_length=100, blank=True, null=True)
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    viewpoint_id = models.IntegerField(blank=True, null=True)
    is_accessible = models.TextField(blank=True, null=True)
    shortage_count = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_rest01_summary'


class ArServicepoint(models.Model):
    servicepoint_id = models.BigAutoField(primary_key=True)
    business_id = models.CharField(max_length=9, blank=True, null=True)
    organisation_code = models.CharField(max_length=50, blank=True, null=True)
    system_id_old = models.CharField(max_length=50, blank=True, null=True)
    servicepoint_name = models.CharField(max_length=500, blank=True, null=True)
    ext_servicepoint_id = models.CharField(max_length=50)
    created = models.DateTimeField()
    created_by = models.CharField(max_length=50)
    modified = models.DateTimeField()
    modified_by = models.CharField(max_length=50)
    address_street_name = models.CharField(
        max_length=100, blank=True, null=True)
    address_no = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(
        max_length=100, blank=True, null=True)
    accessibility_phone = models.CharField(
        max_length=250, blank=True, null=True)
    accessibility_email = models.CharField(
        max_length=250, blank=True, null=True)
    accessibility_www = models.CharField(max_length=250, blank=True, null=True)
    is_searchable = models.CharField(max_length=1)
    organisation_id = models.UUIDField(blank=True, null=True)
    system = models.ForeignKey(
        'ArSystem', models.DO_NOTHING, blank=True, null=True)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)
    location_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_servicepoint'
        unique_together = (('business_id', 'system_id_old',
                            'ext_servicepoint_id'),
                           ('ext_servicepoint_id', 'system'),)


class ArSystem(models.Model):
    system_id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=100)
    checksum_secret = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'ar_system'


class ArSystemForm(models.Model):
    system = models.OneToOneField(
        ArSystem, models.DO_NOTHING, primary_key=True)
    form = models.ForeignKey(ArForm, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ar_system_form'
        unique_together = (('system', 'form'),)


class ArXAccessibilityReqIn(models.Model):
    accessibility_case_proto_id = models.IntegerField()
    requirement_id = models.IntegerField()
    subcondition_id = models.IntegerField()
    rest_variable_id = models.IntegerField()
    condition_type = models.CharField(max_length=1)
    rest_value = models.CharField(max_length=99)
    accessibility_case_names = models.CharField(
        max_length=1000, blank=True, null=True)
    accessibility_fault_title = models.CharField(
        max_length=255, blank=True, null=True)
    bits_qrs = models.CharField(max_length=20, blank=True, null=True)
    requirement_text = models.CharField(
        max_length=1000, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=255, blank=True, null=True)
    effort_to_fix = models.CharField(max_length=10, blank=True, null=True)
    shortcoming_fi = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_sv = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_accessibility_req_in'


class ArXAccessibilityRequirement(models.Model):
    accessibility_case_proto_id = models.IntegerField()
    requirement_id = models.IntegerField()
    subcondition_id = models.IntegerField()
    rest_variable_id = models.IntegerField()
    condition_type = models.CharField(max_length=1)
    rest_value = models.CharField(max_length=99)
    accessibility_case_names = models.CharField(
        max_length=1000, blank=True, null=True)
    accessibility_fault_title = models.CharField(
        max_length=255, blank=True, null=True)
    bits_qrs = models.CharField(
        max_length=20, blank=True, null=True)
    requirement_text = models.CharField(max_length=1000, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=255, blank=True, null=True)
    effort_to_fix = models.CharField(max_length=10, blank=True, null=True)
    shortcoming_fi = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_sv = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_accessibility_requirement'
        unique_together = (('accessibility_case_proto_id', 'requirement_id',
                            'subcondition_id',
                            'rest_variable_id',
                            'condition_type', 'rest_value'),)


class ArXAnswerLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    entrance = models.ForeignKey(ArEntrance, models.DO_NOTHING)
    ip_address = models.CharField(
        max_length=255, blank=True, null=True)
    started_answering = models.DateTimeField(blank=True, null=True)
    finished_answering = models.DateTimeField(blank=True, null=True)
    form_submitted = models.CharField(
        max_length=1, blank=True, null=True)
    form_cancelled = models.CharField(
        max_length=1, blank=True, null=True)
    accessibility_editor = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_answer_log'


class ArXQuestion(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_block = models.ForeignKey('ArXQuestionBlock', models.DO_NOTHING)
    form_id = models.IntegerField()
    question_code = models.CharField(
        max_length=20, blank=True, null=True)
    question_order_text = models.CharField(
        max_length=99, blank=True, null=True)
    question_level = models.SmallIntegerField(blank=True, null=True)
    question_text = models.CharField(max_length=2000, blank=True, null=True)
    question_active = models.CharField(max_length=1, blank=True, null=True)
    question_description = models.CharField(
        max_length=2000, blank=True, null=True)
    question_url = models.CharField(max_length=255, blank=True, null=True)
    question_url_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question'


class ArXQuestionAnswer(models.Model):
    log = models.OneToOneField(
        ArXAnswerLog, models.DO_NOTHING, primary_key=True)
    question_choice = models.ForeignKey(
        'ArXQuestionChoice', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ar_x_question_answer'
        unique_together = (('log', 'question_choice'),)


class ArXQuestionAnswerComment(models.Model):
    answer_comment_id = models.BigAutoField(primary_key=True)
    log = models.ForeignKey(ArXAnswerLog, models.DO_NOTHING)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    comment = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_answer_comment'


class ArXQuestionAnswerLocation(models.Model):
    answer_location_id = models.BigAutoField(primary_key=True)
    log = models.ForeignKey(ArXAnswerLog, models.DO_NOTHING)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    loc_easting = models.IntegerField(blank=True, null=True)
    loc_northing = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_answer_location'


class ArXQuestionAnswerPhoto(models.Model):
    answer_photo_id = models.BigAutoField(primary_key=True)
    log = models.ForeignKey(ArXAnswerLog, models.DO_NOTHING)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    photo_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_answer_photo'


class ArXQuestionAnswerPhotoTxt(models.Model):
    answer_photo_txt_id = models.BigAutoField(primary_key=True)
    answer_photo = models.ForeignKey(ArXQuestionAnswerPhoto, models.DO_NOTHING)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    photo_text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_answer_photo_txt'


class ArXQuestionBlock(models.Model):
    question_block_id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    question_block_code = models.CharField(
        max_length=20, blank=True, null=True)
    question_block_order_text = models.CharField(
        max_length=99, blank=True, null=True)
    question_block_name = models.CharField(
        max_length=255, blank=True, null=True)
    question_block_active = models.CharField(
        max_length=1, blank=True, null=True)
    question_block_decription = models.CharField(
        max_length=2000, blank=True, null=True)
    question_block_url = models.CharField(
        max_length=255, blank=True, null=True)
    question_block_url_text = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_block'


class ArXQuestionBlockDependency(models.Model):
    question_block = models.OneToOneField(
        ArXQuestionBlock, models.DO_NOTHING, primary_key=True)
    condition_type = models.CharField(max_length=1)
    condition_question_choice = models.ForeignKey(
        'ArXQuestionChoice', models.DO_NOTHING)
    condition_question_id = models.IntegerField()
    condition_choice_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ar_x_question_block_dependency'
        unique_together = (('question_block', 'condition_question_choice'),
                           ('question_block', 'condition_question_id',
                            'condition_choice_id'),)


class ArXQuestionBlockDesc(models.Model):
    question_block_desc_id = models.BigAutoField(primary_key=True)
    question_block = models.ForeignKey(ArXQuestionBlock, models.DO_NOTHING)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    description = models.CharField(max_length=2000, blank=True, null=True)
    photo_text = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_block_desc'


class ArXQuestionBlockDescPhoto(models.Model):
    question_block_desc_photo_id = models.BigAutoField(primary_key=True)
    question_block = models.ForeignKey(ArXQuestionBlock, models.DO_NOTHING)
    photo_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_block_desc_photo'


class ArXQuestionBlockLanguage(models.Model):
    question_block = models.OneToOneField(
        ArXQuestionBlock, models.DO_NOTHING, primary_key=True)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_block_language'
        unique_together = (('question_block', 'language'),)


class ArXQuestionChoice(models.Model):
    question_choice_id = models.BigIntegerField(primary_key=True)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    choice_id = models.IntegerField()
    choice_text = models.CharField(max_length=255, blank=True, null=True)
    choice_order_text = models.CharField(max_length=255, blank=True, null=True)
    searchword_fi = models.CharField(max_length=255, blank=True, null=True)
    searchword_sv = models.CharField(max_length=255, blank=True, null=True)
    searchword_en = models.CharField(max_length=255, blank=True, null=True)
    not_searchword_fi = models.CharField(max_length=255, blank=True, null=True)
    not_searchword_sv = models.CharField(max_length=255, blank=True, null=True)
    not_searchword_en = models.CharField(max_length=255, blank=True, null=True)
    rest_variable_id_1 = models.IntegerField(blank=True, null=True)
    rest_value_1 = models.CharField(max_length=255, blank=True, null=True)
    rest_variable_id_2 = models.IntegerField(blank=True, null=True)
    rest_value_2 = models.CharField(max_length=255, blank=True, null=True)
    rest_variable_id_3 = models.IntegerField(blank=True, null=True)
    rest_value_3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_choice'
        unique_together = (('question', 'choice_id'),)


class ArXQuestionChoiceLanguage(models.Model):
    question_choice = models.OneToOneField(
        ArXQuestionChoice, models.DO_NOTHING, primary_key=True)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    text = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_choice_language'
        unique_together = (('question_choice', 'language'),)


class ArXQuestionChoicePlus(models.Model):
    question_choice_id = models.IntegerField(blank=True, null=True)
    question_id = models.IntegerField(blank=True, null=True)
    choice_id = models.IntegerField(blank=True, null=True)
    choice_text = models.CharField(max_length=255, blank=True, null=True)
    choice_order_text = models.CharField(max_length=40, blank=True, null=True)
    searchword_fi = models.CharField(max_length=99, blank=True, null=True)
    searchword_sv = models.CharField(max_length=20, blank=True, null=True)
    searchword_en = models.CharField(max_length=40, blank=True, null=True)
    not_searchword_fi = models.CharField(max_length=40, blank=True, null=True)
    not_searchword_sv = models.CharField(max_length=20, blank=True, null=True)
    not_searchword_en = models.CharField(max_length=20, blank=True, null=True)
    rest_variable_id_1 = models.IntegerField(blank=True, null=True)
    rest_value_1 = models.CharField(max_length=99, blank=True, null=True)
    rest_variable_id_2 = models.IntegerField(blank=True, null=True)
    rest_value_2 = models.CharField(max_length=99, blank=True, null=True)
    rest_variable_id_3 = models.IntegerField(blank=True, null=True)
    rest_value_3 = models.CharField(max_length=99, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_choice_plus'


class ArXQuestionDependency(models.Model):
    question = models.OneToOneField(
        ArXQuestion, models.DO_NOTHING, primary_key=True)
    condition_type = models.CharField(max_length=1)
    condition_question_choice = models.ForeignKey(
        ArXQuestionChoice, models.DO_NOTHING)
    condition_question_id = models.IntegerField()
    condition_choice_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ar_x_question_dependency'
        unique_together = (('question', 'condition_question_choice'),
                           ('question', 'condition_question_id',
                            'condition_choice_id'),)


class ArXQuestionDesc(models.Model):
    question_desc_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    description = models.CharField(max_length=2000, blank=True, null=True)
    photo_text = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_desc'


class ArXQuestionDescPhoto(models.Model):
    question_desc_photo_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    photo_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_desc_photo'


class ArXQuestionExtradata(models.Model):
    question_extradata_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(ArXQuestion, models.DO_NOTHING)
    can_add_location = models.CharField(max_length=1, blank=True, null=True)
    can_add_photo_max_count = models.IntegerField(blank=True, null=True)
    can_add_comment = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_extradata'


class ArXQuestionLanguage(models.Model):
    question = models.OneToOneField(
        ArXQuestion, models.DO_NOTHING, primary_key=True)
    language = models.ForeignKey(ArLanguage, models.DO_NOTHING)
    text = models.CharField(max_length=2000, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_question_language'
        unique_together = (('question', 'language'),)


class ArXRestVariable(models.Model):
    rest_variable_id = models.IntegerField(unique=True, blank=True, null=True)
    rest_variable_name = models.CharField(max_length=99, blank=True, null=True)
    rest_variable_explanation = models.CharField(
        max_length=99, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_rest_variable'


class ArXRestVariablePlus(models.Model):
    rest_variable_id = models.IntegerField(blank=True, null=True)
    rest_variable_name = models.CharField(
        max_length=240, blank=True, null=True)
    rest_variable_explanation = models.CharField(
        max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_rest_variable_plus'


class ArXSentence(models.Model):
    sentence_id = models.IntegerField(primary_key=True)
    question_block_id = models.IntegerField()
    sentence_order_text = models.CharField(
        max_length=10, blank=True, null=True)
    sentence_active = models.CharField(max_length=1, blank=True, null=True)
    sentence_criteria = models.CharField(max_length=255, blank=True, null=True)
    sentence_fi = models.CharField(max_length=2000, blank=True, null=True)
    sentence_sv = models.CharField(max_length=2000, blank=True, null=True)
    sentence_en = models.CharField(max_length=2000, blank=True, null=True)
    sentence_group_id = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_sentence'


class ArXSentenceGroup(models.Model):
    sentence_group_id = models.SmallIntegerField(primary_key=True)
    sentence_group_fi = models.CharField(max_length=255, blank=True, null=True)
    sentence_group_sv = models.CharField(max_length=255, blank=True, null=True)
    sentence_group_en = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_sentence_group'


class ArXStoredEntranceAnswer(models.Model):
    entrance_id = models.BigIntegerField()
    question_id = models.IntegerField()
    choice_id = models.IntegerField()
    stored = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_stored_entrance_answer'
        unique_together = (('entrance_id', 'question_id', 'choice_id'),)


class ArXStoredSentence(models.Model):
    entrance_id = models.BigIntegerField()
    log_id = models.BigIntegerField()
    sentence_group_id = models.SmallIntegerField()
    sentence_group_fi = models.CharField(max_length=255)
    question_block_id = models.IntegerField()
    question_block_name = models.CharField(max_length=255)
    sentence_id = models.IntegerField()
    sentence_order_text = models.CharField(max_length=20)
    sentence_fi = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_stored_sentence'


class ArXStoredSentenceLang(models.Model):
    entrance_id = models.BigIntegerField()
    log_id = models.BigIntegerField()
    language_code = models.CharField(max_length=3)
    sentence_group_id = models.SmallIntegerField()
    sentence_group_name = models.CharField(max_length=255)
    question_block_id = models.IntegerField()
    question_block_name = models.CharField(max_length=255)
    sentence_id = models.IntegerField()
    sentence_order_text = models.CharField(max_length=20)
    sentence = models.CharField(max_length=4000, blank=True, null=True)
    stored = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_stored_sentence_lang'
        unique_together = (
            ('entrance_id', 'log_id', 'language_code', 'sentence_id'),)


class ArXStoredShortageHelper(models.Model):
    servicepoint_id = models.BigIntegerField()
    viewpoint_id = models.IntegerField()
    requirement_id = models.IntegerField()
    requirement_text = models.CharField(
        max_length=1000, blank=True, null=True)
    is_indoor_servicepoint = models.CharField(
        max_length=1, blank=True, null=True)
    evaluation_subject = models.CharField(
        max_length=1, blank=True, null=True)
    big_flag = models.CharField(max_length=1, blank=True, null=True)
    ok_flag = models.CharField(max_length=1, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=1000, blank=True, null=True)
    shortage_fi = models.CharField(max_length=1000, blank=True, null=True)
    shortage_sv = models.CharField(max_length=1000, blank=True, null=True)
    shortage_en = models.CharField(max_length=1000, blank=True, null=True)
    stored = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_x_stored_shortage_helper'
        unique_together = (
            ('servicepoint_id', 'viewpoint_id', 'requirement_id'),)


class ArXViewAccessReqQuickReport(models.Model):
    accessibility_case_id = models.IntegerField(blank=True, null=True)
    requirement_id = models.IntegerField(blank=True, null=True)
    subcondition_id = models.IntegerField(blank=True, null=True)
    rest_variable_id = models.IntegerField(blank=True, null=True)
    condition_type = models.CharField(max_length=1, blank=True, null=True)
    rest_value = models.CharField(max_length=99, blank=True, null=True)
    requirement_text = models.CharField(max_length=1000, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=255, blank=True, null=True)
    effort_to_fix = models.CharField(max_length=10, blank=True, null=True)
    shortcoming_fi = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_sv = models.CharField(max_length=255, blank=True, null=True)
    shortcoming_en = models.CharField(max_length=255, blank=True, null=True)
    evaluation_subject = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_access_req_quick_report'


class ArXViewAccessibilityOut(models.Model):
    question_id = models.IntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    question_code = models.TextField(blank=True, null=True)
    question_order_text = models.TextField(blank=True, null=True)
    question_level = models.SmallIntegerField(blank=True, null=True)
    question_text = models.TextField(blank=True, null=True)
    question_active = models.TextField(blank=True, null=True)
    question_description = models.TextField(blank=True, null=True)
    question_url = models.TextField(blank=True, null=True)
    question_url_text = models.TextField(blank=True, null=True)
    dep = models.TextField(blank=True, null=True)
    choice01 = models.TextField(blank=True, null=True)
    choice02 = models.TextField(blank=True, null=True)
    choice03 = models.TextField(blank=True, null=True)
    choice04 = models.TextField(blank=True, null=True)
    choice05 = models.TextField(blank=True, null=True)
    choice06 = models.TextField(blank=True, null=True)
    choice07 = models.TextField(blank=True, null=True)
    choice08 = models.TextField(blank=True, null=True)
    choice09 = models.TextField(blank=True, null=True)
    choice10 = models.TextField(blank=True, null=True)
    choice11 = models.TextField(blank=True, null=True)
    choice12 = models.TextField(blank=True, null=True)
    choice13 = models.TextField(blank=True, null=True)
    choice14 = models.TextField(blank=True, null=True)
    choice15 = models.TextField(blank=True, null=True)
    choice16 = models.TextField(blank=True, null=True)
    choice17 = models.TextField(blank=True, null=True)
    choice18 = models.TextField(blank=True, null=True)
    choice19 = models.TextField(blank=True, null=True)
    choice20 = models.TextField(blank=True, null=True)
    choice21 = models.TextField(blank=True, null=True)
    choice22 = models.TextField(blank=True, null=True)
    choice23 = models.TextField(blank=True, null=True)
    choice24 = models.TextField(blank=True, null=True)
    choice25 = models.TextField(blank=True, null=True)
    choice26 = models.TextField(blank=True, null=True)
    choice27 = models.TextField(blank=True, null=True)
    choice28 = models.TextField(blank=True, null=True)
    choice29 = models.TextField(blank=True, null=True)
    choice30 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_accessibility_out'


class ArXViewCopyableAccessiblty(models.Model):
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    other_servicepoint_id = models.BigIntegerField(blank=True, null=True)
    other_entrance_id = models.BigIntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_copyable_accessiblty'


class ArXViewCopyableAccessiblty2(models.Model):
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    entrance_id = models.BigIntegerField(blank=True, null=True)
    other_servicepoint_id = models.BigIntegerField(blank=True, null=True)
    other_entrance_id = models.BigIntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_copyable_accessiblty2'


class ArXViewEntranceAnswer(models.Model):
    entrance_id = models.BigIntegerField(blank=True, null=True)
    question_id = models.FloatField(blank=True, null=True)
    choice_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_entrance_answer'


class ArXViewShortageHelper(models.Model):
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    viewpoint_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    requirement_id = models.IntegerField(blank=True, null=True)
    requirement_text = models.TextField(blank=True, null=True)
    is_indoor_servicepoint = models.TextField(blank=True, null=True)
    evaluation_subject = models.TextField(blank=True, null=True)
    big_flag = models.TextField(blank=True, null=True)
    ok_flag = models.TextField(blank=True, null=True)
    explanation_why_not = models.TextField(blank=True, null=True)
    shortage_fi = models.TextField(blank=True, null=True)
    shortage_sv = models.TextField(blank=True, null=True)
    shortage_en = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_shortage_helper'


class ArXViewShortageHelperOld(models.Model):
    servicepoint_id = models.BigIntegerField(blank=True, null=True)
    viewpoint_id = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    requirement_id = models.IntegerField(blank=True, null=True)
    requirement_text = models.TextField(blank=True, null=True)
    is_indoor_servicepoint = models.TextField(blank=True, null=True)
    evaluation_subject = models.TextField(blank=True, null=True)
    big_flag = models.TextField(blank=True, null=True)
    ok_flag = models.TextField(blank=True, null=True)
    explanation_why_not = models.TextField(blank=True, null=True)
    shortage_fi = models.TextField(blank=True, null=True)
    shortage_sv = models.TextField(blank=True, null=True)
    shortage_en = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'ar_x_view_shortage_helper_old'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class SysAddressPostoffice(models.Model):
    municipality_id = models.IntegerField()
    post_office = models.CharField(max_length=50, blank=True, null=True)
    post_office_fi = models.CharField(max_length=50, blank=True, null=True)
    post_office_sv = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sys_address_postoffice'


class TpTempEstBlokkikaannos(models.Model):
    question_block_id = models.IntegerField(blank=True, null=True)
    name_fi = models.CharField(max_length=99, blank=True, null=True)
    description_fi = models.CharField(max_length=1000, blank=True, null=True)
    name_sv = models.CharField(max_length=99, blank=True, null=True)
    description_sv = models.CharField(max_length=1000, blank=True, null=True)
    name_en = models.CharField(max_length=99, blank=True, null=True)
    description_en = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp_temp_est_blokkikaannos'


class TpTempEstKokouskysymys(models.Model):
    question_id = models.IntegerField(blank=True, null=True)
    bid = models.IntegerField(blank=True, null=True)
    qcode = models.CharField(max_length=20, blank=True, null=True)
    qorder = models.CharField(max_length=20, blank=True, null=True)
    qlev = models.IntegerField(blank=True, null=True)
    qtext = models.CharField(max_length=500, blank=True, null=True)
    act = models.CharField(max_length=1, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_text = models.CharField(max_length=255, blank=True, null=True)
    dep = models.CharField(max_length=40, blank=True, null=True)
    choice01 = models.CharField(max_length=255, blank=True, null=True)
    choice02 = models.CharField(max_length=255, blank=True, null=True)
    choice03 = models.CharField(max_length=255, blank=True, null=True)
    choice04 = models.CharField(max_length=255, blank=True, null=True)
    choice05 = models.CharField(max_length=255, blank=True, null=True)
    choice06 = models.CharField(max_length=255, blank=True, null=True)
    choice07 = models.CharField(max_length=255, blank=True, null=True)
    choice08 = models.CharField(max_length=255, blank=True, null=True)
    choice09 = models.CharField(max_length=255, blank=True, null=True)
    choice10 = models.CharField(max_length=255, blank=True, null=True)
    choice11 = models.CharField(max_length=255, blank=True, null=True)
    choice12 = models.CharField(max_length=255, blank=True, null=True)
    choice13 = models.CharField(max_length=255, blank=True, null=True)
    choice14 = models.CharField(max_length=255, blank=True, null=True)
    choice15 = models.CharField(max_length=255, blank=True, null=True)
    choice16 = models.CharField(max_length=20, blank=True, null=True)
    choice17 = models.CharField(max_length=20, blank=True, null=True)
    choice18 = models.CharField(max_length=20, blank=True, null=True)
    choice19 = models.CharField(max_length=20, blank=True, null=True)
    choice20 = models.CharField(max_length=20, blank=True, null=True)
    choice21 = models.CharField(max_length=20, blank=True, null=True)
    choice22 = models.CharField(max_length=20, blank=True, null=True)
    choice23 = models.CharField(max_length=20, blank=True, null=True)
    choice24 = models.CharField(max_length=20, blank=True, null=True)
    choice25 = models.CharField(max_length=20, blank=True, null=True)
    choice26 = models.CharField(max_length=20, blank=True, null=True)
    choice27 = models.CharField(max_length=20, blank=True, null=True)
    choice28 = models.CharField(max_length=20, blank=True, null=True)
    choice29 = models.CharField(max_length=20, blank=True, null=True)
    choice30 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp_temp_est_kokouskysymys'


class TpTempEstKokouslause(models.Model):
    sentence_id = models.IntegerField(blank=True, null=True)
    question_block_id = models.IntegerField(blank=True, null=True)
    sentence_group_id = models.IntegerField(blank=True, null=True)
    criteria = models.CharField(max_length=255, blank=True, null=True)
    fi = models.CharField(max_length=1000, blank=True, null=True)
    sv = models.CharField(max_length=1000, blank=True, null=True)
    en = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp_temp_est_kokouslause'


class TpTempEstKysymyskaannos(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    koodi = models.CharField(max_length=20, blank=True, null=True)
    fi = models.CharField(max_length=1000, blank=True, null=True)
    sv = models.CharField(max_length=1000, blank=True, null=True)
    en = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp_temp_est_kysymyskaannos'


class TpTempStoredShortageHelper(models.Model):
    servicepoint_id = models.BigIntegerField()
    viewpoint_id = models.IntegerField()
    requirement_id = models.IntegerField()
    requirement_text = models.CharField(max_length=1000, blank=True, null=True)
    is_indoor_servicepoint = models.CharField(
        max_length=1, blank=True, null=True)
    evaluation_subject = models.CharField(max_length=1, blank=True, null=True)
    big_flag = models.CharField(max_length=1, blank=True, null=True)
    ok_flag = models.CharField(max_length=1, blank=True, null=True)
    explanation_why_not = models.CharField(
        max_length=1000, blank=True, null=True)
    shortage_fi = models.CharField(max_length=1000, blank=True, null=True)
    shortage_sv = models.CharField(max_length=1000, blank=True, null=True)
    shortage_en = models.CharField(max_length=1000, blank=True, null=True)
    stored = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tp_temp_stored_shortage_helper'
