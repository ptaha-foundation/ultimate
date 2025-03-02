import django_filters# import rest_framework as filters
from django.db.models import Q

from trade.models import Lot


class MultipleIContainsFilter(django_filters.Filter):
    def __init__(self, lookup_field='', *args, **kwargs):
        self.lookup_field = lookup_field
        super().__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        values = value.split(',')
        print(values)
        query = Q()
        for val in values:
            query |= Q(**{f'{self.field_name}{self.lookup_field}': val})
            print(query)
        return queryset.filter(query)


class LotFilter(django_filters.FilterSet):
    fuel_type = MultipleIContainsFilter(field_name='fuel_type__name')
    oilbase_address = MultipleIContainsFilter(field_name='oil_base__address')
    oilbase_name = MultipleIContainsFilter(field_name='oil_base__name')

    class Meta:
        model = Lot
        fields = []
