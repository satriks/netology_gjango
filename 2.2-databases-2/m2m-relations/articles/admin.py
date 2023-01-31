from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        counter = 0
        for form in self.forms:
            for key, value in form.cleaned_data.items():
                if key == 'is_main' and value is True:
                    counter += 1
        if counter > 1:
            raise ValidationError('Основной раздел может быть только один.')
        elif counter == 0:
            raise ValidationError('Укажите основной раздел')

        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 2

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at']
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass




#
# class ScopeInlineFormset(BaseInlineFormSet):
#     pass
#