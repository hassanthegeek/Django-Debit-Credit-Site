from django import template
import math

register = template.Library()


@register.filter(name='makepos')
def absolute(number):
    # print(type(number), number, abs(number))
    if not (number == None):
        return abs(number)


@register.filter(name='getid')
def getid(input):
    l = input.split('/')
    return l[1]


@register.filter
def none_or_zero(input):
    return input if input else "0.00"


@register.filter
def two_decimal_places(input):
    if input:
        return round(input, 2)
