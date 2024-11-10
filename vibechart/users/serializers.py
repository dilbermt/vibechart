from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password']
        extra_kwargs={
            # doesn't return the password
            "password":{"write_only":True}
        }

    # overriding the default create method to save the password as a hashed string
    def create(self,validated_data):
        password = validated_data.pop("password",None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            # set password method hashes the password automatically
            instance.set_password(password)
        instance.save()
        return instance
     