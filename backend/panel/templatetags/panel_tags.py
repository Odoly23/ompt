from django import forms, template

register = template.Library()


@register.filter
def bs(bound_field):
    """Render a form field with Bootstrap 4 classes."""
    widget = bound_field.field.widget
    css = "form-control"
    if isinstance(widget, (forms.CheckboxInput,)):
        css = "custom-control-input"
    elif isinstance(widget, (forms.ClearableFileInput, forms.FileInput)):
        css = "form-control-file"
    elif isinstance(widget, forms.Select):
        css = "custom-select"
    if bound_field.errors:
        css += " is-invalid"
    attrs = {"class": css}
    if isinstance(widget, forms.DateInput):
        attrs["type"] = "date"
    if isinstance(widget, forms.Textarea):
        attrs["rows"] = 5
    return bound_field.as_widget(attrs=attrs)


@register.filter
def is_checkbox(bound_field):
    return isinstance(bound_field.field.widget, forms.CheckboxInput)
