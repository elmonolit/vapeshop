from django import template
from django.utils.safestring import mark_safe
from showcase.models import *

register = template.Library()

TABLE_HEAD = """
            <table class="table">
              <tbody>
            """
TABLE_TAIL = """
          </tbody>
            </table>
"""
TABLE_CONTENT = """
    <tr>
      <td>{name}</td>
      <td>{value}</td>
    </tr>
"""
PRODUCT_SPEC = {
    'mechmod': {
        'Диаметр': 'diameter',
        'Тип коннектора': 'connector',
        'Количество аккумуляторов': 'amount_of_acb',
        'Материал': 'material',
        'Тип аккумулятора': 'accum_type',
    },
    'mod': {
        'Диаметр': 'diameter',
        'Тип коннектора': 'connector',
        'Количество аккумуляторов': 'amount_of_acb',
        'Мощность': 'power',
        'Наличие аккумулятора': 'accum',
        'Емкость аккумулятора': 'accum_capacity',
        'Термоконтроль': 'thermal_control',
    }
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Mod):
        if not product.accum:
            product.accum = 'Нет'
            if 'Емкость аккумулятора' in PRODUCT_SPEC['mod']:
                PRODUCT_SPEC['mod'].pop('Емкость аккумулятора')
        else:
            product.accum = 'Да'

        if product.thermal_control:
            product.thermal_control = 'Есть'
        else:
            product.thermal_control = 'Отсутствует'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
