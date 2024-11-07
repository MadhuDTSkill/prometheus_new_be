from rest_framework import serializers
from .models import Chat, Message, UploadedFile, CustomGPT, GPTResponse

# for obj in CustomGPT.objects.all():
#     obj.delete()

class ChatSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
      default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(
      default=serializers.CurrentUserDefault()
    )

    
    class Meta:
        model = Message
        fields = '__all__'
        
class GPTResponseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GPTResponse
        fields = '__all__'
        

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file', 'created_at']
        

class CustomGPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGPT
        fields = '__all__'