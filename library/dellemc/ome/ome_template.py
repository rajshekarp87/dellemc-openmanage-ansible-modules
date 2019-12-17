#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.1
# Copyright (C) 2019 Dell Inc.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# All rights reserved. Dell, EMC, and other trademarks are trademarks of Dell Inc. or its subsidiaries.
# Other trademarks may be trademarks of their respective owners.
#


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ome_template
short_description: Create, modify or deploy a template.
version_added: "2.8"
description: This module creates, modifies or deploys a template.
options:
  hostname:
    description: Target IP Address or hostname.
    type: str
    required: true
  username:
    description: Target username.
    type: str
    required: true
  password:
    description: Target user password.
    type: str
    required: true
  port:
    description: Target HTTPS port.
    type: int
    default: 443
  state:
    description:
      - C(create) creates a new template.
      - C(modify) modifies an existing template.
      - >-
        C(deploy) deploys an existing template. To deploy a template on iDRAC, ensure the appropriate license is
        present. Refer OpenManage Enterprise Licensing Guide for more details.
    choices: [create, modify, deploy]
    type: str
    default: create
  template_id:
    description:
      - Unique ID of the template to be modified or deployed.
      - This option is mandatory for C(modify) and C(deploy) operations.
    type: int
  template_name:
    description:
      - Unique Name of the template to be modified or deployed.
      - This option is mandatory for C(modify) and C(deploy) operations.
    type: str
  device_id:
    description:
      - List of targeted device id(s) for C(deploy) or a single id for C(create).
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    default: []
  device_service_tag:
    description:
      - List of targeted device service tag(s) for C(deploy) or a single service tag for C(create).
      - Either I(device_id) or I(device_service_tag) is mandatory or both can be applicable.
    type: list
    default: []
  template_view_type:
    description:
      - The features that support template operations.
      - This is applicable only for C(create)
    choices: [Deployment, Compliance, Inventory, Sample, None]
    type: str
    default: Deployment
  attributes:
    type: dict
    default: {}
    description:
      - >-
        Payload data for the template operations. It can take the following values.
      - >-
        Name: Name of the template. This is mandatory for C(create) and C(modify) operations.
      - >-
        Description: Description of the template. This is applicable for C(create) and C(modify) operations.
      - >-
        Fqdds: This provides functionality to copy only certain areas of system configuration from the specified
        reference server. One or more of the following values may be specified in a comma-separated string: iDRAC,
        System, BIOS, NIC, LifeCycleController, RAID, EventFilters, All. Default value is 'All'. This is applicable for
        C(create) operation.
      - >-
        Options: Options to control device shutdown or end power state during template deployment. This is applicable
        for C(deploy) operation.
      - >-
        Schedule: Options to schedule the deployment task immediately or at a specified time. This is applicable for
        C(deploy) operation.
      - >-
        NetworkBootIsoModel: Payload to specify the ISO deployment details. This is applicable for C(deploy) operation.
      - >-
        Attributes: list of dictionaries of attribute values (if any) to be modified in the template to be deployed.
        This is applicable for C(modify) and C(deploy) operations.
      - >-
        Refer OpenManage Enterprise API Reference Guide for more details.
requirements:
    - "python >= 2.7.5"
author: "Jagadeesh N V (@jagadeeshnv)"
'''

EXAMPLES = r'''
---
- name: "Create a template from a reference device."
  ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    device_id: 25123
    attributes:
      Name: "New Template"
      Description: "New Template description"

- name: "Modify template name, description, and attribute value."
  ome_template:
    hostname: "192.168.0.1"
    username: "username"
    password: "password"
    state: "modify"
    template_id: 1234
    attributes:
      Name: "New Custom Template"
      Description: "Custom Template Description"
      # Attributes to be modified in the template.
      # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
      # This section is optional
      Attributes:
        - Id: 1234
          Value: "Test Attribute"
          IsIgnored: false

- name: "Deploys template on multiple devices and changes the device level attributes. After the template is deployed,
an operating system can be installed using its image."
  ome_template:
    hostname:  "192.168.0.1"
    username: "username"
    password: "password"
    state: "deploy"
    template_id: 1234
    device_id:
      - 12765
      - 10173
    device_service_tag:
      - 'SVTG123'
      - 'SVTG456'
    attributes:
      # Device specific attributes to be modified during deployment.
      # For information on any attribute id, use API /TemplateService/Templates(Id)/Views(Id)/AttributeViewDetails
      # This section is optional
      Attributes:
        # specific device where attribute to be modified at deployment run-time.
        # The DeviceId should be mentioned above in the 'device_id' section.
        # Service tags not allowed.
        - DeviceId: 12765
          Attributes:
            - Id : 15645
              Value : "0.0.0.0"
              IsIgnored : false
        - DeviceId: 10173
          Attributes:
            - Id : 18968,
              Value : "hostname-1"
              IsIgnored : false
      # Include this to install operating system on the devices.
      # This section is optional
      NetworkBootIsoModel:
        BootToNetwork: false
        ShareType: "NFS"
        IsoPath: "/home/iso_path/filename.iso"
        ShareDetail:
          IpAddress: "192.168.0.2"
          ShareName: "sharename"
          User: "share_user"
          Password: "share_password"
      Options:
        EndHostPowerState: 1
        ShutdownType: 0
        TimeToWaitBeforeShutdown: 300
      Schedule:
        RunLater: true
        RunNow: false
'''

RETURN = r'''
---
msg:
  description: Overall status of the template operation.
  returned: always
  type: str
  sample: "Successfully created a Template with id 123"
return_id:
  description: id of the template for C(create) and C(modify) or task created in case of C(deploy)
  returned: success
  type: int
  sample: 124
template_status:
  description: Details of the HTTP Error.
  returned: on HTTP error
  type: dict
  sample: {
    "error": {
      "code": "Base.1.0.GeneralError",
      "message": "A general error has occurred. See ExtendedInfo for more information.",
      "@Message.ExtendedInfo": [
        {
          "MessageId": "GEN1234",
          "RelatedProperties": [],
          "Message": "Unable to process the request because an error occurred.",
          "MessageArgs": [],
          "Severity": "Critical",
          "Resolution": "Retry the operation. If the issue persists, contact your system administrator."
        }
      ]
    }
  }
'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.remote_management.dellemc.ome import RestOME
from ansible.module_utils.six.moves.urllib.error import URLError, HTTPError
from ansible.module_utils.urls import ConnectionError, SSLValidationError


def get_device_ids(module, rest_obj):
    """Getting the list of device ids filtered from the device inventory."""
    device_id = list(map(str, module.params.get('device_id')))
    for devid in device_id:
        if not devid.isdigit():
            fail_module(module, msg="Invalid device id {0} found. Please provide a valid number".format(devid))
    service_tags = module.params.get('device_service_tag')
    if not service_tags:
        return list(set(device_id))
    device_uri = "DeviceService/Devices"
    resp = rest_obj.invoke_request('GET', device_uri)
    if resp.success and resp.json_data.get('value'):
        device_resp = {device.get('DeviceServiceTag'): str(device.get('Id')) for device in resp.json_data.get('value', [])}
        device_tags = list(map(str, service_tags))
        invalid_tags = []
        for tag in device_tags:
            if device_resp.get(tag):
                device_id.append(device_resp.get(tag))
            else:
                invalid_tags.append(tag)
        if invalid_tags:
            fail_module(module, msg="Unable to complete the operation because the entered target service"
                                    " tag(s) '{0}' are invalid.".format(",".join(set(invalid_tags))))
    else:
        fail_module(module, msg="Failed to fetch the device ids.")
    invalid_ids = set(device_id) - set(device_resp.values())
    if invalid_ids:
        fail_module(module, msg="Unable to complete the operation because the entered target device"
                                " id(s) '{0}' are invalid.".format(",".join(list(map(str, set(invalid_ids))))))
    return list(map(int, set(device_id)))


def get_view_id(rest_obj, viewstr):
    resp = rest_obj.invoke_request('GET', "TemplateService/TemplateViewTypes")
    if resp.success and resp.json_data.get('value'):
        tlist = resp.json_data.get('value', [])
        for xtype in tlist:
            if xtype.get('Description', "") == viewstr:
                return xtype.get('Id')
    viewmap = {"Deployment": 2, "Compliance": 1, "Inventory": 3, "Sample": 4, "None": 0}
    return viewmap.get(viewstr)


def get_create_payload(module_params, deviceid, view_id):
    create_payload = {"Fqdds": "All",  # Mandatory for create
                      "ViewTypeId": view_id}
    if isinstance(module_params.get("attributes"), dict):
        create_payload.update(module_params.get("attributes"))
    create_payload["SourceDeviceId"] = int(deviceid)
    return create_payload


def get_modify_payload(module_params, template_id):
    modify_payload = {}
    if isinstance(module_params.get("attributes"), dict):
        modify_payload.update(module_params.get("attributes"))
    modify_payload['Id'] = template_id
    return modify_payload


def get_deploy_payload(module_params, deviceidlist, template_id):
    deploy_payload = {}
    # deploy_payload["NetworkBootIsoModel"] = {"BootToNetwork": False}
    deploy_payload["Options"] = {"ShutdownType": 1,
                                 "TimeToWaitBeforeShutdown": 300,
                                 "EndHostPowerState": 1}
    deploy_payload["Schedule"] = {"RunNow": True, "RunLater": False,
                                  "Cron": None, "StartTime": None, "EndTime": None}
    if isinstance(module_params.get("attributes"), dict):
        deploy_payload.update(module_params.get("attributes"))
    deploy_payload["Id"] = template_id
    deploy_payload["TargetIds"] = deviceidlist
    return deploy_payload


def get_template_by_name(template_name, module, rest_obj):
    """Filter out specific template based on name, and it returns template_id.

    :param template_name: string
    :param module: dictionary
    :param rest_obj: object
    :return: template_id: integer
    """
    template_id = None
    template_path = "TemplateService/Templates"
    query_param = {"$filter": "Name eq '{0}'".format(template_name)}
    template_req = rest_obj.invoke_request("GET", template_path, query_param=query_param)
    for each in template_req.json_data.get('value'):
        if each['Name'] == template_name:
            template_id = each['Id']
            break
    else:
        fail_module(module, msg="Unable to complete the operation because the"
                                " requested template is not present.")
    return template_id


def _get_resource_parameters(module, rest_obj):
    state = module.params.get("state")
    template_id = module.params.get("template_id")
    template_name = module.params.get("template_name")
    if state == "create":
        devid_list = get_device_ids(module, rest_obj)
        if len(devid_list) != 1:
            fail_module(module, msg="Create template requires only one reference device")
        view_id = get_view_id(rest_obj, module.params['template_view_type'])
        payload = get_create_payload(module.params, devid_list[0], view_id)
        path = "TemplateService/Templates"
        rest_method = 'POST'
    elif state == "modify":
        if template_name:
            template_id = get_template_by_name(template_name, module, rest_obj)
        path = "TemplateService/Templates({template_id})".format(template_id=template_id)
        payload = get_modify_payload(module.params, template_id)
        rest_method = 'PUT'
    else:
        devid_list = get_device_ids(module, rest_obj)
        path = "TemplateService/Actions/TemplateService.Deploy"
        if template_name:
            template_id = get_template_by_name(template_name, module, rest_obj)
        payload = get_deploy_payload(module.params, devid_list, template_id)
        rest_method = 'POST'
    return path, payload, rest_method


def _validate_inputs(module):
    """validates input parameters"""
    state = module.params.get("state")
    template_id = module.params.get("template_id")
    template_name = module.params.get("template_name")
    if not state == "modify":
        dev_id = module.params["device_id"]
        dev_st = module.params["device_service_tag"]
        if not isinstance(dev_id, list) or not isinstance(dev_st, list):
            fail_module(module, msg="Argument device_id or device_service_tag is not of valid type - list")
        if None in dev_id or None in dev_st:
            fail_module(module, msg="Argument device_id or device_service_tag has null values")
        if ((len(dev_id) + len(dev_st)) != 1) and state == "create":
            fail_module(module, msg="Create template operation accepts either a single device id or a single device"
                                    " service tag")
    if state in ("modify", "deploy") and not isinstance(template_id, int) and not isinstance(template_name, str):
        fail_module(module, msg="one of the following is required: template_id, template_name")
    elif state in ("modify", "deploy") and (isinstance(template_id, int) and isinstance(template_name, str)):
        fail_module(module, msg="parameters are mutually exclusive: template_id|template_name")


def password_no_log(attributes):
    if isinstance(attributes, dict):
        netdict = attributes.get("NetworkBootIsoModel")
        if isinstance(netdict, dict):
            sharedet = netdict.get("ShareDetail")
            if isinstance(sharedet, dict) and 'Password' in sharedet:
                sharedet['Password'] = "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"


def fail_module(module, **failmsg):
    password_no_log(module.params.get("attributes"))
    module.fail_json(**failmsg)


def exit_module(module, response):
    password_no_log(module.params.get("attributes"))
    msg_dict = {'create': "Successfully created a Template with id {0}".format(response.json_data),
                'modify': "Successfully modified the Template with id {0}".format(response.json_data),
                'deploy': "Successfully created the Template-deployment job with id {0}".format(response.json_data)}
    state = module.params.get('state')
    module.exit_json(msg=msg_dict.get(state), changed=True, return_id=response.json_data)


def main():
    module = AnsibleModule(
        argument_spec={
            "hostname": {"required": True, "type": 'str'},
            "username": {"required": True, "type": 'str'},
            "password": {"required": True, "type": 'str', "no_log": True},
            "port": {"required": False, "default": 443, "type": 'int'},
            "state": {"required": False, "default": "create",
                      "choices": ['create', 'modify', 'deploy']},
            "template_id": {"required": False, "type": 'int'},
            "template_name": {"required": False, "type": 'str'},
            "template_view_type": {"required": False, "default": 'Deployment',
                                   "choices": ['Deployment', 'Compliance', 'Inventory', 'Sample', 'None']},
            "device_id": {"required": False, "type": 'list', "default": [], "elements": 'int'},
            "device_service_tag": {"required": False, "type": 'list', "default": [], "elements": 'str'},
            "attributes": {"required": False, "type": 'dict', "default": {}},
        },
        required_if=[['state', 'create', ['attributes']]],
        supports_check_mode=False)

    try:
        _validate_inputs(module)
        with RestOME(module.params, req_session=True) as rest_obj:
            path, payload, rest_method = _get_resource_parameters(module, rest_obj)
            resp = rest_obj.invoke_request(rest_method, path, data=payload)
            if resp.success:
                exit_module(module, resp)
    except HTTPError as err:
        fail_module(module, msg=str(err), template_status=json.load(err))
    except (URLError, SSLValidationError, ConnectionError, TypeError, ValueError, KeyError) as err:
        fail_module(module, msg=str(err))


if __name__ == '__main__':
    main()
