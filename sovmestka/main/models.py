from django.db import models

class Block(models.Model):
    number = models.CharField(max_length=100, unique=True)
    time_stamp = models.CharField(max_length=100)
    miner = models.CharField(max_length=100)
    gase_used = models.CharField(max_length=100)
    def __str__(self):
        return self.number

class Transaction(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    hash = models.CharField(max_length=100, unique=True)
    from_address = models.CharField(max_length=100)
    to_address = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    def __str__(self):
        return self.hash

class Prompt(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    def __str__(self):
        return self.name

class Answer(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    text = models.TextField()
    def __str__(self):
        return str(self.prompt)