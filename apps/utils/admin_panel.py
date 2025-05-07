from django.contrib import admin


class AdminRegister:
    @staticmethod
    def register(model, fields_to_display=None, fields_to_edit=None):
        if not fields_to_display:
            fields_to_display = [field.name for field in model._meta.fields]

        if not fields_to_edit:
            fields_to_edit = []

        @admin.register(model)
        class CustomAdmin(admin.ModelAdmin):
            list_display = fields_to_display
            list_editable = fields_to_edit
