from django.contrib import admin
from Vinux.models import WineProductionArea, WineDenomination, WineCellar, StoredWineBottle

# Register your models here.
admin.site.register(WineProductionArea)
admin.site.register(WineDenomination)
admin.site.register(WineCellar)
admin.site.register(StoredWineBottle)
