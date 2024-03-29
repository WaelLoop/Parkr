"""Generated client library for cloudbilling version v1."""
# NOTE: This file is autogenerated and should not be edited by hand.
from apitools.base.py import base_api
from googlecloudsdk.third_party.apis.cloudbilling.v1 import cloudbilling_v1_messages as messages


class CloudbillingV1(base_api.BaseApiClient):
  """Generated client library for service cloudbilling version v1."""

  MESSAGES_MODULE = messages
  BASE_URL = u'https://cloudbilling.googleapis.com/'

  _PACKAGE = u'cloudbilling'
  _SCOPES = [u'https://www.googleapis.com/auth/cloud-platform']
  _VERSION = u'v1'
  _CLIENT_ID = '1042881264118.apps.googleusercontent.com'
  _CLIENT_SECRET = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _USER_AGENT = 'x_Tw5K8nnjoRAqULM9PFAC2b'
  _CLIENT_CLASS_NAME = u'CloudbillingV1'
  _URL_VERSION = u'v1'
  _API_KEY = None

  def __init__(self, url='', credentials=None,
               get_credentials=True, http=None, model=None,
               log_request=False, log_response=False,
               credentials_args=None, default_global_params=None,
               additional_http_headers=None, response_encoding=None):
    """Create a new cloudbilling handle."""
    url = url or self.BASE_URL
    super(CloudbillingV1, self).__init__(
        url, credentials=credentials,
        get_credentials=get_credentials, http=http, model=model,
        log_request=log_request, log_response=log_response,
        credentials_args=credentials_args,
        default_global_params=default_global_params,
        additional_http_headers=additional_http_headers,
        response_encoding=response_encoding)
    self.billingAccounts_projects = self.BillingAccountsProjectsService(self)
    self.billingAccounts = self.BillingAccountsService(self)
    self.projects = self.ProjectsService(self)
    self.services_skus = self.ServicesSkusService(self)
    self.services = self.ServicesService(self)

  class BillingAccountsProjectsService(base_api.BaseApiService):
    """Service class for the billingAccounts_projects resource."""

    _NAME = u'billingAccounts_projects'

    def __init__(self, client):
      super(CloudbillingV1.BillingAccountsProjectsService, self).__init__(client)
      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      r"""Lists the projects associated with a billing account. The current.
authenticated user must have the `billing.resourceAssociations.list` IAM
permission, which is often given to billing account
[viewers](https://cloud.google.com/billing/docs/how-to/billing-access).

      Args:
        request: (CloudbillingBillingAccountsProjectsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListProjectBillingInfoResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}/projects',
        http_method=u'GET',
        method_id=u'cloudbilling.billingAccounts.projects.list',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'pageSize', u'pageToken'],
        relative_path=u'v1/{+name}/projects',
        request_field='',
        request_type_name=u'CloudbillingBillingAccountsProjectsListRequest',
        response_type_name=u'ListProjectBillingInfoResponse',
        supports_download=False,
    )

  class BillingAccountsService(base_api.BaseApiService):
    """Service class for the billingAccounts resource."""

    _NAME = u'billingAccounts'

    def __init__(self, client):
      super(CloudbillingV1.BillingAccountsService, self).__init__(client)
      self._upload_configs = {
          }

    def Create(self, request, global_params=None):
      r"""Creates a billing account.
This method can only be used to create
[billing subaccounts](https://cloud.google.com/billing/docs/concepts)
by GCP resellers.
When creating a subaccount, the current authenticated user must have the
`billing.accounts.update` IAM permission on the main account, which is
typically given to billing account
[administrators](https://cloud.google.com/billing/docs/how-to/billing-access).
This method will return an error if the main account has not been
provisioned as a reseller account.

      Args:
        request: (BillingAccount) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (BillingAccount) The response message.
      """
      config = self.GetMethodConfig('Create')
      return self._RunMethod(
          config, request, global_params=global_params)

    Create.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'POST',
        method_id=u'cloudbilling.billingAccounts.create',
        ordered_params=[],
        path_params=[],
        query_params=[],
        relative_path=u'v1/billingAccounts',
        request_field='<request>',
        request_type_name=u'BillingAccount',
        response_type_name=u'BillingAccount',
        supports_download=False,
    )

    def Get(self, request, global_params=None):
      r"""Gets information about a billing account. The current authenticated user.
must be a [viewer of the billing
account](https://cloud.google.com/billing/docs/how-to/billing-access).

      Args:
        request: (CloudbillingBillingAccountsGetRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (BillingAccount) The response message.
      """
      config = self.GetMethodConfig('Get')
      return self._RunMethod(
          config, request, global_params=global_params)

    Get.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}',
        http_method=u'GET',
        method_id=u'cloudbilling.billingAccounts.get',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1/{+name}',
        request_field='',
        request_type_name=u'CloudbillingBillingAccountsGetRequest',
        response_type_name=u'BillingAccount',
        supports_download=False,
    )

    def GetIamPolicy(self, request, global_params=None):
      r"""Gets the access control policy for a billing account.
The caller must have the `billing.accounts.getIamPolicy` permission on the
account, which is often given to billing account
[viewers](https://cloud.google.com/billing/docs/how-to/billing-access).

      Args:
        request: (CloudbillingBillingAccountsGetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('GetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}:getIamPolicy',
        http_method=u'GET',
        method_id=u'cloudbilling.billingAccounts.getIamPolicy',
        ordered_params=[u'resource'],
        path_params=[u'resource'],
        query_params=[u'options_requestedPolicyVersion'],
        relative_path=u'v1/{+resource}:getIamPolicy',
        request_field='',
        request_type_name=u'CloudbillingBillingAccountsGetIamPolicyRequest',
        response_type_name=u'Policy',
        supports_download=False,
    )

    def List(self, request, global_params=None):
      r"""Lists the billing accounts that the current authenticated user has.
permission to
[view](https://cloud.google.com/billing/docs/how-to/billing-access).

      Args:
        request: (CloudbillingBillingAccountsListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListBillingAccountsResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'cloudbilling.billingAccounts.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'filter', u'pageSize', u'pageToken'],
        relative_path=u'v1/billingAccounts',
        request_field='',
        request_type_name=u'CloudbillingBillingAccountsListRequest',
        response_type_name=u'ListBillingAccountsResponse',
        supports_download=False,
    )

    def Patch(self, request, global_params=None):
      r"""Updates a billing account's fields.
Currently the only field that can be edited is `display_name`.
The current authenticated user must have the `billing.accounts.update`
IAM permission, which is typically given to the
[administrator](https://cloud.google.com/billing/docs/how-to/billing-access)
of the billing account.

      Args:
        request: (CloudbillingBillingAccountsPatchRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (BillingAccount) The response message.
      """
      config = self.GetMethodConfig('Patch')
      return self._RunMethod(
          config, request, global_params=global_params)

    Patch.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}',
        http_method=u'PATCH',
        method_id=u'cloudbilling.billingAccounts.patch',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[u'updateMask'],
        relative_path=u'v1/{+name}',
        request_field=u'billingAccount',
        request_type_name=u'CloudbillingBillingAccountsPatchRequest',
        response_type_name=u'BillingAccount',
        supports_download=False,
    )

    def SetIamPolicy(self, request, global_params=None):
      r"""Sets the access control policy for a billing account. Replaces any existing.
policy.
The caller must have the `billing.accounts.setIamPolicy` permission on the
account, which is often given to billing account
[administrators](https://cloud.google.com/billing/docs/how-to/billing-access).

      Args:
        request: (CloudbillingBillingAccountsSetIamPolicyRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (Policy) The response message.
      """
      config = self.GetMethodConfig('SetIamPolicy')
      return self._RunMethod(
          config, request, global_params=global_params)

    SetIamPolicy.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}:setIamPolicy',
        http_method=u'POST',
        method_id=u'cloudbilling.billingAccounts.setIamPolicy',
        ordered_params=[u'resource'],
        path_params=[u'resource'],
        query_params=[],
        relative_path=u'v1/{+resource}:setIamPolicy',
        request_field=u'setIamPolicyRequest',
        request_type_name=u'CloudbillingBillingAccountsSetIamPolicyRequest',
        response_type_name=u'Policy',
        supports_download=False,
    )

    def TestIamPermissions(self, request, global_params=None):
      r"""Tests the access control policy for a billing account. This method takes.
the resource and a set of permissions as input and returns the subset of
the input permissions that the caller is allowed for that resource.

      Args:
        request: (CloudbillingBillingAccountsTestIamPermissionsRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (TestIamPermissionsResponse) The response message.
      """
      config = self.GetMethodConfig('TestIamPermissions')
      return self._RunMethod(
          config, request, global_params=global_params)

    TestIamPermissions.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/billingAccounts/{billingAccountsId}:testIamPermissions',
        http_method=u'POST',
        method_id=u'cloudbilling.billingAccounts.testIamPermissions',
        ordered_params=[u'resource'],
        path_params=[u'resource'],
        query_params=[],
        relative_path=u'v1/{+resource}:testIamPermissions',
        request_field=u'testIamPermissionsRequest',
        request_type_name=u'CloudbillingBillingAccountsTestIamPermissionsRequest',
        response_type_name=u'TestIamPermissionsResponse',
        supports_download=False,
    )

  class ProjectsService(base_api.BaseApiService):
    """Service class for the projects resource."""

    _NAME = u'projects'

    def __init__(self, client):
      super(CloudbillingV1.ProjectsService, self).__init__(client)
      self._upload_configs = {
          }

    def GetBillingInfo(self, request, global_params=None):
      r"""Gets the billing information for a project. The current authenticated user.
must have [permission to view the
project](https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo
).

      Args:
        request: (CloudbillingProjectsGetBillingInfoRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ProjectBillingInfo) The response message.
      """
      config = self.GetMethodConfig('GetBillingInfo')
      return self._RunMethod(
          config, request, global_params=global_params)

    GetBillingInfo.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/projects/{projectsId}/billingInfo',
        http_method=u'GET',
        method_id=u'cloudbilling.projects.getBillingInfo',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1/{+name}/billingInfo',
        request_field='',
        request_type_name=u'CloudbillingProjectsGetBillingInfoRequest',
        response_type_name=u'ProjectBillingInfo',
        supports_download=False,
    )

    def UpdateBillingInfo(self, request, global_params=None):
      r"""Sets or updates the billing account associated with a project. You specify.
the new billing account by setting the `billing_account_name` in the
`ProjectBillingInfo` resource to the resource name of a billing account.
Associating a project with an open billing account enables billing on the
project and allows charges for resource usage. If the project already had a
billing account, this method changes the billing account used for resource
usage charges.

*Note:* Incurred charges that have not yet been reported in the transaction
history of the GCP Console might be billed to the new billing
account, even if the charge occurred before the new billing account was
assigned to the project.

The current authenticated user must have ownership privileges for both the
[project](https://cloud.google.com/docs/permissions-overview#h.bgs0oxofvnoo
) and the [billing
account](https://cloud.google.com/billing/docs/how-to/billing-access).

You can disable billing on the project by setting the
`billing_account_name` field to empty. This action disassociates the
current billing account from the project. Any billable activity of your
in-use services will stop, and your application could stop functioning as
expected. Any unbilled charges to date will be billed to the previously
associated account. The current authenticated user must be either an owner
of the project or an owner of the billing account for the project.

Note that associating a project with a *closed* billing account will have
much the same effect as disabling billing on the project: any paid
resources used by the project will be shut down. Thus, unless you wish to
disable billing, you should always call this method with the name of an
*open* billing account.

      Args:
        request: (CloudbillingProjectsUpdateBillingInfoRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ProjectBillingInfo) The response message.
      """
      config = self.GetMethodConfig('UpdateBillingInfo')
      return self._RunMethod(
          config, request, global_params=global_params)

    UpdateBillingInfo.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/projects/{projectsId}/billingInfo',
        http_method=u'PUT',
        method_id=u'cloudbilling.projects.updateBillingInfo',
        ordered_params=[u'name'],
        path_params=[u'name'],
        query_params=[],
        relative_path=u'v1/{+name}/billingInfo',
        request_field=u'projectBillingInfo',
        request_type_name=u'CloudbillingProjectsUpdateBillingInfoRequest',
        response_type_name=u'ProjectBillingInfo',
        supports_download=False,
    )

  class ServicesSkusService(base_api.BaseApiService):
    """Service class for the services_skus resource."""

    _NAME = u'services_skus'

    def __init__(self, client):
      super(CloudbillingV1.ServicesSkusService, self).__init__(client)
      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      r"""Lists all publicly available SKUs for a given cloud service.

      Args:
        request: (CloudbillingServicesSkusListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListSkusResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        flat_path=u'v1/services/{servicesId}/skus',
        http_method=u'GET',
        method_id=u'cloudbilling.services.skus.list',
        ordered_params=[u'parent'],
        path_params=[u'parent'],
        query_params=[u'currencyCode', u'endTime', u'pageSize', u'pageToken', u'startTime'],
        relative_path=u'v1/{+parent}/skus',
        request_field='',
        request_type_name=u'CloudbillingServicesSkusListRequest',
        response_type_name=u'ListSkusResponse',
        supports_download=False,
    )

  class ServicesService(base_api.BaseApiService):
    """Service class for the services resource."""

    _NAME = u'services'

    def __init__(self, client):
      super(CloudbillingV1.ServicesService, self).__init__(client)
      self._upload_configs = {
          }

    def List(self, request, global_params=None):
      r"""Lists all public cloud services.

      Args:
        request: (CloudbillingServicesListRequest) input message
        global_params: (StandardQueryParameters, default: None) global arguments
      Returns:
        (ListServicesResponse) The response message.
      """
      config = self.GetMethodConfig('List')
      return self._RunMethod(
          config, request, global_params=global_params)

    List.method_config = lambda: base_api.ApiMethodInfo(
        http_method=u'GET',
        method_id=u'cloudbilling.services.list',
        ordered_params=[],
        path_params=[],
        query_params=[u'pageSize', u'pageToken'],
        relative_path=u'v1/services',
        request_field='',
        request_type_name=u'CloudbillingServicesListRequest',
        response_type_name=u'ListServicesResponse',
        supports_download=False,
    )
