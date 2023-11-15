from django.db import models
from django.contrib.auth.models import User

class TagManager(models.Manager):
    def most_popular(self, total):
        return self.all()[:total]

class Tag(models.Model):
    name = models.CharField(max_length=50)

    objects = TagManager()
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class QuestionsManager(models.Manager):
        def newest(self):
            return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.order_by('-creation_date')]
    
        def best(self):
            return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.order_by('-rating')]
    
        def with_tag(self, tag_name):
            return [{'question': q, 'tags': self.get_tags(q.pk)} for q in self.filter(tags=tag_name)]
    
        def with_id(self, id):
            q = self.get(pk=id)
            return {'question': q, 'tags': self.get_tags(q.pk)}
    
        def get_tags(self, id):
            tag_names = self.values_list('tags', flat=True).filter(pk=id)
            return Tag.objects.filter(pk__in=tag_names)  

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionsManager()

    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
        def newest(self, question_id):
            return self.filter(question=question_id).order_by('-creation_date')

        def best(self, question_id):
            return self.filter(question=question_id).order_by( '-is_correct', '-rating')

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return f"Answer to '{self.question.title}'"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} likes {self.question.title}{' - ' + self.answer.content if self.answer else ''}"

