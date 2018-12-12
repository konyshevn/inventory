from django import forms
from django.core.cache import caches
from django.core import signing
from django.db.models import Q
from django.forms.models import ModelChoiceIterator
from functools import reduce

cache = caches['selectize']


class ModelSelectizeWidget(forms.Select):
    model = None
    search_fields = []
    queryset = None

    def __init__(self, *args, **kwargs):
        """
        Overwrite class parameters if passed as keyword arguments.

        Args:
            model (django.db.models.Model): Model to select choices from.
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
            search_fields (list): List of model lookup strings.
            max_results (int): Max. JsonResponse view page size.

        """
        self.model = kwargs.pop('model', self.model)
        self.queryset = kwargs.pop('queryset', self.queryset)
        self.search_fields = kwargs.pop('search_fields', self.search_fields)
        #self.max_results = kwargs.pop('max_results', self.max_results)
        #defaults = {'data_view': 'django_select2-json'}
        #defaults.update(kwargs)
        super(ModelSelectizeWidget, self).__init__(*args,)


    def build_attrs(self, *args, **kwargs):
        """Set select2's AJAX attributes."""
        attrs = super(ModelSelectizeWidget, self).build_attrs(*args, **kwargs)

        # encrypt instance Id
        self.widget_id = signing.dumps(id(self))

        attrs['data-field_id'] = self.widget_id
        #attrs.setdefault('data-ajax--url', self.get_url())
        #attrs.setdefault('data-ajax--cache', "true")
        #attrs.setdefault('data-ajax--type', "GET")
        #attrs.setdefault('data-minimum-input-length', 2)
        #if self.dependent_fields:
        #    attrs.setdefault('data-select2-dependent-fields', " ".join(self.dependent_fields))

        attrs['class'] = 'selectize_widget'
        return attrs

    def render(self, *args, **kwargs):
        """Render widget and register it in Django's cache."""
        output = super(ModelSelectizeWidget, self).render(*args, **kwargs)
        self.set_to_cache()
        return output

    def _get_cache_key(self):
        return "%s%s" % ('selectize_widget_', id(self))

    def set_to_cache(self):
        cache.set(self._get_cache_key(), {
            'cls': self.__class__,
            'search_fields': self.search_fields,
            'model': self.model,
        })

    def filter_queryset(self, term, queryset=None, **dependent_fields):
        """
        Return QuerySet filtered by search_fields matching the passed term.

        Args:
            term (str): Search term
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
            **dependent_fields: Dependent fields and their values. If you want to inherit
                from ModelSelect2Mixin and later call to this method, be sure to pop
                everything from keyword arguments that is not a dependent field.

        Returns:
            QuerySet: Filtered QuerySet

        """
        if queryset is None:
            queryset = self.get_queryset()
        search_fields = self.get_search_fields()
        select = Q()
        term = term.replace('\t', ' ')
        term = term.replace('\n', ' ')
        for t in [t for t in term.split(' ') if not t == '']:
            select &= reduce(lambda x, y: x | Q(**{y: t}), search_fields,
                             Q(**{search_fields[0]: t}))
        if dependent_fields:
            select &= Q(**dependent_fields)

        return queryset.filter(select).distinct()

    def get_queryset(self):
        """
        Return QuerySet based on :attr:`.queryset` or :attr:`.model`.

        Returns:
            QuerySet: QuerySet of available choices.

        """
        if self.queryset is not None:
            queryset = self.queryset
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise NotImplementedError(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
        return queryset

    def get_search_fields(self):
        """Return list of lookup names."""
        if self.search_fields:
            return self.search_fields
        raise NotImplementedError('%s, must implement "search_fields".' % self.__class__.__name__)

    def optgroups(self, name, value, attrs=None):
        """Return only selected options and set QuerySet from `ModelChoicesIterator`."""
        default = (None, [], 0)
        groups = [default]
        has_selected = False
        selected_choices = {str(v) for v in value}
        if not self.is_required and not self.allow_multiple_selected:
            default[1].append(self.create_option(name, '', '', False, 0))
        if not isinstance(self.choices, ModelChoiceIterator):
            return super(ModelSelectizeWidget, self).optgroups(name, value, attrs=attrs)
        selected_choices = {
            c for c in selected_choices
            if c not in self.choices.field.empty_values
        }
        field_name = self.choices.field.to_field_name or 'pk'
        query = Q(**{'%s__in' % field_name: selected_choices})
        for obj in self.choices.queryset.filter(query):
            option_value = self.choices.choice(obj)[0]
            option_label = self.label_from_instance(obj)

            selected = (
                str(option_value) in value and
                (has_selected is False or self.allow_multiple_selected)
            )
            if selected is True and has_selected is False:
                has_selected = True
            index = len(default[1])
            subgroup = default[1]
            subgroup.append(self.create_option(name, option_value, option_label, selected_choices, index))
        '''
        '''

        return groups

    def label_from_instance(self, obj):
        """
        Return option label representation from instance.

        Can be overridden to change the representation of each choice.

        Example usage::

            class MyWidget(ModelSelect2Widget):
                def label_from_instance(obj):
                    return str(obj.title).upper()

        Args:
            obj (django.db.models.Model): Instance of Django Model.

        Returns:
            str: Option label.

        """
        return str(obj)