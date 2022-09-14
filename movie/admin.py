from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Category, Comment, Genres, Rating, Persons, Stars, Frame, Movie

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name", )


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("name", "email")


class FrameInLine(admin.TabularInline):
    model = Frame
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height=110')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    list_display_links = ("title",)
    search_fields = ("title", "category__name")
    inlines = [FrameInLine, CommentInLine]
    readonly_fields = ("get_image", )
    form = MovieAdminForm
    save_on_top = True
    actions = ["publish", "unpublish"]
    save_as = True
    list_editable = ("draft",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"),)
        }),
        (None, {
            "fields": (("year", "world_premiere","country"),)
        }),
        ("Actors", {
            "classes": ("collapse", ),
            "fields": (("actors", "directors", "genres"),)
        }),
        (None, {
            "fields": (("budget", "world_profit"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height=110')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} были записей обновлны"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} были записей обновлны"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"

    unpublish.short_description = "Снять с публикации"
    unpublish.allow_permission = ("change",)

    get_image.short_description = "Постер"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Persons)
class PersonsAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height=60')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "star", "ip")


@admin.register(Stars)
class StarsAdmin(admin.ModelAdmin):
    list_display = ("value", )


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height=60')

    get_image.short_description = "Изображение"


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
