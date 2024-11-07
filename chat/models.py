from django.db import models
from users.models import User
from .ai_prompts import get_name
import uuid


class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='uploads/')  # You can customize the upload directory
    vector_db_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class CustomGPT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_gpts')
    slug = models.CharField(null=True, blank=True, max_length=100, unique=True)
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    long_description = models.TextField()
    conversation_starters = models.JSONField(default=list)
    system_prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if self.slug is None or self.slug == '':
            some_uuid = str(self.id)[:8]
            self.slug = "g-" + some_uuid + "-" + self.name.replace(' ', '-').lower()
        super().save(*args, **kwargs)
    


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    first_prompt = models.TextField()
    name = models.CharField(max_length=100, null=True, blank=True)
    gpt = models.ForeignKey(CustomGPT, default = None, null=True, blank=True, related_name='chats', on_delete=models.CASCADE)
    attach = models.OneToOneField(UploadedFile, on_delete=models.CASCADE, null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        if self.name is None or self.name == '':
            self.name = get_name(self.first_prompt)
        super().save(*args, **kwargs)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    
    prompt = models.TextField()    
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        
class GPTResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gpt_responses')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='gpt_responses')
    prompt = models.TextField()
    response = models.TextField()
    llm_config = models.JSONField(default=dict)
    token_usage = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
        