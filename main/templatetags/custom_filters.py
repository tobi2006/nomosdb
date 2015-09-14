from django import template
from django.utils.datastructures import OrderedDict

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

@register.filter
def academic_year(year):
    """Turns 1900 into 1900/01"""
    int_year = int(year)
    ac_year = str(int_year) + "/" + str(int_year+1)[-2:]
    return ac_year

@register.filter(name='sort')
def listsort(value):
        if isinstance(value, dict):
            new_dict = OrderedDict()
            key_list = value.keys()
            key_list.sort()
            for key in key_list:
                new_dict[key] = value[key]
            return new_dict
        elif isinstance(value, list):
            new_list = list(value)
            new_list.sort()
            return new_list
        else:
            return value
        listsort.is_safe = True
