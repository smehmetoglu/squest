from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from resource_tracker_v2.api.serializers.resource_serializer import ResourceSerializer, ResourceCreateSerializer
from resource_tracker_v2.filters.resource_filter import ResourceFilter
from resource_tracker_v2.models import Resource, ResourceGroup


class ResourceListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResourceSerializer
    filterset_class = ResourceFilter

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Resource.objects.none()
        resource_group_id = self.kwargs['resource_group_id']
        queryset = Resource.objects.filter(resource_group_id=resource_group_id)
        return queryset

    def create(self, request, **kwargs):
        resource_group_id = self.kwargs['resource_group_id']
        resource_group = get_object_or_404(ResourceGroup, pk=resource_group_id)
        context = {'resource_group': resource_group}
        serializer = ResourceCreateSerializer(data=request.data, context=context)
        if serializer.is_valid():
            new_resource = serializer.save()
            read_serializer = ResourceSerializer(instance=new_resource)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)