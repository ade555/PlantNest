from django.views.generic import ListView
from plant_store.models import Products
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import FeedbackForm

# this view from the homepage inherits from the plant_store.PlantListView view and the plant_store.AccessoryListView in the plant_store app
class HomePage(ListView):
    model = Products
    template_name = 'content_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context
        
        accessories = Products.objects.filter(product_type="accessory")
        accessories_id = [accessory.id for accessory in accessories]
        accessories_and_ids = zip(accessories, accessories_id)
        sliced_accessories_and_ids = list(accessories_and_ids)[:4]

        plants = Products.objects.filter(product_type="plant")
        plants_id = [plant.id for plant in plants]
        plants_and_ids = zip(plants, plants_id)
        sliced_plants_and_ids = list(plants_and_ids)[:4]

        context['sliced_accessories_and_ids'] = sliced_accessories_and_ids
        context['sliced_plants_and_ids'] = sliced_plants_and_ids
        return context

# contact view for user to send feedback
class FeedbackView(FormView):
    template_name = 'content_app/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('content_app:contact')

    # if the form is valid, save the message to the model
    def form_valid(self, form):
        # Save the message in the database
        form.save()
        messages.success(self.request, 'We have received your feedback. Thank you!')

        return super().form_valid(form)
