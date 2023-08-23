from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.utils import timezone
from django.http import HttpResponseForbidden

from misc.utils.get_model_by_name import get_model_by_name


class ObjectDetailsView(DetailView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        model_name = self.kwargs.get('model_name', None)
        model = get_model_by_name(model_name)
        obj = get_object_or_404(model, pk=pk)
        return render(request, 'details/%s.html' % model_name, locals())


# class ObjectPublishView(View):
#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk', None)
#         model_name = self.kwargs.get('model_name', None)
#         url = ''
#         if '_changelist_filters' in request.GET:
#             url = '?' + request.GET['_changelist_filters']
#         if model_name == 'user' and request.user.pk == pk:
#             messages.error(request, words.ERROR_CURRENT_USER.capitalize())
#             return redirect(reverse('admin:%s_%s_%s' % ('misc', model_name, 'changelist')) + url)
#         model = get_object_or_404(get_model_by_name(model_name), pk=pk)
#         model_str = str(model)
#         model.published = not model.published
#         model.save()
#         if model.published:
#             messages.success(request, words.SUCCESSFULLY_PUBLISH_MESSAGE.capitalize())
#         else:
#             messages.success(request, words.SUCCESSFULLY_UNPUBLISH_MESSAGE.capitalize())
#         LogEntry.objects.log_action(
#             user_id=request.user.pk,
#             content_type_id=ContentType.objects.get_for_model(model).pk,
#             object_id=model.pk,
#             object_repr=model_str,
#             action_flag=2
#         )
#         return redirect(reverse('admin:%s_%s_%s' % (model._meta.app_label, model_name, 'changelist')) + url)


# class ObjectActiveView(View):
#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk', None)
#         model_name = self.kwargs.get('model_name', None)
#         url = ''
#         if '_changelist_filters' in request.GET:
#             url = '?' + request.GET['_changelist_filters']
#         model = get_object_or_404(get_model_by_name(model_name), pk=pk)
#         if model_name == 'user' and request.user.pk == pk:
#             messages.error(request, words.ERROR_CURRENT_USER.capitalize())
#             return redirect(reverse('admin:%s_%s_%s' % (model._meta.app_label, model_name, 'changelist')) + url)
#         elif model_name == 'news' and model.end_datetime < timezone.now():
#             messages.error(request, words.ERROR_NEW_NO_LONGER_ACTIVE.capitalize())
#             return redirect(reverse('admin:%s_%s_%s' % (model._meta.app_label, model_name, 'changelist')) + url)
#         model_str = str(model)
#         model.is_active = not model.is_active
#         model.save()
#         if model.is_active:
#             messages.success(request, words.SUCCESSFULLY_ACTIVE_MESSAGE.capitalize())
#         else:
#             messages.success(request, words.SUCCESSFULLY_INACTIVE_MESSAGE.capitalize())
#         LogEntry.objects.log_action(
#             user_id=request.user.pk,
#             content_type_id=ContentType.objects.get_for_model(model).pk,
#             object_id=model.pk,
#             object_repr=model_str,
#             action_flag=2
#         )
#         return redirect(reverse('admin:%s_%s_%s' % (model._meta.app_label, model_name, 'changelist')) + url)