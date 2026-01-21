from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from targets.models import Target
from scans.models import ScanTask
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import AdminLog

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {
        'targets_count': Target.objects.filter(owner=request.user).count(),
        'scans_count': ScanTask.objects.filter(user=request.user).count(),
    })

def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def admin_panel(request):
    context = {
        'users_count': User.objects.count(),
        'targets_count': Target.objects.count(),
        'scans_count': ScanTask.objects.count(),
    }
    return render(request, 'core/admin_panel.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    users = User.objects.all()
    return render(request, 'core/admin_users.html', {
        'users': users
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return redirect('core:admin_users')

    user.is_active = not user.is_active
    user.save()

    return redirect('core:admin_users')


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def promote_to_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # لا نعبث بالسوبر يوزر
    if user.is_superuser:
        return redirect('core:admin_users')

    user.is_staff = True
    user.save()

    return redirect('core:admin_users')

@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def demote_from_staff(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # لا نلمس السوبر يوزر
    if user.is_superuser:
        return redirect('core:admin_users')

    user.is_staff = False
    user.save()

    return redirect('core:admin_users')



@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_target_admin(request, target_id):
    Target.objects.filter(id=target_id).delete()
    return redirect('admin_panel')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def delete_scan_admin(request, scan_id):
    ScanTask.objects.filter(id=scan_id).delete()
    return redirect('admin_panel')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_targets(request):
    targets = Target.objects.select_related('owner').all()
    return render(request, 'core/admin_targets.html', {
        'targets': targets
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def admin_delete_target(request, target_id):
    target = get_object_or_404(Target, id=target_id)

    AdminLog.objects.create(
        admin=request.user,
        action=f"Deleted target '{target.name}' (ID {target.id}) owned by {target.owner.username}"
    )

    target.delete()
    return redirect('core:admin_targets')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_scans(request):
    scans = ScanTask.objects.select_related('user', 'target', 'tool').all()
    return render(request, 'core/admin_scans.html', {
        'scans': scans
    })


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
@require_POST
def admin_delete_scan(request, scan_id):
    scan = get_object_or_404(ScanTask, id=scan_id)

    AdminLog.objects.create(
        admin=request.user,
        action=f"Deleted scan ID {scan.id} for target '{scan.target.name}'"
    )

    scan.delete()
    return redirect('core:admin_scans')


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_logs(request):
    logs = AdminLog.objects.select_related('admin').order_by('-created_at')
    return render(request, 'core/admin_logs.html', {
        'logs': logs
    })


@login_required
def staff_panel(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    context = {
        'targets_count': Target.objects.count(),
        'scans_count': ScanTask.objects.count(),
        'logs_count': AdminLog.objects.count(),
    }
    return render(request, 'core/staff_panel.html', context)
