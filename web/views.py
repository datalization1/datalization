from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from .models import CaseStudy, ContactMessage
from .forms import ContactForm
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

@cache_page(60 * 60)
@ensure_csrf_cookie
def home(request):
    case_studies = CaseStudy.objects.filter(published=True).order_by("-date")[:6]
    return render(request, "home.html", {"case_studies": case_studies})


def about(request):
    return render(request, "about.html")

@cache_page(60 * 60)
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


@require_http_methods(["GET", "POST"])
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

            msg = None
            if not exists:
                msg = form.save()

                # ---------- Admin-Mail ----------
                try:
                    context = {"msg": msg}
                    subject_admin = f"[Datalization] Neue Kontaktanfrage von {msg.first_name} {msg.last_name}"

                    text_admin = render_to_string("emails/contact_admin.txt", context)
                    html_admin = render_to_string("emails/contact_admin.html", context)

                    email_admin = EmailMultiAlternatives(
                        subject=subject_admin,
                        body=text_admin,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                        to=[getattr(settings, "CONTACT_RECEIVER_EMAIL", "info@datalization.ch")],
                    )
                    email_admin.attach_alternative(html_admin, "text/html")
                    email_admin.send(fail_silently=True)
                except Exception:
                    # Wir loggen nur – die Anfrage soll trotzdem durchgehen
                    pass

                # ---------- Bestätigungs-Mail an User ----------
                try:
                    context_u = {"msg": msg}
                    subject_user = (
                        "Vielen Dank für Ihre Anfrage bei datalization"
                        if msg.language == "de"
                        else "Thank you for contacting datalization"
                    )

                    text_user = render_to_string("emails/contact_user.txt", context_u)
                    html_user = render_to_string("emails/contact_user.html", context_u)

                    email_user = EmailMultiAlternatives(
                        subject=subject_user,
                        body=text_user,
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "info@datalization.ch"),
                        to=[msg.email],
                    )
                    email_user.attach_alternative(html_user, "text/html")
                    email_user.send(fail_silently=True)
                except Exception:
                    pass

            # Erfolgsmeldung Richtung Browser
            success_text = (
                "Danke! Wir melden uns in Kürze."
                if request.LANGUAGE_CODE == "de"
                else "Thank you! We'll get back to you soon."
            )

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"ok": True, "message": success_text})

            messages.success(request, success_text)
            return redirect("web:home")

        # Form invalid
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)

        messages.error(
            request,
            "Bitte prüfen Sie Ihre Eingaben."
            if request.LANGUAGE_CODE == "de"
            else "Please check your input."
        )
        return redirect("web:home")

    # GET
    form = ContactForm(initial={"language": request.LANGUAGE_CODE})
    return render(request, "contact.html", {"form": form})