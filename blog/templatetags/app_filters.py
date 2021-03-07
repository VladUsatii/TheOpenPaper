from django import template

register = template.Library()

@register.filter(name='get_city_string')
def get_city_string(values):
    # Checks if city or location contains a comma.
    city = values
    if city.find(','):
        city = city.split(",", 1)
        substring = city[0]
        return substring
    return city

@register.filter(name='cool_num', is_safe=False)
def cool_num(val, precision=2):
    try:
        int_val = int(val)
    except ValueError:
        raise template.TemplateSyntaxError(
            f'Value must be an integer. {val} is not an integer')
    if int_val < 1000:
        return str(int_val)
    elif int_val < 1_000_000:
        return f'{ int_val/1000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'K'
    else:
        return f'{int_val/1_000_000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'M'
