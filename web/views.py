from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import CaseStudy, ContactMessage
from .forms import ContactForm


@ensure_csrf_cookie
def home(request):
    case_studies = CaseStudy.objects.filter(published=True).order_by("-date")[:6]
    return render(request, "home.html", {"case_studies": case_studies})


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def case_list(request):
    qs = CaseStudy.objects.filter(published=True).order_by("-date")
    return render(request, "cases_list.html", {"cases": qs})


def case_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug, published=True)
    return render(request, "case_detail.html", {"case": case})


def _is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"

@ensure_csrf_cookie
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # De-Dup: gleiche Email + gleicher Text innerhalb von 20 Sekunden
            window_start = timezone.now() - timedelta(seconds=20)
            exists = ContactMessage.objects.filter(
                email=cd["email"],
                message=cd["message"],
                created__gte=window_start,
            ).exists()

            if not exists:
                msg = form.save()
                # (Optional) E-Mail versenden – fehlerresistent
                try:
                    send_mail(
                        subject=f"[Datalization] New contact from {msg.first_name} {msg.last_name}",
                        message=f"Language: {msg.language}\n"
                                f"Name: {msg.first_name} {msg.last_name}\n"
                                f"Company: {msg.company or '-'}\n"
                                f"Email: {msg.email}\n\n{msg.message}",
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@yourdomain"),
                        recipient_list=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            success_text = (
                "Danke! Wir melden uns in Kürze."
                if request.LANGUAGE_CODE == "de"
                else "Thank you! We'll get back to you soon."
            )

            if _is_ajax(request):
                return JsonResponse({"ok": True, "message": success_text})

            messages.success(request, success_text)
            return redirect("web:home")

        # Form invalid
        if _is_ajax(request):
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)

        messages.error(
            request,
            "Bitte prüfen Sie Ihre Eingaben." if request.LANGUAGE_CODE == "de" else "Please check your input."
        )
        return redirect("web:home")

    # GET: normales Rendern
    form = ContactForm(initial={"language": request.LANGUAGE_CODE})
    return render(request, "contact.html", {"form": form})


    # Falls du eine separate Kontaktseite hast:
    return render(request, "contact.html", {"form": form})