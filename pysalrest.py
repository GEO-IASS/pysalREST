from collections import namedtuple
import inspect
import json
import api

__doc__ = """Welcome to the PySAL API.  Available sub URLS are: <br>
    weights <br>
    spreg <br>
    cg <br>
    common <br>
    spatial_dynamics <br>
    core <br>
    ergodic <br>
    directional <br>
    region <br>
    pysal <br>
    examples <br>
    inequality <br>
    esda
    """

Response = namedtuple('response', 'status content')

#Standard HTML Responses
OkResponse = lambda msg: Response('200 Ok', json.dumps(msg))
CreatedResponse = lambda msg: Response('201 Created', json.dumps(msg))
MalformedResponse = lambda msg: Response('400 Malformed Request', json.dumps(msg))
UnauthorizedResponse = lambda msg: Response('401 Unauthorized',json.dumps( msg))
NotFoundResponse = lambda msg: Response('404 Not found', json.dumps(msg))
UnsupportedResponse = lambda msg: Response('405 Method Not Allowed', json.dumps(msg))
ConflictResponse = lambda msg: Response('409 Conflict', json.dumps(msg))
ErrorResponse = lambda msg: Response('500 Internal Server Error', json.dumps(msg))

def get_handlers(package):
    handlers = {}
    for member_name, member in [module for module in inspect.getmembers(package) if inspect.ismodule(module[1])]:
        if [fn for name, fn in inspect.getmembers(member) if name in ('get', 'post', 'put', 'delete')]:
            print("Adding handler %s" % member_name)
            handlers[member_name]  = member
    print "With url handlers extracted from: {}".format(handlers)
    return handlers


def requesthandler(handlers, method, resource, *pathargs, **kwargs):
    """Main dispatch for calls to PySALRest; no framework specific
    code to be present after this point"""

    if not resource in handlers:
        return NotFoundResponse(handlers)

    if not hasattr(handlers[resource], method):
        return UnsupportedResponse('Unsupported method for resource') #Need to add supported method

    return getattr(handlers[resource], method)(*pathargs, **kwargs)
