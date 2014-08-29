from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_range(value):
    """Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)

@register.filter
def get_item_plus_1(dictionary, key):
    """Returns the next dictionary item, necessary for Group Assignment"""
    number = int(key)
    number += 1
    key = str(number)
    return dictionary.get(key)

@register.filter
def remove_spacebars(words):
    """Simply removes blank spaces from a word"""
    if words is not None:
        result = words.strip()
        result = result.replace('/', '')
        result = result.replace(' ', '_')
        result = result.replace('__', '_')
    else:
        result = ''
    return result

@register.filter
def get_attendance(performance, week):
    result = performance.attendance_for(week)
    return result

@register.filter
def joinby(value, arg):
    value_list = []
    for entry in value:
        value_list.append(entry.__str__())
    return arg.join(value_list)

@register.filter
def upper_case_first_letter(inputstring):
    return inputstring.title()
