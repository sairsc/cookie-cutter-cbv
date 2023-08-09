from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import FeedbackForm
from .models import Feedback


# Create your views here.
class FeedbackListView(ListView):
    model = Feedback
    context_object_name = "feedbacks"
    template_name = "feedback/feedback_list.html"


class FeedbackCreateView(CreateView):
    model_class = Feedback
    form_class = FeedbackForm
    template_name = "feedback/feedback_new.html"
    success_url = "/"

    def form_valid(self, form):
        validation = super().form_valid(form)
        if validation:
            feedback = form.save(commit=False)
            feedback.save()
            subject = "Feedback submitted."
            message = f"Name:\n\t{feedback.name}\nEmail:\n\t{feedback.email}\nFeedback:\n{feedback.feedback}\n\n"
            from_email = "sair@ignishealth.com"
            send_mail(subject, message, from_email, [feedback.email])
        return validation
