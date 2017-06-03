from django.contrib import admin
from Vinux.models import WineProductionArea, WineDenomination, WineCellar, StoredWineBottle, UserComment, BottleUserReview, ProducerUserReview

# Register your models here.
admin.site.register(WineProductionArea)
admin.site.register(WineDenomination)
admin.site.register(WineCellar)
admin.site.register(StoredWineBottle)
admin.site.register(UserComment)
admin.site.register(BottleUserReview)
admin.site.register(ProducerUserReview)
