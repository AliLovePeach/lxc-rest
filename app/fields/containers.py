#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_restplus import fields
from app import api


lxc_container_conf = api.model('LxcContainerConf', {
    'aa_allow_incomplete': fields.Integer(default=0),
    'aa_profile': fields.String,
    'arch': fields.String,
    'autodev': fields.Integer(default=1),
    'cap': fields.Nested(api.model('LxcCap', {
        'drop': fields.List(fields.String),
        'keep': fields.List(fields.String)
    })),
    'cgroup': fields.Nested(api.model('LxcCgroup', {
        'memory': fields.Nested(api.model('LxcCgroupMemory', {
            'limit_in_bytes': fields.Integer,
            'memsw': fields.Nested(api.model('LxcCgroupMemoryMemsw', {
                'limit_in_bytes': fields.Integer
            }))
        })),
        'cpu': fields.Nested(api.model('LxcCgroupCpu', {
            'shares': fields.Integer(default=1024)
        })),
        'cpuset': fields.Nested(api.model('LxcCgroupCpuset', {
            'cpus': fields.List(fields.String)
        }))
    })),
    'console': fields.Nested(api.model('LxcConsole', {
        '_': fields.String,
        'logfile': fields.String
    })),
    'devttydir': fields.String,
    'environment': fields.List(fields.String),
    'ephemeral': fields.Integer(default=0),
    'group': fields.List(fields.String),
    'haltsignal': fields.String(default='SIGPWR'),
    'hook': fields.Nested(api.model('LxcHook', {
        'autodev': fields.List(fields.String),
        'clone': fields.List(fields.String),
        'destroy': fields.List(fields.String),
        'mount': fields.List(fields.String),
        'post-stop': fields.List(fields.String),
        'pre-mount': fields.List(fields.String),
        'pre-start': fields.List(fields.String),
        'start': fields.List(fields.String),
        'stop': fields.List(fields.String)
    })),
    'id_map': fields.String,
    'include': fields.String,
    'init_cmd': fields.String,
    'init_gid': fields.Integer(default=0),
    'init_uid': fields.Integer(default=0),
    'kmsg': fields.Integer(default=0),
    'logfile': fields.String,
    'loglevel': fields.Integer(default=5),
    'monitor': fields.Nested(api.model('LxcMonitor', {
        'unshare': fields.Integer(default=0)
    })),
    'mount': fields.Nested(api.model('LxcMount', {
        '_': fields.String,
        'auto': fields.String,
        'entry': fields.List(fields.String)
    })),
    'network': fields.Nested(api.model('LxcNetwork', {
        'type': fields.String,
        'veth': fields.Nested(api.model('LxcNetworkVeth', {
            'pair': fields.Integer
        })),
        'vlan': fields.Nested(api.model('LxcNetworkVlan', {
            'id': fields.Integer
        })),
        'macvlan': fields.Nested(api.model('LxcNetworkMacvlan', {
            'mode': fields.String
        })),
        'flags': fields.String,
        'link': fields.String,
        'mtu': fields.Integer,
        'name': fields.String,
        'hwaddr': fields.String,
        'ipv4': fields.Nested(api.model('LxcNetworkIpv4', {
            '_': fields.List(fields.String),
            'gateway': fields.String
        })),
        'ipv6': fields.Nested(api.model('LxcNetworkIpv6', {
            '_': fields.List(fields.String),
            'gateway': fields.String
        })),
        'script': fields.Nested(api.model('LxcNetworkScript', {
            'up': fields.String,
            'down': fields.String
        }))
    }), as_list=True),
    'no_new_privs': fields.Integer(default=0),
    'pts': fields.String,
    'rebootsignal': fields.String(default='SIGINT'),
    'rootfs': fields.Nested(api.model('LxcRootfs', {
        '_': fields.String,
        'mount': fields.String,
        'options': fields.String,
        'backend': fields.String
    })),
    'se_context': fields.String,
    'seccomp': fields.String,
    'start': fields.Nested(api.model('LxcStart', {
        'auto': fields.Integer(default=0),
        'delay': fields.Integer(default=None),
        'order': fields.Integer(default=None)
    })),
    'stopsignal': fields.String(default='SIGKILL'),
    'syslog': fields.String,
    'tty': fields.String,
    'utsname': fields.String
})

containers_fields_attributes = api.model('ContainersFieldsAttributes', {
    'name': fields.String,
    'pid': fields.Integer,
    'state': fields.String,
    'lxc': fields.Nested(lxc_container_conf)
})

containers_fields_attributes_post = api.model('ContainersFieldsAttributesPost', {
    'name': fields.String(required=True, pattern='^(?!\s*$).+'),
    'template': fields.Nested(api.model('ContainersTemplatePost', {
        'name': fields.String(required=True, pattern='^(?!\s*$).+'),
        'args': fields.List(fields.String)
    })),
    'lxc': fields.Nested(lxc_container_conf)
})

containers_fields_with_relationships_post_put = api.model('ContainersFieldsWithRelationshipsPost', {
    'relationships': fields.Nested(api.model('ContainersRelationshipsPost', {
        'users': fields.Nested(api.model('ContainersDataPost', {
            'data': fields.Nested(api.model('ContainersPostData', {
                'type': fields.String(pattern='users'),
                'id': fields.Integer
            }), as_list=True)
        })),
    }))
})

containers_fields_get = api.inherit('ContainersFieldsGet', containers_fields_with_relationships_post_put, {
    'type': fields.String,
    'id': fields.Integer,
    'attributes': fields.Nested(containers_fields_attributes),
})

containers_fields_post = api.inherit('ContainersFieldsPost', containers_fields_with_relationships_post_put, {
    'type': fields.String(pattern='containers'),
    'attributes': fields.Nested(containers_fields_attributes_post),
})

containers_fields_put = api.inherit('ContainersFieldsPut', containers_fields_with_relationships_post_put, {
    'type': fields.String(pattern='containers'),
    'attributes': fields.Nested(containers_fields_attributes),
})
