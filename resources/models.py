from django.db import models
from django.contrib.auth.models import User



#


class Profile(models.Model):
    
    class UserRole(models.TextChoices):
        LANDER = 'Lander'
        BORROWER = 'Borrower'
        BOTH = 'LanderAndBorrower'
    class GenderChoice(models.TextChoices):
        M  = 'Male'
        F = 'Female'


    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50 )
    age = models.PositiveIntegerField()
    gender =  models.CharField(max_length=6, choices=GenderChoice)
    user_role = models.CharField(choices=UserRole, default=UserRole.BOTH, max_length=25)
    address  = models.CharField(max_length=300)
    phone =models.CharField(max_length=12)
    joined_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


class Resource(models.Model):

    class ResourceType(models.TextChoices):
        TOOL = 'Tool'
        SKILL = 'Skill'
        ITEM = 'Item'
        SERVICE= 'Service'

    class ConditionStatus(models.TextChoices):
        GOOD = 'Good'
        MODERATE= 'Moderate'

  
        
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='shared_resources')
    name = models.CharField(max_length=200)
    condition= models.CharField(max_length=10, choices=ConditionStatus, default=ConditionStatus.MODERATE)
    day_price = models.DecimalField(max_digits=5, decimal_places=1)
    availabel = models.BooleanField(default=True)
    image = models.ImageField(upload_to='resource/images', null=True)
    location = models.CharField(max_length=40)
    description = models.TextField()
    # trusted_borrowers = models.PositiveSmallIntegerField(default=0)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.name
    

class RequestResource(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = 'Pending'
        ACCEPTED = 'Accepted'
        REJECTED = 'Rejected'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='borrow_requests')
    duration_in_days = models.PositiveSmallIntegerField(default=1)
    starting_date = models.DateField()
    end_date= models.DateField()
    status = models.CharField(max_length=10, choices=RequestStatus, default=RequestStatus.PENDING)

    def __str__(self):
        return f'{self.user.profile.name} request {self.resource.name}'

class Message(models.Model):

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    on_date = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE,related_name='ratings')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.PositiveSmallIntegerField(default=0)
    feedback = models.TextField()

    def __str__(self):
        return f'{self.resource.name} rating {self.user.profile.name}'


