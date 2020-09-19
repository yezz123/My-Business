from django.views import View
from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from common.mixins import AccessModelMixin, PermissionsRequiredMixin, NextPageMixin
from servers.models import Server
from servers.forms import ServerForm
from servers.linode_api import get_linode, get_linodes, get_bootstrap_colored_status


class ListView(PermissionsRequiredMixin, View):
    def get(self, request):
        servers = Server.objects.all()
        linodes = get_linodes()
        for server in servers:
            for linode in linodes:
                if server.uid == linode.id:
                    setattr(server, "label", linode.label)
                    setattr(server, "status", [get_bootstrap_colored_status(linode.status), linode.status])
                    setattr(server, "region", linode.region.id)
        return render(request=request, template_name="servers/list.html", context={"servers": servers})


class CreateView(PermissionsRequiredMixin, NextPageMixin, View):
    superuser = True

    def get(self, request):
        form = ServerForm()
        return render(request=request, template_name="servers/create.html", context={"form": form})

    def post(self, request):
        form = ServerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The server has been successfully created.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="servers/create.html", context={"form": form})


class DetailView(PermissionsRequiredMixin, AccessModelMixin, View):
    model = Server

    def get(self, request):
        linode = get_linode(self.server.uid)
        if not linode:
            messages.add_message(request, messages.ERROR, "The linode is invalid.")
            return HttpResponseRedirect(reverse("servers:list"))
        status = get_bootstrap_colored_status(linode.status)
        return render(
            request=request,
            template_name="servers/detail.html",
            context={"server": self.server, "linode": linode, "status": status},
        )


class EditView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Server

    def get(self, request):
        form = ServerForm(instance=self.server)
        return render(request=request, template_name="servers/edit.html", context={"form": form})

    def post(self, request):
        form = ServerForm(request.POST, instance=self.server)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "The server has been successfully edited.")
            return HttpResponseRedirect(self.next)
        return render(request=request, template_name="servers/edit.html", context={"form": form})


class DeleteView(PermissionsRequiredMixin, AccessModelMixin, NextPageMixin, View):
    superuser = True
    model = Server

    def get(self, request):
        return render(request=request, template_name="servers/delete.html")

    def post(self, request):
        self.server.delete()
        messages.add_message(request, messages.SUCCESS, "The server has been deleted.")
        return HttpResponseRedirect(self.next)
