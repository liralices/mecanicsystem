from django import template
import locale

register = template.Library()

@register.filter
def br_format(value):
    if value is None or value == '':
        return "0,00"
    try:
        # Tentar converter para float se for string
        if isinstance(value, str):
            value = float(value.replace(',', '.'))
        # Formatar como moeda brasileira
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(value, grouping=True, symbol=False).strip()
    except (ValueError, locale.Error):
        # Fallback se locale não funcionar ou conversão falhar
        try:
            num = float(value)
            return f"{num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return str(value)