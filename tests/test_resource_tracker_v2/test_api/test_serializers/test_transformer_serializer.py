from django.db import IntegrityError

from resource_tracker_v2.api.serializers.transformer_serializer import TransformerSerializer
from resource_tracker_v2.models import AttributeDefinition, ResourceGroup, Transformer
from tests.test_resource_tracker_v2.base_test_resource_tracker_v2 import BaseTestResourceTrackerV2API


class TransformerSerializerTests(BaseTestResourceTrackerV2API):

    def setUp(self):
        super(TransformerSerializerTests, self).setUp()
        self.context = {
            "resource_group": self.cluster,
        }
        self.new_rg = ResourceGroup.objects.create(name="new_rg")
        self.new_attribute = AttributeDefinition.objects.create(name="new_attribute")
        self.new_transformer = Transformer.objects.create(resource_group=self.new_rg,
                                                          attribute_definition=self.core_attribute)
        self.number_transformer_before = Transformer.objects.all().count()

    def _validate_transformer_created(self):
        self.assertEqual(self.number_transformer_before + 1, Transformer.objects.all().count())

    def test_create_transformer_no_consumption(self):
        data = {
            "attribute_definition": self.new_attribute.id,
            "consume_from_resource_group": None,
            "consume_from_attribute_definition": None,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self._validate_transformer_created()

    def test_create_transformer_with_consumption(self):
        data = {
            "attribute_definition": self.new_attribute.id,
            "consume_from_resource_group": self.new_rg.id,
            "consume_from_attribute_definition": self.core_attribute.id,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self._validate_transformer_created()

    def test_cannot_create_transformer_with_target_rg_and_no_target_attribute(self):
        data = {
            "attribute_definition": self.new_attribute.id,
            "consume_from_resource_group": self.new_rg.id,
            "consume_from_attribute_definition": None,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'consume_from_attribute_definition'})

    def test_cannot_create_transformer_with_not_target_rg_and_target_attribute(self):
        data = {
            "attribute_definition": self.new_attribute.id,
            "consume_from_resource_group": None,
            "consume_from_attribute_definition": self.new_attribute.id,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'consume_from_resource_group'})

    def test_transformer_exist_already_on_selected_attribute(self):
        data = {
            "attribute_definition": self.core_attribute.id,
            "consume_from_resource_group": None,
            "consume_from_attribute_definition": None,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(IntegrityError):
            serializer.save()

    def test_invalid_target_attribute_in_transformer(self):
        data = {
            "attribute_definition": self.new_attribute.id,
            "consume_from_resource_group": self.new_rg.id,
            "consume_from_attribute_definition": self.vcpu_attribute.id,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'consume_from_attribute'})

    def test_can_link_attribute_to_multiple_same_attribute_def_from_different_rg(self):
        other_vms = ResourceGroup.objects.create(name="other_vms")
        Transformer.objects.create(resource_group=other_vms, attribute_definition=self.vcpu_attribute)
        other_field = AttributeDefinition.objects.create(name="other_field")
        data = {
            "attribute_definition": other_field.id,
            "consume_from_resource_group": other_vms.id,
            "consume_from_attribute_definition": self.vcpu_attribute.id,
        }
        context = {
            "resource_group": self.single_vms,
        }
        serializer = TransformerSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())
        self._validate_transformer_created()

    def test_cannot_create_circular_loop_when_adding_consumer(self):
        data = {
            "attribute_definition": self.core_attribute.id,
            "consume_from_resource_group": self.ocp_projects.id,
            "consume_from_attribute_definition": self.request_cpu.id,
        }
        serializer = TransformerSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {'consume_from_attribute_definition'})