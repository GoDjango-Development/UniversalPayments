from django.conf import settings
from django.urls import reverse_lazy

def get_permissions(request):
    all_permissions = request.user.get_all_permissions()
    perms = {}
    objects = [
        {'app': 'misc', 'model': 'application'},
        {'app': 'auth', 'model': 'group'},
        {'app': 'auth', 'model': 'user'},
        {'app': 'admin', 'model': 'logentry'},
        {'app': 'applications', 'model': 'wellsfargoapplication'},
        {'app': 'applications', 'model': 'squaresapplication'},
        {'app': 'documentation', 'model': 'wellsfargodocumentation'},
        {'app': 'documentation', 'model': 'squaresdocumentation'},
        {'app': 'payments', 'model': 'wellsfargopayment'},
        {'app': 'payments', 'model': 'squarespayment'},
    ]

    for obj in objects:
        perms[f'{obj["app"]}_add_{obj["model"]}'] = request.user.has_perm(f'{obj["app"]}.add_{obj["model"]}')
        perms[f'{obj["app"]}_view_{obj["model"]}'] = request.user.has_perm(f'{obj["app"]}.view_{obj["model"]}')
        perms[f'{obj["app"]}_change_{obj["model"]}'] = request.user.has_perm(f'{obj["app"]}.change_{obj["model"]}')
        perms[f'{obj["app"]}_delete_{obj["model"]}'] = request.user.has_perm(f'{obj["app"]}.delete_{obj["model"]}')
        perms['has_%s_perm' % obj['model']] = any(
            perm in all_permissions for perm in
            [
                '%s.view_%s' % (obj['app'], obj['model']),
                '%s.add_%s' % (obj['app'], obj['model']),
                '%s.change_%s' % (obj['app'], obj['model']),
                '%s.delete_%s' % (obj['app'], obj['model'])
            ]
        )

    perms.update({
        'has_security_perm': request.user.is_superuser or
                             perms['has_group_perm'] or
                             perms['has_user_perm'],
        'has_applications_perm': request.user.is_superuser or
                                  perms['has_wellsfargoapplication_perm'] or
                                  perms['has_squaresapplication_perm'],
        'has_documentation_perm': request.user.is_superuser or
                                  perms['has_wellsfargodocumentation_perm'] or
                                  perms['has_squaresdocumentation_perm'],
        'has_payments_perm': request.user.is_superuser or
                                  perms['has_wellsfargopayment_perm'] or
                                  perms['has_squarespayment_perm'],
    })
    return {
        'permissions': perms
    }

def build_menu(request):
    permissions = get_permissions(request).get('permissions')
    
    return {
        'menu': [
            # APPS
            {
                'name': 'Autenticación y autorización',
                'icon': 'fas fa-user-lock',
                'models': [
                    {
                        'name': 'Grupos',
                        'icon': 'fas fa-users',
                        'url': reverse_lazy('admin:auth_group_changelist'),
                        'perms': permissions.get('has_group_perm')
                    },
                    {
                        'name': 'Usuarios',
                        'icon': 'fas fa-user',
                        'url': reverse_lazy('admin:auth_user_changelist'),
                        'perms': permissions.get('has_user_perm')
                    },
                ],
                'perms': permissions.get('has_security_perm')
            },
            {
                'name': 'Aplicaciones',
                'icon': 'fas fa-code',
                'models': [
                    {
                        'name': 'Wells Fargo',
                        'icon': '',
                        'url': reverse_lazy('admin:applications_wellsfargoapplication_changelist'),
                        'perms': permissions.get('has_wellsfargoapplication_perm')
                    },
                    {
                        'name': 'Square',
                        'icon': '',
                        'url': reverse_lazy('admin:applications_squaresapplication_changelist'),
                        'perms': permissions.get('has_squaresapplication_perm')
                    },
                ],
                'perms': permissions.get('has_applications_perm')
            },
            {
                'name': 'Documentación',
                'icon': 'fas fa-book',
                'models': [
                    {
                        'name': 'Wells Fargo',
                        'icon': '',
                        'url': reverse_lazy('admin:documentation_wellsfargodocumentation_changelist'),
                        'perms': permissions.get('has_wellsfargodocumentation_perm')
                    },
                    {
                        'name': 'Square',
                        'icon': '',
                        'url': reverse_lazy('admin:documentation_squaresdocumentation_changelist'),
                        'perms': permissions.get('has_squaresdocumentation_perm')
                    },
                ],
                'perms': permissions.get('has_documentation_perm')
            },
            {
                'name': 'Pagos',
                'icon': 'fas fa-money-bill',
                'models': [
                    {
                        'name': 'Wells Fargo',
                        'icon': '',
                        'url': reverse_lazy('admin:payments_wellsfargopayment_changelist'),
                        'perms': permissions.get('has_wellsfargopayment_perm')
                    },
                    {
                        'name': 'Square',
                        'icon': '',
                        'url': reverse_lazy('admin:payments_squarespayment_changelist'),
                        'perms': permissions.get('has_squarespayment_perm')
                    },
                ],
                'perms': permissions.get('has_payments_perm')
            },
        ]
    }