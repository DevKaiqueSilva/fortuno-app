from rest_framework import serializers

class OwnedByUserModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(
        read_only=True, 
        required=False,
    )
    created = serializers.DateTimeField(
        required=False,
        read_only=True, 
        format="%Y-%m-%d %H:%M:%S"
    )
    updated = serializers.DateTimeField(
        required=False,
        read_only=True, 
        format="%Y-%m-%d %H:%M:%S"
    )

    def _set_user(self, instance):
        user = self.context.get('user')
        instance.user = user
        instance.save()

    def create(self, validated_data):
        instance = super().create(validated_data)
        self._set_user(instance=instance)        
        return instance


    