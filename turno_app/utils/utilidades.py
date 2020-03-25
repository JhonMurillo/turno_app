import itertools

def groupby_queryset_with_fields(queryset, fields):
    fields_qs = {}
    from itertools import groupby

    for field in fields:
        queryset = queryset.order_by(field)

        def getter(obj):
            related_names = field.split('__')
            for related_name in related_names:
                try:
                    obj = getattr(obj, related_name)
                except AttributeError:
                    obj = None
            return obj

        fields_qs[field] = [{'grouper': key, 'list': list(group)} for key, group in
                            groupby(queryset, lambda x: getattr(x, field)
                            if '__' not in field else getter(x))]
    return fields_qs
