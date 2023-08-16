from django.contrib import admin
from .models import Questions,Comments,Reviews,YouPoll,Apppolls,Ninja,Tags,likes1,dlikes1,likes2,dlikes2,Watch,Collab
# Register your models here.
admin.site.register(Questions)
admin.site.register(Comments)
admin.site.register(Reviews)


admin.site.register(Apppolls)
admin.site.register(Tags)
admin.site.register(likes1)
admin.site.register(dlikes1)
admin.site.register(likes2)
admin.site.register(dlikes2)

admin.site.register(Watch)
admin.site.register(Collab)