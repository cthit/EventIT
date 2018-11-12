import os

DEBUG = True

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = os.environ.get('MONGO_PORT', 27017)
MONGO_USERNAME = os.environ.get('MONGO_USERNAME', 'root')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', 'password')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'EventIT')

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']

users = {
    'description': 'Unique identifiers which allows tickets and booked locations to be associated with a single user',
    'schema': {
        'roles': {
            'description': 'List of the roles belonging to the user. Determines which locations can be booked etc.',
            'type': 'list',
            'schema': {
                'description': 'References a role through its id.',
                'type': 'objectid',
                'data_relation': {
                    'resource': 'roles',
                    # make the role embeddable with ?embedded={"roles":1}
                    'embeddable': True
                }
            }
        }
    }
}

events = {
    'description': 'The events on EventIT',
    'schema': {
        'location-bookings': {
            'description': 'The set of locations associated with the event',
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'location': {
                        'description': 'References a Location',
                        'type': 'objectid',
                        'data_relation': {
                            'resource': 'locations',
                            'embeddable': True
                        }
                    },
                    'is_open_event': {
                        'description': 'Weather or not the location is open to the public',
                        'type': 'boolean'
                    }
                }
            }
        },
        'start-date': {
            'type': 'datetime',
            'required': True
        },
        'end-date': {
            'type': 'datetime',
            'required': True
        },
        'requires-tickets': {
            'type': 'boolean',
            'default': False
        },
        'ticket-price': {
            'type': 'integer'
        },
        'ticket-amount': {
            'type': 'integer'
        },
        'extra-fields': {
            'type': 'dict',
            'allow_unknown': True
        }
    }
}

bookings = {
    'schema': {
        'event': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'events',
                # make the role embeddable with ?embedded={"user":1}
                'embeddable': True
            }
        },
        'owner': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                # make the role embeddable with ?embedded={"user":1}
                'embeddable': True
            }
        },
        'status': {
            'type': 'string',
            'allowed': ["USED", "READY_FOR_USE", "PAYMENT_PENDING"]
        },
        # TODO implement custom validation routine for the extra fields
        'extra-fields': {
            'type': 'dict',
            'allow_unknown': True
        }
    }
}

locations = {
    'description': 'A location on which an event can be held',
    'schema': {
        'name': {
            'description': 'The name of the location',
            'example': 'Hubben 2.1',
            'type': 'string'
        },
        'address': {
            'description': 'The address of the location',
            'example': 'Hörsalsvägen 9, 412 58 Göteborg',
            'type': 'string'
        },
        'description': {
            'description': 'A short description of the location',
            'example': 'An awesome place for awesome people!',
            'type': 'string'
        },
        'coordinate': {
            'type': 'point',
            'example': {
                "type": "Point",
                "coordinates": [
                    57.688348, 11.979196
                ]
            }
        },
        'ruleset': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'location-rulesets',
                # make the role embeddable with ?embedded={"location-ruleset":1}
                'embeddable': True
            }
        }
    }
}

location_rulesets = {
    'description': 'Determines when a location is available to book depending on user role.',
    'schema': {
        'rulesets': {
            'type': 'list',
            'schema': {
                'role': {
                    'description': 'The role for which this rule applies',
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'roles',
                        # make the role embeddable with ?embedded={"role":1}
                        'embeddable': True
                    }
                },
                'time-rules': {
                    'type': 'list',
                    'schema': {
                        "rule-type": {
                            'description': 'Weather or not the rule should ALLOW or BLOCK bookings during the '
                                           'specified time',
                            'example': 'ALLOW',
                            'type': 'string',
                            'allowed': ["ALLOW", "BLOCK"],
                            'required': True
                        },
                        'timespan-start': {
                            'type': 'datetime',
                            'required': True
                        },
                        'timespan-end': {
                            'type': 'datetime',
                            'required': True
                        },
                        "repeat-every": {
                            'type': 'string',
                            'allowed': ["DAY", "WEEK", "MONTH", "YEAR"]
                        },
                    }
                }
            }
        }
    }
}

roles = {
    'description': 'A role represents an access level that determines when a user is allowed to book a location.',
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'role_name'
    },
    'schema': {
        'role_name': {
            'description': 'A suitable name for the role',
            'example': 'DEFAULT_USER_ROLE',
            'type': 'string',
            'required': True
        }
    }
}

DOMAIN = {
    'users': users,
    'events': events,
    'bookings': bookings,
    'locations': locations,
    'location-rulesets': location_rulesets,
    'roles': roles
}
