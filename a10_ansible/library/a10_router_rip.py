#!/usr/bin/python

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")


DOCUMENTATION = """
module: a10_router_rip
description:
    - None
short_description: Configures A10 router.rip
author: A10 Networks 2018 
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
        - present
        - absent
        required: True
    a10_host:
        description:
        - Host for AXAPI authentication
        required: True
    a10_username:
        description:
        - Username for AXAPI authentication
        required: True
    a10_password:
        description:
        - Password for AXAPI authentication
        required: True
    default_metric:
        description:
        - "None"
        required: False
    route_cfg:
        description:
        - "Field route_cfg"
        required: False
        suboptions:
            route:
                description:
                - "None"
    cisco_metric_behavior:
        description:
        - "None"
        required: False
    uuid:
        description:
        - "None"
        required: False
    rip_maximum_prefix_cfg:
        description:
        - "Field rip_maximum_prefix_cfg"
        required: False
        suboptions:
            maximum_prefix:
                description:
                - "None"
            maximum_prefix_thres:
                description:
                - "None"
    offset_list:
        description:
        - "Field offset_list"
        required: False
        suboptions:
            acl_cfg:
                description:
                - "Field acl_cfg"
            uuid:
                description:
                - "None"
    passive_interface_list:
        description:
        - "Field passive_interface_list"
        required: False
        suboptions:
            tunnel:
                description:
                - "None"
            ethernet:
                description:
                - "None"
            trunk:
                description:
                - "None"
            ve:
                description:
                - "None"
            loopback:
                description:
                - "None"
    redistribute:
        description:
        - "Field redistribute"
        required: False
        suboptions:
            vip_list:
                description:
                - "Field vip_list"
            redist_list:
                description:
                - "Field redist_list"
            uuid:
                description:
                - "None"
    neighbor:
        description:
        - "Field neighbor"
        required: False
        suboptions:
            value:
                description:
                - "None"
    network_interface_list_cfg:
        description:
        - "Field network_interface_list_cfg"
        required: False
        suboptions:
            tunnel:
                description:
                - "None"
            ethernet:
                description:
                - "None"
            trunk:
                description:
                - "None"
            ve:
                description:
                - "None"
            loopback:
                description:
                - "None"
    recv_buffer_size:
        description:
        - "None"
        required: False
    timers:
        description:
        - "Field timers"
        required: False
        suboptions:
            timers_cfg:
                description:
                - "Field timers_cfg"
    version:
        description:
        - "None"
        required: False
    default_information:
        description:
        - "None"
        required: False
    distribute_list:
        description:
        - "Field distribute_list"
        required: False
        suboptions:
            acl_cfg:
                description:
                - "Field acl_cfg"
            prefix:
                description:
                - "Field prefix"
            uuid:
                description:
                - "None"
    distance_list_cfg:
        description:
        - "Field distance_list_cfg"
        required: False
        suboptions:
            distance:
                description:
                - "None"
            distance_ipv4_mask:
                description:
                - "None"
            distance_acl:
                description:
                - "None"
    network_addresses:
        description:
        - "Field network_addresses"
        required: False
        suboptions:
            network_ipv4_mask:
                description:
                - "None"


"""

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = ["cisco_metric_behavior","default_information","default_metric","distance_list_cfg","distribute_list","neighbor","network_addresses","network_interface_list_cfg","offset_list","passive_interface_list","recv_buffer_size","redistribute","rip_maximum_prefix_cfg","route_cfg","timers","uuid","version",]

# our imports go at the top so we fail fast.
try:
    from a10_ansible import errors as a10_ex
    from a10_ansible.axapi_http import client_factory, session_factory
    from a10_ansible.kwbl import KW_IN, KW_OUT, translate_blacklist as translateBlacklist

except (ImportError) as ex:
    module.fail_json(msg="Import Error:{0}".format(ex))
except (Exception) as ex:
    module.fail_json(msg="General Exception in Ansible module import:{0}".format(ex))


def get_default_argspec():
    return dict(
        a10_host=dict(type='str', required=True),
        a10_username=dict(type='str', required=True),
        a10_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=["present", "absent"])
    )

def get_argspec():
    rv = get_default_argspec()
    rv.update(dict(
        default_metric=dict(type='int',),
        route_cfg=dict(type='list',route=dict(type='str',)),
        cisco_metric_behavior=dict(type='str',choices=['enable','disable']),
        uuid=dict(type='str',),
        rip_maximum_prefix_cfg=dict(type='dict',maximum_prefix=dict(type='int',),maximum_prefix_thres=dict(type='int',)),
        offset_list=dict(type='dict',acl_cfg=dict(type='list',ve=dict(type='str',),loopback=dict(type='str',),tunnel=dict(type='str',),metric=dict(type='int',),offset_list_direction=dict(type='str',choices=['in','out']),acl=dict(type='str',),trunk=dict(type='str',),ethernet=dict(type='str',)),uuid=dict(type='str',)),
        passive_interface_list=dict(type='list',tunnel=dict(type='str',),ethernet=dict(type='str',),trunk=dict(type='str',),ve=dict(type='str',),loopback=dict(type='str',)),
        redistribute=dict(type='dict',vip_list=dict(type='list',vip_metric=dict(type='int',),vip_route_map=dict(type='str',),vip_type=dict(type='str',choices=['only-flagged','only-not-flagged'])),redist_list=dict(type='list',metric=dict(type='int',),route_map=dict(type='str',),ntype=dict(type='str',choices=['bgp','connected','floating-ip','ip-nat-list','ip-nat','isis','lw4o6','nat-map','ospf','static'])),uuid=dict(type='str',)),
        neighbor=dict(type='list',value=dict(type='str',)),
        network_interface_list_cfg=dict(type='list',tunnel=dict(type='str',),ethernet=dict(type='str',),trunk=dict(type='str',),ve=dict(type='str',),loopback=dict(type='str',)),
        recv_buffer_size=dict(type='int',),
        timers=dict(type='dict',timers_cfg=dict(type='dict',val_3=dict(type='int',),val_2=dict(type='int',),basic=dict(type='int',))),
        version=dict(type='int',),
        default_information=dict(type='str',choices=['originate']),
        distribute_list=dict(type='dict',acl_cfg=dict(type='list',acl_direction=dict(type='str',choices=['in','out']),ve=dict(type='str',),loopback=dict(type='str',),tunnel=dict(type='str',),acl=dict(type='str',),trunk=dict(type='str',),ethernet=dict(type='str',)),prefix=dict(type='dict',uuid=dict(type='str',),prefix_cfg=dict(type='list',ve=dict(type='str',),loopback=dict(type='str',),tunnel=dict(type='str',),prefix_list=dict(type='str',),trunk=dict(type='str',),prefix_list_direction=dict(type='str',choices=['in','out']),ethernet=dict(type='str',))),uuid=dict(type='str',)),
        distance_list_cfg=dict(type='list',distance=dict(type='int',),distance_ipv4_mask=dict(type='str',),distance_acl=dict(type='str',)),
        network_addresses=dict(type='list',network_ipv4_mask=dict(type='str',))
    ))

    return rv

def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/router/rip"
    f_dict = {}

    return url_base.format(**f_dict)

def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/router/rip"
    f_dict = {}

    return url_base.format(**f_dict)


def build_envelope(title, data):
    return {
        title: data
    }

def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")

def _build_dict_from_param(param):
    rv = {}

    for k,v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        if isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv

def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            if isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)

def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([x for x in requires_one_of if params.get(x)])
    
    errors = []
    marg = []
    
    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc,msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc,msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc,msg = REQUIRED_VALID
    
    if not rc:
        errors.append(msg.format(", ".join(marg)))
    
    return rc,errors

def get(module):
    return module.client.get(existing_url(module))

def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return False

def create(module, result):
    payload = build_json("rip", module)
    try:
        post_result = module.client.post(new_url(module), payload)
        result.update(**post_result)
        result["changed"] = True
    except a10_ex.Exists:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def delete(module, result):
    try:
        module.client.delete(existing_url(module))
        result["changed"] = True
    except a10_ex.NotFound:
        result["changed"] = False
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def update(module, result, existing_config):
    payload = build_json("rip", module)
    try:
        post_result = module.client.put(existing_url(module), payload)
        result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result

def present(module, result, existing_config):
    if not exists(module):
        return create(module, result)
    else:
        return update(module, result, existing_config)

def absent(module, result):
    return delete(module, result)

def run_command(module):
    run_errors = []

    result = dict(
        changed=False,
        original_message="",
        message=""
    )

    state = module.params["state"]
    a10_host = module.params["a10_host"]
    a10_username = module.params["a10_username"]
    a10_password = module.params["a10_password"]
    # TODO(remove hardcoded port #)
    a10_port = 443
    a10_protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        map(run_errors.append, validation_errors)
    
    if not valid:
        result["messages"] = "Validation failure"
        err_msg = "\n".join(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(a10_host, a10_port, a10_protocol, a10_username, a10_password)
    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)
        module.client.session.close()
    elif state == 'absent':
        result = absent(module, result)
        module.client.session.close()
    return result

def main():
    module = AnsibleModule(argument_spec=get_argspec())
    result = run_command(module)
    module.exit_json(**result)

# standard ansible module imports
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()