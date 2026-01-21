from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ScanTask, ScanResult
from targets.models import Target
from tools.models import Tool
from .utils import run_ping, run_dns, run_whois, run_headers
from django.http import HttpResponse
from .forms import ScanAddForm
                       

@login_required
def scan_list(request):
    scans = ScanTask.objects.filter(user=request.user)
    return render(request, 'scans/list.html', {'scans': scans})


@login_required
def scan_add(request):
    targets = Target.objects.filter(owner=request.user)
    tools = Tool.objects.filter(active=True)

    if request.method == 'POST':
        form = ScanAddForm(request.POST)
        if not form.is_valid():
            return redirect('scans:add')

        target_id = form.cleaned_data['target']
        tool_id = form.cleaned_data['tool']

        if not target_id or not tool_id:
          return redirect('scans:add')

        if not targets or not tools:
          return redirect('scans:list')

        scan = ScanTask.objects.create(
            user=request.user,
            target_id=target_id,
            tool_id=tool_id,
            status='running'
        )

        output = ""
        if scan.tool.command_key == 'ping':
         output = run_ping(scan.target.name)
        elif scan.tool.command_key == 'dns':
           output = run_dns(scan.target.name)
        elif scan.tool.command_key == 'whois':
           output = run_whois(scan.target.name)
        elif scan.tool.command_key == 'headers':
            output = run_headers(scan.target.name)

        ScanResult.objects.create(
            scan_task=scan,
            output=output
        )

        scan.status = 'done'
        scan.save()

        return redirect('scans:list')

    return render(request, 'scans/add.html', {
        'targets': targets,
        'tools': tools
    })


@login_required
def scan_delete(request, pk):
    scan = get_object_or_404(ScanTask, pk=pk, user=request.user)
    if request.method == 'POST':
        scan.delete()
        return redirect('scans:list')
    return render(request, 'scans/delete.html', {'scan': scan})

@login_required
def export_result(request, pk):
    scan = get_object_or_404(ScanTask, pk=pk, user=request.user)

    if not hasattr(scan, 'result'):
        return HttpResponse("No result available", status=404)

    response = HttpResponse(scan.result.output, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=scan_{scan.id}.txt'
    return response