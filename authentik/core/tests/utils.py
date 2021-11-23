"""Test Utils"""
from typing import Optional

from django.utils.text import slugify

from authentik.core.models import Group, User
from authentik.crypto.builder import CertificateBuilder
from authentik.crypto.models import CertificateKeyPair
from authentik.flows.models import Flow, FlowDesignation
from authentik.lib.generators import generate_id
from authentik.tenants.models import Tenant


def create_test_flow(designation: FlowDesignation = FlowDesignation.STAGE_CONFIGURATION) -> Flow:
    """Generate a flow that can be used for testing"""
    uid = generate_id(10)
    return Flow.objects.create(
        name=uid,
        title=uid,
        slug=slugify(uid),
        designation=designation,
    )


def create_test_admin_user(name: Optional[str] = None, set_password = False) -> User:
    """Generate a test-admin user"""
    uid = generate_id(20) if not name else name
    group = Group.objects.create(name=uid, is_superuser=True)
    user: User = User.objects.create(
        username=uid,
        name=uid,
        email=f"{uid}@goauthentik.io",
    )
    if set_password:
        user.set_password(uid)
    group.users.add(user)
    return user


def create_test_tenant() -> Tenant:
    """Generate a test tenant, removing all other tenants to make sure this one
    matches."""
    uid = generate_id(20)
    Tenant.objects.all().delete()
    return Tenant.objects.create(domain=uid, default=True)


def create_test_cert() -> CertificateKeyPair:
    """Generate a certificate for testing"""
    CertificateKeyPair.objects.filter(name="goauthentik.io").delete()
    builder = CertificateBuilder()
    builder.common_name = "goauthentik.io"
    builder.build(
        subject_alt_names=["goauthentik.io"],
        validity_days=360,
    )
    return builder.save()
