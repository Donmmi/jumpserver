# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.utils.translation import ugettext as _

from orgs.mixins.serializers import BulkOrgResourceModelSerializer
from ..models import Asset, Node


__all__ = [
    'NodeSerializer', "NodeAddChildrenSerializer",
    "NodeAssetsSerializer",
]


class NodeSerializer(BulkOrgResourceModelSerializer):
    name = serializers.ReadOnlyField(source='value')
    value = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, label=_("value")
    )

    class Meta:
        model = Node
        only_fields = ['id', 'key', 'value', 'org_id']
        fields = only_fields + ['name', 'full_value']
        read_only_fields = ['key', 'org_id']

    def validate_value(self, data):
        if not self.instance and not data:
            return data
        instance = self.instance
        siblings = instance.get_siblings()
        if siblings.filter(value=data):
            raise serializers.ValidationError(
                _('The same level node name cannot be the same')
            )
        return data


class NodeAssetsSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Asset.objects.all())

    class Meta:
        model = Node
        fields = ['assets']


class NodeAddChildrenSerializer(serializers.Serializer):
    nodes = serializers.ListField()

